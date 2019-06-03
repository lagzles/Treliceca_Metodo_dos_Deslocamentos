import desenhar as des
import nos as ns
import barras as b
import rigidez_001 as rig
##import matplotlib.pyplot as plt

espacamento_padrao = 2.0

coord_y = {}
coord_x = {}
nos = {}
x = 0
y = 0

e = 300
a = 400


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
    inclinacao = 1
    cumeeira = list_cumeeira[0]
    
    if len(ponto_i) == 2:
        y = round(ponto_i[1],2)
        if ponto_i[1]< ponto_f[1]:
            inclinacao = 1
        else:
            inclinacao = -1
    elif len(ponto_i) == 3:
        y = round(ponto_i[2],2)
        zy = round(ponto_i[1],2)
        if ponto_i[2]< ponto_f[2]:
            inclinacao = 1
        else:
            inclinacao = -1
    
    espacamento_calc = 2.1
    vaof += ponto_f[0]
    x = round(ponto_i[0],2)

    n_vao_montantes = round(vao / espacamento_padrao,0)
    while espacamento_calc > 2:
        espacamento_calc = vao / n_vao_montantes
        n_vao_montantes +=1

    coord_x[ix] = x
    while x < vaof:
        x += espacamento_calc
        ix += 1
        coord_x[ix] = round(x,2)
    
    coord_y[iy] = y    
    for k in range(int(n_v_montantes_i), int(n_v_montantes_i + n_vao_montantes - 1)):
        dy = espacamento_calc*3/100
        y += dy * inclinacao
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

        # defini restrições caso pontos sejam apoios
        if i == 1 or i == int(n_v_montantes_i + n_vao_montantes - 1):
            if i == 1 and primeiro_vao == True:
                rx = "x"                
            else:
                rx = 0

            if coord_x[i] != cumeeira or list_cumeeira[1] == True:
                ry = "x"
            elif (ponto_f[0] == cumeeira or ponto_i[0] == cumeeira) and list_cumeeira[1] == True:
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
    gdl = len(nos)*2
    
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
        
        barr = b.Barras(n1a, n2a, e, a, gdl, 'banzo')
        barras_objetos.append(barr)
                
        # banzo superior
        k = i + int(n_vao_montantes)
        n1b = nos_objetos[k]
        n2b = nos_objetos[k+1]
        
        barr = b.Barras(n1b, n2b, e, a, gdl, 'banzo')
        barras_objetos.append(barr)

        # montante(s)
        # desenha o primeiro montante, se for o primeiro vão da sequencia
        if i == 1 and primeiro_vao == True:
            barr = b.Barras(n1a, n1b, e, a, gdl, 'montante')
            barras_objetos.append(barr)

        # desenha montantes, que não sejam o primeiro 
        if i != 1:
            barr = b.Barras(n1a, n1b, e, a, gdl, 'montante')
            barras_objetos.append(barr)

        # desenha o ultimo montante do vao
        if i == (n_vao_montantes-1):
            barr = b.Barras(n2a, n2b, e, a, gdl, 'montante')
            barras_objetos.append(barr)
        # Orientação sempre da esquerda para direita
        if vento == 1:
            if n1a.x <= meio_vao:
                barr = b.Barras(n1a, n2b, e, a, gdl, 'diagonal')
                barras_objetos.append(barr)
            else:
                barr = b.Barras(n1b, n2a, e, a, gdl, 'diagonal')
                barras_objetos.append(barr)
        else:
            if n1a.x <= meio_vao:
                barr = b.Barras(n1b, n2a, e, a, gdl, 'diagonal')
                barras_objetos.append(barr)
            else:
                barr = b.Barras(n1a, n2b, e, a, gdl, 'diagonal')
                barras_objetos.append(barr)
                
    return (nos_objetos_list, barras_objetos)#, plt)


def desenhar_trelica(dwg, h_viga, ponto_i, ponto_f, vento, primeiro_vao, pre_gdl, cumeeira):

    retorno = pontos_treliceca( h_viga, ponto_i, ponto_f, vento, primeiro_vao, pre_gdl, cumeeira)
##    subplt = plt.subplot(111)

    if len(ponto_i) == 2:
        y = round(ponto_i[1],2)
        if ponto_i[1]< ponto_f[1]:
            inclinacao = 1
        else:
            inclinacao = -1
    elif len(ponto_i) == 3:
        y = round(ponto_i[2],2)
        zy = round(ponto_i[1],2)
        if ponto_i[2]< ponto_f[2]:
            inclinacao = 1
        else:
            inclinacao = -1
    

    n_vao_montantes = retorno[0]
    n_v_montantes_i = 1
    meio_vao = retorno[1]
    
    nos = retorno[3]
    
    # lançamento de banzos
    for i in range(int(n_v_montantes_i), int(n_v_montantes_i+n_vao_montantes-1)):
        x1a = nos[i][0]
        y1a = nos[i][1]
        
        x2a = nos[i+1][0]
        y2a = nos[i+1][1]

        if len(ponto_i) == 2:
            des.desenhar_banzos(dwg,[x1a, y1a], [x2a, y2a])
        else:
            des.desenhar_banzos(dwg,[x1a, zy, y1a], [x2a, zy, y2a])
        # banzo superior
        k = i + int(n_vao_montantes)
        x1b = nos[k][0]
        y1b = nos[k][1]
        
        x2b = nos[k+1][0]        
        y2b = nos[k+1][1]
        
        if len(ponto_i) == 2:
            des.desenhar_banzos(dwg, [x1b, y1b], [x2b, y2b])
        else:
            des.desenhar_banzos(dwg, [x1b, zy, y1b], [x2b, zy, y2b])

        # montante(s)
        # desenha o primeiro montante, se for o primeiro vão da sequencia
        if i == 1 and primeiro_vao == True:
            if len(ponto_i) == 2:
                des.desenhar_montantes(dwg, [x1a, y1a], [x1b, y1b])
            else:
                des.desenhar_montantes(dwg, [x1a, zy, y1a], [x1b, zy, y1b])

        # desenha montantes, que não sejam o primeiro 
        if i != 1:
            if len(ponto_i) == 2:
                des.desenhar_montantes(dwg, [x1a, y1a], [x1b, y1b])
            else:
                des.desenhar_montantes(dwg, [x1a, zy, y1a], [x1b, zy, y1b])

        # desenha o ultimo montante do vao
        if i == (n_vao_montantes-1):
            if len(ponto_i) == 2:
                des.desenhar_montantes(dwg, [x2a, y2a], [x2b, y2b])
            else:
                des.desenhar_montantes(dwg, [x2a, zy, y2a], [x2b, zy, y2b])

        if vento == 1:
            if x1a <= meio_vao:
                if len(ponto_i) == 2:
                    des.desenhar_diagonais(dwg, [x1a, y1a], [x2b, y2b])
                else:
                    des.desenhar_diagonais(dwg, [x1a, zy, y1a], [x2b, zy, y2b])
            else:
                if len(ponto_i) == 2:
                    des.desenhar_diagonais(dwg, [x2a, y2a], [x1b, y1b])
                else:
                    des.desenhar_diagonais(dwg, [x2a, zy, y2a], [x1b, zy, y1b])
        else:
            if x1a <= meio_vao:
                if len(ponto_i) == 2:
                    des.desenhar_diagonais(dwg, [x2a, y2a], [x1b, y1b])
                else:
                    des.desenhar_diagonais(dwg, [x2a, zy, y2a], [x1b, zy, y1b])                
            else:
                if len(ponto_i) == 2:
                    des.desenhar_diagonais(dwg, [x1a, y1a], [x2b, y2b])
                else:
                    des.desenhar_diagonais(dwg, [x1a, zy, y1a], [x2b, zy, y2b])



##########################################################
##########################################################
