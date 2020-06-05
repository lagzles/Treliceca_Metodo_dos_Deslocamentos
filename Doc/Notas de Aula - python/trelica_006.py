import nos as ns
import barras_001 as b
import rigidez_002 as rig
from numpy import zeros


espacamento_padrao = 2.0

coord_y = {}
coord_x = {}
nos = {}
x = 0
y = 0

e = 300
a = 400


class Trelica(object):
    def __init__(self, h, pontos_vao, cumeeira, cumeeira_alinhada_com_pilar, vento, vt):
        self.h_viga = h
        self.cumeeira = cumeeira
        self.cumeeira_alinhada = cumeeira_alinhada_com_pilar
        self.vento = vento
        self.nos_objetos = []
        self.barras_objetos = []
        self.vt = vt
        self.pontos_vao = pontos_vao
        print('Viga Treliçada')
        print('altura da Viga', h)
        
        # setado por metodos
        self.carregamentos = []
        self.k = None # matriz rigidez
        self.ua = None # deslocamentos nodais
        self.fa_grav = None
        self.fa_cv = None

        pre_gdl = 4
        i_d = 1
        self.gdl = 4 
        
        for i in range(len(pontos_vao)-1):
            xi = [pontos_vao[i][0], pontos_vao[i][1]]
            xf = [pontos_vao[i+1][0], pontos_vao[i+1][1]]
            if i == 0:
                primeiro_vao = True
            else:
                primeiro_vao = False
        
            indice_inicial = 0
            if primeiro_vao == False:
                indice_inicial = 2

            # método para coordenadas das barras de cada vão!
            parcial = self.barras_e_nos_trelica(xi, xf, primeiro_vao, pre_gdl)
            # itera nos nós da trelica parcial, para acrescentar aos da
            # treliça completa
            for ni in range(indice_inicial, len(parcial[0])):
                n = parcial[0][ni]
                self.nos_objetos.append(n)
            
            pre_gdl = self.nos_objetos[-1].gy
            
            for b in parcial[1]:
                b.id = i_d
                self.barras_objetos.append(b)
                i_d += 1
        self.gdl = len(self.nos_objetos) * 2
        
        print('gdl ', self.gdl)


    def montar_matrizes_trelica(self):        
        gdl = len(self.nos_objetos) * 2
        self.gdl = gdl
        
        print('montando matriz de rigidez 1')
        print('carregamentos \n', self.carregamentos)
        #print(gdl, "gdl dos nós")
        #print(self.gdl, "gdl do objeto")
        k = zeros((gdl,gdl))

        liv = []
        ap = []
        fa = []
        # monta a lista de graus de liberdade 'livres' e a listagem de 'apoios'
        for no in self.nos_objetos:
            if no.fx != 'x':
                liv = liv + [no.gx - 1]
                fa = fa + [no.fx]
            else:
                ap = ap + [no.gx - 1]
                
            if no.fy != 'x':
                liv = liv + [no.gy - 1]
                fa = fa + [no.fy]
            else:
                ap = ap + [no.gy - 1]

        # monta a matriz de rigidez da Treliça
        fa_grav = []
        fa_cv = []
        # para cada carregamento, aplica a carga nos nós
        for carregamento in self.carregamentos:
            for barra in self.barras_objetos:
                barra.set_gdl(gdl)
                k = k + barra.kci                
                tipo_barra = barra.tipo.split("-")[-1]                
                if tipo_barra == 'superior':
                    if self.vt != 1: # caso a viga seja de cobertura
                        dx = abs(barra.nf.x - barra.ni.x)
                        # 2xcaregamento, pois considera que é o carregamento dos dois banzos conectados no nó
                        barra.ni.fy = carregamento * dx - barra.peso*0.5
                        barra.nf.fy = carregamento * dx - barra.peso*0.5
                    elif self.vt == 1: # caso a viga seja de transição
                        # cada 'vano' é o valor de vão entre pontos de aplicação de carga
                        for vano in self.pontos_vao:
                            #print(vano)
                            if vano[0] == barra.ni.x and vano[0] != 0.00 and vano[0] < self.cumeeira:                                
                                valor_de_carga = carregamento - (barra.peso*0.5)
                                barra.ni.set_fy(valor_de_carga)
                                
                                # por algum motivo, o nó da barra esta diferente dos nós da lista
                                # localiza o nó necessario pela 'id'
                                ni_id = barra.ni.id
                                for no in self.nos_objetos:
                                    no_id = no.id
                                    if no_id == ni_id:
                                        no.fy = valor_de_carga
                                        
                                print('carga nas coordenadas:', barra.ni.x, barra.ni.y, barra.ni.id, barra.ni.fy)
                            else:
                                barra.ni.fy = 0
            
            #for carregamento in self.carregamentos:
            #for no in self.nos_objetos:
            #    if no.fy != 0:
            #        no.fy = carregamento
            # monta a lista de graus de liberdade 'livres' e a listagem de 'apoios'
            # para cada carregamento (gravitacional, vento), monta as matrizes de vinculações
            i = 0
            j = 0
            for no in self.nos_objetos:
                if no.fx != 'x':
                    if carregamento > 0:
                        fa_cv = fa_cv + [no.fx]
                        #i += 1
                    elif carregamento <= 0:
                        fa_grav = fa_grav + [no.fx]
                        #j += 1
                    
                if no.fy != 'x':
                    if carregamento > 0:
                        fa_cv = fa_cv + [no.fy]
                        i += 1
                    elif carregamento <= 0:
                        fa_grav = fa_grav + [no.fy]
                        
            
        self.k = k        
        self.liv = liv
        self.ap = ap
        self.fa_grav = fa_grav        
        self.fa_cv = fa_cv
        
    
    def set_carregamentos(self, carregamentos):
        self.carregamentos = carregamentos
        return carregamentos


    def analise_matricial(self):
        if len(self.carregamentos) != 0:
            # re monta as matrizes, caso modifique as barras
            # rigidez, vinculações, esforços externos
            self.montar_matrizes_trelica()
            
            rig.analise_matriz_carregamentos(self)

    def barras_e_nos_trelica(self, xi, xf, primeiro_vao, pre_gdl):
        h_viga = self.h_viga
        ponto_i = xi
        ponto_f = xf
        vento = self.vento
        primeiro_vao = primeiro_vao
        pre_gdl = pre_gdl
        cumeeira = self.cumeeira
        cumeeira_alinhada = self.cumeeira_alinhada
        
        # Definições de vãos para vigas de cobertura
        vao = abs(ponto_f[0] - ponto_i[0])
        meio_vao = round(vao/2 + ponto_i[0],2)
        n_v_montantes_i = 1
        vaof = 0 # valor dfinal do vao
        ix = 1 # indice inicial das coordenadas 'x'
        iy = 1 # indice inicial das coordenadas 'y'
        dy = 0 # variação da coordenada 'y', conforme inclinação
        inclinacao = 3.0 / 100.0
        aclive_declive = 1
        espacamento_max = 2
        
        y = round(ponto_i[1],2)
        
        if ponto_i[1] < ponto_f[1]:
            aclive_declive = 1
        else:
            aclive_declive = -1
        
        espacamento_calc = 2.1
        vaof += ponto_f[0]
        x = round(ponto_i[0], 2)
        
        n_vao_montantes = round(vao / espacamento_padrao, 0)

        # Definições de vãos para Vigas de Transição
        # print(self.vt, "vt")
        if self.vt == 1:
            meio_vao = cumeeira / 2.0
            espacamento_max = h_viga
            espacamento_calc = espacamento_max + 0.2
            aclive_declive = 0
            n_vao_montantes = round(vao / espacamento_max, 0)
            #print(xi, xf, " xi, xf")
            #print(h_viga, "h_viga")
            #print(n_vao_montantes, "n_vao_montantes")
            
        # calcula distancia entre montantes
        while espacamento_calc > espacamento_max:
            espacamento_calc = vao / n_vao_montantes
            n_vao_montantes +=1

        coord_x[ix] = x

        # acrescentando banzos, até o valor ser menor que o ponto final
        # coordenadas x, para cada nó inicial e final das barras de banzo
        while x < vaof:
            x += espacamento_calc
            ix += 1        
            coord_x[ix] = round(x, 2)
            
        coord_y[iy] = y

        # coordenadas y, utilizando a quantidade de montantes calculadas
        # conforme espacamento entre montantes
        for k in range(int(n_v_montantes_i), int(n_v_montantes_i + n_vao_montantes - 1)):
            dy = espacamento_calc * inclinacao
            y += dy * aclive_declive
            iy += 1
            coord_y[iy] = round(y,2)
            
        iy += 1
        coord_y[iy] = y = ponto_f[1]
        nos_objetos = {}
        barras_objetos = []
        nos_objetos_list = []
        
        # preenchimento do dicionario de pontos (x,y)
        for i in range(int(n_v_montantes_i), int(n_v_montantes_i + n_vao_montantes)):
            # graus de liberdade dos nós superiores        
            js = i * 4  + pre_gdl - 4# vertical
            jss = js - 1 # horizontal
            # graus de liberdade dos nós inferiores 
            ji = js - 2 # vertical
            jii = jss - 2 # horizontal

            rx = 0
            ry = 0

            # define restrições caso pontos sejam apoios        
            if i == 1 or i == int(n_v_montantes_i + n_vao_montantes - 1):            
                ultimo_i = int(n_v_montantes_i + n_vao_montantes - 1)
                
                # caso seja o primeiro, ou o ultimo, montante do vão
                if i == 1 and primeiro_vao == True:
                    # casos eja o primeiro montante do vão, e seja o primeiro dos vãos da viga
                    rx = "x"
                    ry = "x"
                    #print(rx, ry, "vinculações 1")
                    #print(coord_x[i], coord_y[i])
                    
                # para vigas que não são de transição. VIGAS DE COBERTURA
                if self.vt != 1:   
                    # caso seja 1 vão apenas, alinhado com cumeeira
                    if i == ultimo_i: # caso ultimo montante
                        if ponto_f[0] == cumeeira or ponto_i[0] == cumeeira:
                            # caso ponto final seja cota da cumeeira
                            if cumeeira_alinhada == True:
                                if coord_x[i] == cumeeira:
                                    ry = "x"
                                    #print(rx, ry, "vinculações 2")
                                    #print(coord_x[i], coord_y[i])
                    
                if primeiro_vao == False:
                    if i == ultimo_i: # caso ultimo montante
                        #se coordenada for cumeeira e cumeeira alinhada com pilar
                        if cumeeira_alinhada == True and coord_x[i] == cumeeira and coord_x[i] == ponto_f[0]:
                            ry = "x"
                            #print(rx, ry, "vinculações 3")
                            #print(coord_x[i], coord_y[i])
                        # se coordenada final for equivalente ao ponto final do vão
                        elif coord_x[i] == ponto_f[0] and self.vt != 1:
                            ry = "x"
                            #print(rx, ry, "vinculações 4")
                            #print(coord_x[i], coord_y[i])
                        elif coord_x[i] == cumeeira:
                            ry = "x"
                            #print(rx, ry, "vinculações 5")
                            #print(coord_x[i], coord_y[i])
                    
            # pontos dos banzos inferiores
            xi = coord_x[i]
            yi = round(coord_y[i],2)

            nos[i]=[xi, yi]    
            nos_objetos[i] = ns.Nos(xi, yi, jii, ji, rx, ry)
            nos_objetos_list.append(nos_objetos[i])
            #self.nos_objetos.append(nos_objetos[i])
            
            # pontos dos banzos superiores
            rx = 0
            # setado valor inicial, para identificação posterior
            ry = -10
            
            xf = xi
            yf = round(coord_y[i]+h_viga,2)

            nos[i+n_vao_montantes]=[xf, yf]
            nos_objetos[i+n_vao_montantes] = ns.Nos(xf, yf, jss, js, rx, ry)
            nos_objetos_list.append(nos_objetos[i+n_vao_montantes])
            #self.nos_objetos.append(nos_objetos[i+n_vao_montantes])

        j = 0
        gdl = len(nos) * 2

        #print(gdl," gdl no método")
        #print(self.gdl, "gdl do self")
        #self.gdl += gdl
        #print(self.gdl, "gdl do self +=")
        
        barras_objetos = []
        
        # lançamento de banzos
        for i in range(int(1), int(1+n_vao_montantes-1)):
            # banzo inferior
            n1a = nos_objetos[i]
            n2a = nos_objetos[i+1]
            
            barr = b.Barras(n1a, n2a, gdl, 'banzo-inferior')
            barras_objetos.append(barr)
                    
            # banzo superior
            k = i + int(n_vao_montantes)
            n1b = nos_objetos[k]
            n2b = nos_objetos[k + 1]
            
            barr = b.Barras(n1b, n2b, gdl, 'banzo-superior')
            barras_objetos.append(barr)

            # montante(s)
            # desenha o primeiro montante, se for o primeiro vão da sequencia
            if i == 1 and primeiro_vao == True:
                barr = b.Barras(n1a, n1b, gdl, 'montante')
                barras_objetos.append(barr)

            # desenha montantes, que não sejam o primeiro 
            if i != 1:
                barr = b.Barras(n1a, n1b, gdl, 'montante')
                barras_objetos.append(barr)

            # desenha o ultimo montante do vao
            if i == (n_vao_montantes - 1):
                barr = b.Barras(n2a, n2b, gdl, 'montante')
                barras_objetos.append(barr)
            # Orientação sempre da esquerda para direita
            if vento == 1:
                if n1a.x < meio_vao:
                    barr = b.Barras(n1a, n2b, gdl, 'diagonal')
                    barras_objetos.append(barr)
                else:
                    barr = b.Barras(n1b, n2a, gdl, 'diagonal')
                    barras_objetos.append(barr)
            else:
                if n1a.x < meio_vao:
                    barr = b.Barras(n1b, n2a, gdl, 'diagonal')
                    barras_objetos.append(barr)
                else:
                    barr = b.Barras(n1a, n2b, gdl, 'diagonal')
                    barras_objetos.append(barr)
         
        barras_objetos = barras_objetos
        return (nos_objetos_list, barras_objetos)#, plt)

