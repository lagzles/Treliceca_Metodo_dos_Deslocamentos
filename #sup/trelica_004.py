import desenhar as des
import nos as ns
import barras_001 as b
import rigidez_002 as rig
##import matplotlib.pyplot as plt

espacamento_padrao = 2.0

coord_y = {}
coord_x = {}
nos = {}
x = 0
y = 0

e = 300
a = 400

class Trelica(object):
    def __init__(self, h, pontos_vao, cumeeira, cumeeira_alinhada_com_pilar, vento):
        self.h_viga = h
        self.cumeeira = cumeeira
        self.cumeeira_alinhada = cumeeira_alinhada_com_pilar
        self.vento = vento


class TrelicaParcial(object):
    def __init__(self, trelica, xi, xf, primeiro_vao, pre_gdl):
        self.h_viga = trelica.h_viga
        self.xi = xi
        self.xf = xf        
        self.vento = trelica.vento
        self.primeiro_vao = primeiro_vao
        self.pre_gdl = pre_gdl
        self.cumeeira = trelica.cumeeira
        self.cumeeira_alinhada = trelica.cumeeira_alinhada
        

def pontos_treliceca( h_viga, ponto_i, ponto_f,
                      vento, primeiro_vao, pre_gdl,
                      list_cumeeira):
    vao = abs(ponto_f[0] - ponto_i[0])
    meio_vao = round(vao/2 + ponto_i[0],2)
    n_v_montantes_i = 1
    vaof = 0
    ix = 1
    iy = 1
    dy = 0
    inclinacao = 3.0 / 100.0
    aclive_declive = 1
    cumeeira = list_cumeeira[0]

    # se estrutura é 2D
    if len(ponto_i) == 2:
        y = round(ponto_i[1],2)
        
        if ponto_i[1]< ponto_f[1]:
            aclive_declive = 1
        else:
            aclive_declive = -1
    
    espacamento_calc = 2.1
    vaof += ponto_f[0]
    x = round(ponto_i[0],2)

    n_vao_montantes = round(vao / espacamento_padrao,0)

    # calcula distancia entre montantes
    while espacamento_calc > 2:
        espacamento_calc = vao / n_vao_montantes
        n_vao_montantes +=1

    coord_x[ix] = x

    # acrescentando banzos, até o valor ser menor que o ponto final
    # coordenadas x, para cada nó inicial e final das barras de banzo
    while x < vaof:
        x += espacamento_calc
        ix += 1        
        coord_x[ix] = round(x,2)
##        print('x=',x,'  ix=', ix)
    
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
            
            # caso seja 1 vão apenas, alinhado com cumeeira
            if i == ultimo_i: # caso ultimo montante
                if ponto_f[0] == cumeeira or ponto_i[0] == cumeeira:
                    # caso ponto final seja cota da cumeeira
                    if list_cumeeira[1] == True:
                        if coord_x[i] == cumeeira:
                            ry = "x"
            
            if primeiro_vao == False:
                if i == ultimo_i: # caso ultimo montante
                    #se coordenada for cumeeira e cumeeira alinhada com pilar
                    if list_cumeeira[1] == True and coord_x[i] == cumeeira and coord_x[i] == ponto_f[0]:
                        ry = "x"
                    # se coordenada final for equivalente ao ponto final do vão
                    elif coord_x[i] == ponto_f[0]:
                        ry = "x"
                
        # pontos dos banzos inferiores
        xi = coord_x[i]
        yi = round(coord_y[i],2)

        nos[i]=[xi, yi]    
        nos_objetos[i] = ns.Nos(xi, yi, jii, ji, rx, ry)
        nos_objetos_list.append(nos_objetos[i])
        
        # pontos dos banzos superiores
        rx = 0
        # setado valor inicial, para identificação posterior
        ry = -10
        
        xf = xi
        yf = round(coord_y[i]+h_viga,2)

        nos[i+n_vao_montantes]=[xf, yf]
        nos_objetos[i+n_vao_montantes] = ns.Nos(xf, yf, jss, js, rx, ry)
        nos_objetos_list.append(nos_objetos[i+n_vao_montantes])

    j = 0
    gdl = len(nos) * 2
    
    return (n_vao_montantes, meio_vao, gdl, nos, nos_objetos, nos_objetos_list)



# def rigidez_trelica(dwg, h_viga, ponto_i, ponto_f, vento, primeiro_vao, pre_gdl, cumeeira):
def rigidez_trelica(h_viga, ponto_i, ponto_f, vento, primeiro_vao, pre_gdl, cumeeira):

    retorno = pontos_treliceca(h_viga, ponto_i, ponto_f, vento, primeiro_vao, pre_gdl, cumeeira)

    n_vao_montantes = retorno[0]
    meio_vao = retorno[1]
    gdl = retorno[2]
    nos_objetos = retorno[4]
    nos_objetos_list = retorno[5]
    barras_objetos = []
    
    # lançamento de banzos
##    m = 0
    for i in range(int(1), int(1+n_vao_montantes-1)):
        # banzo inferior
        n1a = nos_objetos[i]
        n2a = nos_objetos[i+1]
        
        barr = b.Barras(n1a, n2a, gdl, 'banzo-inferior')
        barras_objetos.append(barr)
                
        # banzo superior
        k = i + int(n_vao_montantes)
        n1b = nos_objetos[k]
        n2b = nos_objetos[k+1]
        
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
        if i == (n_vao_montantes-1):
            barr = b.Barras(n2a, n2b, gdl, 'montante')
            barras_objetos.append(barr)
        # Orientação sempre da esquerda para direita
        if vento == 1:
            if n1a.x <= meio_vao:
                barr = b.Barras(n1a, n2b, gdl, 'diagonal')
                barras_objetos.append(barr)
            else:
                barr = b.Barras(n1b, n2a, gdl, 'diagonal')
                barras_objetos.append(barr)
        else:
            if n1a.x <= meio_vao:
                barr = b.Barras(n1b, n2a, gdl, 'diagonal')
                barras_objetos.append(barr)
            else:
                barr = b.Barras(n1a, n2b, gdl, 'diagonal')
                barras_objetos.append(barr)
                
    return (nos_objetos_list, barras_objetos)#, plt)

