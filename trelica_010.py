import nos_001 as ns
import barras_002 as b
import rigidez_002 as rig
import math as m
from numpy import zeros

espacamento_padrao = 2.0

coord_y = {}
coord_x = {}
nos = {}
x = 0
y = 0

class Trelica(object):
    # def __init__(self, h, pontos_vao, cumeeira, cumeeira_alinhada_com_pilar, vento, vt, banzo_reto):
    def __init__(self, n_vaos, lista_vaos, cumeeira, vao_secundaria, altura_viga, vento, vt, banzo_reto):

        self.geometrizar_inputs(n_vaos, lista_vaos, cumeeira, vao_secundaria, altura_viga, vento, vt, banzo_reto)

        self.fa_externa = None
        print('Viga Treliçada - h=', self.h_viga)
        
        # setado por metodos
        self.carregamentos = []
        self.peso = 0
        self.peso_dobrado = 0
        self.peso_soldado = 0
        self.peso_miscelanias = 0
        self.pecas = 0
        self.peso_linear = 0
        
        self.k = None # matriz rigidez
        self.ua = None # deslocamentos nodais
        self.fa_grav = None
        self.fa_cv = None
        self.reacoes_grav = None
        self.reacoes_cv = None
        self.conjunto_banzos = []

        i_d = 1
        pre_gdl = 4
        self.gdl = 4 
        
        self.comprimento = self.pontos_vao[-1][0]

        for i in range(len(self.pontos_vao)-1):
            xi = [self.pontos_vao[i][0], self.pontos_vao[i][1]]
            xf = [self.pontos_vao[i+1][0], self.pontos_vao[i+1][1]]
            if i == 0:
                primeiro_vao = True
            else:
                primeiro_vao = False
        
            indice_inicial = 0
            if primeiro_vao == False:
                indice_inicial = 2

            # método para coordenadas das barras de cada vão!
            parcial = self.barras_e_nos_trelica(xi, xf, primeiro_vao, pre_gdl)
            # parcial = self.barras_e_nos_trelica_menor(xi, xf, primeiro_vao, pre_gdl)

            # itera nos nós da trelica parcial, para acrescentar aos da treliça inteira
            # monta a treliça completa, com 'apppend' das parciais
            for ni in range(indice_inicial, len(parcial[0])):
                n = parcial[0][ni]
                self.nos_objetos.append(n)
            
            pre_gdl = self.nos_objetos[-1].gy
            
            for b in parcial[1]:
                b.id = i_d
                self.barras_objetos.append(b)
                i_d += 1
        i = 0 
        ii = 0
        for barra in self.barras_objetos:
            ii = max(barra.ni.gy, barra.nf.gy)
            i = max(ii, i)

        self.gdl = len(self.nos_objetos) * 2
        
        # self.gdl = i

        # loop verifica se os nós iniciais e finais das barras, são os mesmo da lista de objetos.
        # devido a logica de criação das listas, nem todas as barras estão com os mesmos nós da lista de nós
        for barra in self.barras_objetos:
            # if barra.ni not in self.nos_objetos:
            if barra.get_ni() not in self.nos_objetos:
                for noh in self.nos_objetos:
                    # barra_no_id = barra.ni.id
                    barra_no_id = barra.get_ni().id
                    no_lista_id = noh.id
                    if barra_no_id == no_lista_id:
                        barra.set_ni(noh)

            if barra.get_nf() not in self.nos_objetos:
                for noh in self.nos_objetos:
                    barra_no_id = barra.get_nf().id
                    no_lista_id = noh.id
                    if barra_no_id == no_lista_id:
                        barra.set_nf(noh)# = noh
        self.propriedades()

    def geometrizar_inputs(self, n_vaos, lista_vaos, cumeeira, vao_secundaria, altura_viga, vento, vt, banzo_reto):
        pontos_viga = []        
        # pontos 1 e 2, do primeiro pilar
        pontos_viga.append([0, 0])

        cumeeira_alinhada_com_pilar = False

        # Rotina faz uma distribuição das coordenadas da viga de cobertura, considerando a inclinação da viga
        # Pontos de Banzo Inferior
        if vt == 0:
            inc = 3

            largura_parcial = 0
            pe_direito = 0
            
            h_cumeeira = pe_direito + (cumeeira * inc / 100.)
            #############################################
            for vao in lista_vaos:
                largura_parcial += vao
                if largura_parcial < cumeeira:
                    cota_trecho = pe_direito + largura_parcial * inc / 100.

                elif largura_parcial == cumeeira:
                    cumeeira_alinhada_com_pilar = True            
                    cota_trecho = h_cumeeira
                    
                elif  largura_parcial > cumeeira:
                    cota_trecho = h_cumeeira - (largura_parcial - cumeeira) * inc / 100.

                if largura_parcial > cumeeira and (largura_parcial-vao) < cumeeira:
                    pontos_viga.append([cumeeira, h_cumeeira])
                    
                pontos_viga.append([largura_parcial, cota_trecho])
            
            if altura_viga == 0:
                h_viga = round(max(lista_vaos)/14,2)
            else:
                h_viga = altura_viga
            
            
        elif vt == 1:
            inc = 0
            vao_vt = cumeeira
            
            if altura_viga == 0:
                h_viga = round(vao_vt / 14, 2)
            else:
                h_viga = altura_viga
            var_vao = 0
            
            for i in lista_vaos:
                var_vao += i
                pontos_viga.append([var_vao, 0])
                
            pontos_viga.append([vao_vt, 0])

        self.h_viga = h_viga
        self.cumeeira = cumeeira
        self.cumeeira_alinhada = cumeeira_alinhada_com_pilar
        self.vento = vento
        self.nos_objetos = []
        self.barras_objetos = []
        self.vt = vt
        self.banzo_reto = banzo_reto
        self.pontos_vao = pontos_viga


    ################################################################################################
    ################################################################################################
    ################################# FUNÇÕES DO METODO DA RIGIDEZ #################################
    ################################################################################################
    ################################################################################################
    def montar_matrizes_trelica(self):        
        gdl = len(self.nos_objetos) * 2
        self.gdl = gdl
        
        k = zeros((gdl,gdl))

        liv = []
        ap = []
        # monta a lista de graus de liberdade 'livres' e a listagem de 'apoios'
        # cuidar a ordem de preenchimento, conforme graus de liberdade
        # primeiro 'x' depois 'y'
        for no in self.nos_objetos:
            if no.apoio == 'duplo':
                ap = ap + [no.gx-1]
                ap = ap + [no.gy-1]

            elif no.apoio == 'simples':
                ap = ap + [no.gy - 1]
                liv = liv + [no.gx - 1] 

            elif no.apoio == False:
                liv = liv + [no.gx-1]
                liv = liv + [no.gy-1]

        # monta a matriz de rigidez da Treliça
        fa_grav = []
        fa_cv = []
        fa_externa = []
        # para cada carregamento, aplica a carga nos nós
        for carregamento in self.carregamentos:
            # antes de cada carregamento, se zera as cargas aplicadas nos nós
            for barra in self.barras_objetos:
                tipo_barra = barra.tipo.split("-")[-1]
                if tipo_barra == 'superior':
                    barra.get_ni().set_fy(0)
                    barra.get_nf().set_fy(0)# fy = 0
                elif tipo_barra == 'inferior':
                    barra.get_ni().set_fy(0)
                    barra.get_nf().set_fy(0)# fy = 0
                else:
                    barra.get_ni().set_fy(0)
                    barra.get_nf().set_fy(0)# fy = 0
                    barra.get_ni().set_fx(0)
                    barra.get_nf().set_fx(0)# fy = 0

            for barra in self.barras_objetos:
                barra.set_gdl(gdl)
                k = k + barra.get_kci()
                # por padrao, banzos são separados em: 'banzo-superior' e 'banzo-inferior'
                tipo_barra = barra.tipo.split("-")[-1]
                if self.vt != 1: # situação de viga de cobertura
                    dx = barra.comprimento()
                    if tipo_barra == 'superior': # carregamento nos banzos superiores
                        # considerando que esta sendo aplicado o carregamento das duas barras adjacentes ao nó
                        barra.get_ni().add_fy(carregamento * (0.5 * dx) - barra.get_peso()*0.5)
                        barra.get_nf().add_fy(carregamento * (0.5 * dx) - barra.get_peso()*0.5)

                    else: #if tipo_barra == 'inferior': # adicionar peso próprio nos banzos inferiores, diagonais, montantes
                        barra.get_ni().add_fy(-barra.get_peso()*0.5)#*m.sin(barra.theta))
                        barra.get_nf().add_fy(-barra.get_peso()*0.5)#*m.sin(barra.theta))

                elif self.vt == 1: # caso a viga seja de transição
                    barra.get_ni().add_fy(-barra.get_peso()*0.5)
                    barra.get_nf().add_fy(-barra.get_peso()*0.5)
                    if tipo_barra == 'superior':
                        # cada 'vano' é o valor de vão entre pontos de aplicação de carga
                        for vano in self.pontos_vao:
                            if vano[0] == barra.get_ni().get_x() and vano[0] != 0.00 and vano[0] < self.cumeeira:
                                valor_de_carga = carregamento - (barra.get_peso()*0.5)
                                barra.get_ni().set_fy(valor_de_carga)
                                
                                # por algum motivo, o nó da barra esta diferente dos nós da lista
                                # localiza o nó necessario pela 'id'
                                ni_id = barra.get_ni().get_id()
                                for no in self.nos_objetos:
                                    no_id = no.get_id()
                                    if no_id == ni_id:
                                        no.set_fy(valor_de_carga)
                                        print('carga nas coordenadas:', barra.get_ni().get_x(), barra.ni.y, barra.ni.id, barra.ni.fy)
                                        break

            # monta a lista de graus de liberdade 'livres' e a listagem de 'apoios'
            # para cada carregamento (gravitacional, vento), monta as matrizes de vinculações
            for no in self.nos_objetos:
                if carregamento > 0:
                    fa_cv = fa_cv + [no.get_fx()]
                    fa_cv = fa_cv + [no.get_fy()]
                elif carregamento <= 0 :
                    fa_grav = fa_grav + [no.get_fx()]
                    fa_grav = fa_grav + [no.get_fy()]

        self.k = k
        self.liv = liv
        self.ap = ap
        self.fa_grav = fa_grav
        self.fa_cv = fa_cv
        self.fa_externa = fa_externa
        
    
    def set_carregamentos(self, carregamentos):
        self.carregamentos = carregamentos
        return carregamentos


    def analise_matricial(self):
        if len(self.carregamentos) != 0:
            pass
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
        if cumeeira == ponto_i[0] and not cumeeira_alinhada:
            meio_vao = 0
        elif cumeeira == ponto_f[0] and not cumeeira_alinhada:
            meio_vao = vao
        else:
            meio_vao = round(vao/2 + ponto_i[0],2)
        # n_v_montantes_i = 1
        vaof = 0 # valor dfinal do vao
        ix = 1 # indice inicial das coordenadas 'x'
        iy = 1 # indice inicial das coordenadas 'y'
        dy = 0 # variação da coordenada 'y', conforme inclinação
        inclinacao = 3.0 / 100.0
        aclive_declive = 1
        espacamento_max = 2
        
        y = round(ponto_i[1],2)
        
        # verifica qual tem a coordenada Y maior
        if ponto_i[1] < ponto_f[1]:
            aclive_declive = 1
        else:
            aclive_declive = -1
        
        espacamento_calc = 2.1
        vaof += ponto_f[0]
        x = round(ponto_i[0], 2)
        
        n_vao_montantes = round(vao / espacamento_padrao, 0)

        kxi = 4
        kxs = 1
        ky = 1
        kx = 1

        # Definições de vãos para Vigas de Transição
        if self.vt == 1:
            meio_vao = cumeeira / 2.0
            espacamento_max = h_viga
            espacamento_calc = espacamento_max + 0.2
            aclive_declive = 0
            n_vao_montantes = round(vao / espacamento_max, 0)
            kxi = 3
            kxs = 3
            
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
        for k in range(1, int(n_vao_montantes)):
            dy = espacamento_calc * inclinacao
            y += dy * aclive_declive
            iy += 1
            coord_y[iy] = round(y,2)
            
        iy += 1
        coord_y[iy] = y = ponto_f[1]
        nos_objetos = {}
        barras_objetos = []
        nos_objetos_list = []
        
        ultimo_i = int(n_vao_montantes)
        js = 4 + pre_gdl - 4 # vertical
        jss = 3 + pre_gdl - 4# horizontal

        ji = 2 + pre_gdl - 4# vertical
        jii = 1 + pre_gdl - 4# horizontal
        
        # preenchimento do dicionario de pontos (x,y)
        for i in range(1, int(1 + n_vao_montantes)):
            # graus de liberdade começam a distribuição a partir dos nós inferiores
            # graus de liberdade dos nós superiores   
            if i > 1 and (i%2 != 0 or h_viga <= 3):
                jii = js + 1
                ji = jii + 1

                jss = ji + 1
                js = jss + 1

            elif (h_viga > 3 and i%2 == 0) and i >1:
                jmm = js +1
                jm = jmm + 1

                jss = jm + 1
                js = jss + 1

            rx = 0
            ry = 0
            apoio = False
            ###############################################################
            ####################### VIGA COBERTURA ########################
            ###############################################################
            # define restrições caso pontos sejam apoios      
            # # se a iteração é na posição do primeiro, ou ultimo montante do vão
            if self.vt != 1:
                if i == 1 or i == ultimo_i:
                    # caso seja o primeiro, ou o ultimo, montante do vão
                    if i == 1:
                        if primeiro_vao:
                            # casos eja o primeiro montante do vão, e seja o primeiro dos vãos da viga
                            apoio = 'duplo'
                        elif not primeiro_vao:
                            if (coord_x[i] == cumeeira and cumeeira_alinhada) or coord_x[i] != cumeeira:
                                apoio = 'simples'

                            # elif coord_x[i] != cumeeira:
                            #     apoio = 'simples'
                    # na maioria das situações, o ultimo montante é um ponto de apoio
                    # com exceção de quando é o montante da cumeeira e esta não é alinhada com pilar
                    elif i == ultimo_i:
                        if coord_x[i] == ponto_f[0]:
                            apoio = 'simples' 

                            if not cumeeira_alinhada and coord_x[i] == cumeeira:
                                apoio = False
            else:
                if i == 1:
                    apoio = 'duplo' 
                # para a VT, cumeeira é o valor do vão
                elif coord_x[i] == cumeeira:
                    apoio = 'simples'
            
            # pontos dos banzos inferiores
            xi = coord_x[i]
            # caso a viga seja de banzo reto, define a cota a cota da coordenada como 0 (zero)
            if self.banzo_reto == 1:
                yi = round(0,2)
            else:
                yi = round(coord_y[i],2)

            if h_viga <= 3 or i%2 != 0 or i == n_vao_montantes:
                # dicionario 'global nos' - treliça inteira
                nos[i]=[xi, yi]
                # dicionario local dos nós - treliça parcial
                nos_objetos[i] = ns.Nos(xi, yi, jii, ji, rx, ry, apoio)
                nos_objetos_list.append(nos_objetos[i])
            else:
                nos_objetos[i] = ns.Nos(xi, yi, 0, 0, rx, ry, apoio)
            
            # pontos dos banzos superiores
            apoio = False
            xs = coord_x[i]
            ys = round(coord_y[i]+h_viga,2)
            
            # pontos intermediarios
            if h_viga > 3 and i%2 == 0 and i != n_vao_montantes:
                xm = xi
                if self.banzo_reto == 1:
                    ym = (ys - yi) / 2 
                    pass
                else:
                    ym = (ys - yi) / 2 + coord_y[i]

                nos[i+n_vao_montantes+1000] = [xm, ym]
                nos_objetos[i+n_vao_montantes+1000] = ns.Nos(xm, ym, jmm, jm, rx, ry, apoio)
                nos_objetos_list.append(nos_objetos[i+n_vao_montantes+1000])
            
            nos[i+n_vao_montantes] = [xs, ys]
            # usando dicionario, para usar a ordem(indice) como chave
            # verificar real necessidade de se ter LISTA e DICIONARIO
            nos_objetos[i+n_vao_montantes] = ns.Nos(xs, ys, jss, js, rx, ry, apoio)
            nos_objetos_list.append(nos_objetos[i+n_vao_montantes])

        gdl = len(nos) * 2
        gdl = len(nos_objetos) * 2

        barras_objetos = []
        
        b_id = 0
        # lançamento de banzos
        passo = 1
        if h_viga > 3:
            passo = 2

        for i in range(int(1), int(1+n_vao_montantes-1), passo):
            b_id +=1
            # banzo inferior
            n1a = nos_objetos[i]
            if i+passo > n_vao_montantes:
                n2a = nos_objetos[n_vao_montantes]
                pass
            else:
                n2a = nos_objetos[i+passo]
        
            barr = b.Barras(n1a, n2a, gdl, 'banzo-inferior', b_id, kxi, ky)
            barras_objetos.append(barr)
        
        # lançamento de banzos
        for i in range(int(1), int(1+n_vao_montantes-1)):
            # banzo superior
            k = i + int(n_vao_montantes)
            n1b = nos_objetos[k]
            n2b = nos_objetos[k + 1]

            b_id +=1            
            barr = b.Barras(n1b, n2b, gdl, 'banzo-superior', b_id, kxs, ky)
            barras_objetos.append(barr)
        
        # lançamento de montantes
        for i in range(int(1), int(n_vao_montantes)):#-1)):
            # montante(s)
            # nós inferiores
            n1a = nos_objetos[i]
            n2a = nos_objetos[i+1]
            
            # nós superiores
            k = i + int(n_vao_montantes)
            n1b = nos_objetos[k]
            n2b = nos_objetos[k + 1]

            if (h_viga > 3) and i%2 == 0:
                # nós intermediarios
                n1m = nos_objetos[k+1000]

            # desenha o primeiro montante, se for o primeiro vão da sequencia
            if i == 1 and primeiro_vao == True:
                b_id +=1
                barr = b.Barras(n1a, n1b, gdl, 'montante', b_id, kx, ky)
                barras_objetos.append(barr)

            # desenha montantes, que não sejam o primeiro 
            if i != 1: #and i < (n_vao_montantes-1):
                if (h_viga > 3) and i%2 == 0:
                    b_id +=1
                    barr = b.Barras(n1b, n1m, gdl, 'montante', b_id, kx, ky)
                    barras_objetos.append(barr)
                else:
                    b_id +=1
                    barr = b.Barras(n1a, n1b, gdl, 'montante', b_id, kx, ky)
                    barras_objetos.append(barr)

            # desenha o ultimo montante do vao
            if i == (n_vao_montantes - 1):
                b_id +=1
                barr = b.Barras(n2a, n2b, gdl, 'montante', b_id, kx, ky)
                barras_objetos.append(barr)
        
        # lançamento de diagonais
        ###########################################################################################
        # Vigas com altura maiores que 3m
        ###########################################################################################
        if h_viga > 3:
            for i in range(int(1), int(n_vao_montantes-1), 2):
                # nós inferiores
                n1a = nos_objetos[i]
                n2a = nos_objetos[i+2]
                
                # nós superiores
                k = i + int(n_vao_montantes)
                n1b = nos_objetos[k]
                n2b = nos_objetos[k+2]
                
                # # nós intermediarios
                n1m = nos_objetos[k+1000+1]

                # b_id += 1
                # barr = b.Barras(n1a, n1m, gdl, 'diagonal', b_id, kx, ky)
                # barras_objetos.append(barr)
                
                # b_id += 1
                # barr = b.Barras(n1m, n2a, gdl, 'diagonal', b_id, kx, ky)
                # barras_objetos.append(barr)

                # Orientação sempre da esquerda para direita
                # verifica se o carregamento dominante é o vento
                if vento == 1:
                    # verifica se a coordenada do ponto esta antes do 'meio' do vão
                    # No meio do vão, a rotina faz a inversão da orientação das diagonais
                    if n1a.x < meio_vao:
                        # diagonais
                        b_id += 1
                        barr = b.Barras(n1a, n1m, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)

                        b_id +=1
                        barr = b.Barras(n1m, n2b, gdl, 'diagonal', b_id, 2, ky)
                        barras_objetos.append(barr)

                        #travamento
                        b_id += 1
                        barr = b.Barras(n1m, n2a, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                    else:
                        # diagonais
                        b_id +=1
                        barr = b.Barras(n1b, n1m, gdl, 'diagonal', b_id, 2, ky)
                        barras_objetos.append(barr)
                                
                        b_id += 1
                        barr = b.Barras(n1m, n2a, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                        
                        #travamento
                        b_id += 1
                        barr = b.Barras(n1a, n1m, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                else:
                    if n1a.x < meio_vao:
                        # diagonais
                        b_id +=1
                        barr = b.Barras(n1b, n1m, gdl, 'diagonal', b_id, 2, ky)
                        barras_objetos.append(barr)

                        b_id += 1
                        barr = b.Barras(n1m, n2a, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
     
                        #travamento
                        b_id += 1
                        barr = b.Barras(n1a, n1m, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                    else:
                        # diagonais
                        b_id +=1
                        barr = b.Barras(n1m, n2b, gdl, 'diagonal', b_id, 2, ky)
                        barras_objetos.append(barr)

                        b_id += 1
                        barr = b.Barras(n1a, n1m, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)

                        #travamento
                        b_id += 1
                        barr = b.Barras(n1m, n2a, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)

            if (n_vao_montantes -1) %2 == 1:
                na = nos_objetos[n_vao_montantes-1]
                nb = nos_objetos[n_vao_montantes*2]
                b_id +=1
                barr = b.Barras(na, nb, gdl, 'diagonal', b_id, kx, ky)
                barras_objetos.append(barr)

        ###########################################################################################
        # Vigas com altura menores que 3m
        ###########################################################################################
        else:
            for i in range(int(1), int(1+n_vao_montantes-1)):
                # nós inferiores
                n1a = nos_objetos[i]
                n2a = nos_objetos[i+1]
                
                # nós superiores
                k = i + int(n_vao_montantes)
                n1b = nos_objetos[k]
                n2b = nos_objetos[k + 1]
                
                # Orientação sempre da esquerda para direita
                # verifica se o carregamento dominante é o vento
                if vento == 1:
                    # verifica se a coordenada do ponto esta antes do 'meio' do vão
                    # No meio do vão, a rotina faz a inversão da orientação das diagonais
                    if n1a.x < meio_vao:
                        b_id +=1
                        barr = b.Barras(n1a, n2b, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                    else:
                        b_id +=1
                        barr = b.Barras(n1b, n2a, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                else:
                    if n1a.x < meio_vao:
                        b_id +=1
                        barr = b.Barras(n1b, n2a, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
                    else:
                        b_id +=1
                        barr = b.Barras(n1a, n2b, gdl, 'diagonal', b_id, kx, ky)
                        barras_objetos.append(barr)
            pass

        barras_objetos = barras_objetos
        return (nos_objetos_list, barras_objetos)#, plt)
        # return (lista_nos_objetos, barras_objetos)#, plt)

  
    def propriedades(self):
        peso = 0
        peso_dobrado = 0
        peso_soldado = 0
        for barra in self.barras_objetos:
            peso += barra.get_peso()
            if barra.section.tipo == 'soldado':
                peso_soldado += barra.get_peso()
            elif barra.section.tipo == 'dobrado':
                peso_dobrado += barra.get_peso()
        
        pecas = len(self.barras_objetos)

        self.peso = peso * 1.25
        self.peso_dobrado = peso_dobrado
        self.peso_soldado = peso_soldado
        self.peso_miscelanias = peso * 0.25
        self.pecas = pecas
        self.peso_linear = self.peso / self.comprimento

