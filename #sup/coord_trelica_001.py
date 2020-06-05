import desenhar as des
import nos as ns

espacamento_padrao = 2.0

coord_y = {}
coord_x = {}
nos = {}
x = 0
y = 0

ponto_i = (20, 30, 12)
ponto_f = (42, 30, 12.66)

def treliceca(dwg, h_viga, ponto_i, ponto_f, vento, primeiro_vao):
    vao = abs(ponto_f[0] - ponto_i[0])
    meio_vao = round(vao/2 + ponto_i[0],2)
    n_v_montantes_i = 1
    vaof = 0
    ix = 1
    iy = 1
    dy = 0
    inclinacao = 1
##    print('ponto_i',ponto_i)
##    print('ponto_f',ponto_f)
    
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

    for i in range(int(n_v_montantes_i), int(n_v_montantes_i + n_vao_montantes)):
        nos[i]=[coord_x[i], round(coord_y[i],2)]
        nos[i+n_vao_montantes]=[coord_x[i], round(coord_y[i]+h_viga,2)]

##    print(len(nos))
    for i in range(1,len(nos)-1):
##        print(i)
        ni = nos[i]
        for k in range(1,len(nos)-1):
            nf = nos[k]
##            if ni[0] == nf[0]:
    j = 0
    gdl = len(nos)
    # lançamento de banzos
    for i in range(int(n_v_montantes_i), int(n_v_montantes_i+n_vao_montantes-1)):
        # banzo inferior
        x1a = nos[i][0]
        y1a = nos[i][1]
        
        j += 1
        jj = j + 1
        n1 = ns.Nos(x1a, y1a, j, jj, 0, 0)
        j = jj
        
        x2a = nos[i+1][0]
        y2a = nos[i+1][1]

        if len(ponto_i) == 2:
            des.desenhar_banzos(dwg,[x1a,y1a], [x2a, y2a])
        else:
            des.desenhar_banzos(dwg,[x1a, zy,y1a], [x2a, zy, y2a])
        # banzo superior
        k = i + int(n_vao_montantes)
        x1b = nos[k][0]
        y1b = nos[k][1]

        j += 1
        jj = j + 1
        n2 = ns.Nos(x1b, y1b, j, jj, 0, -10)
        j = jj
        
        x2b = nos[k+1][0]        
        y2b = nos[k+1][1]
        
        if len(ponto_i) == 2:
            des.desenhar_banzos(dwg, [x1b,y1b], [x2b, y2b])
        else:
            des.desenhar_banzos(dwg, [x1b, zy, y1b], [x2b, zy, y2b])

        # montante(s)
        # desenha o primeiro montante, se for o primeiro vão da sequencia
        if i == 1 and primeiro_vao == True:
##            print('primeiro', i, primeiro_vao)
            if len(ponto_i) == 2:
                des.desenhar_montantes(dwg, [x1a, y1a], [x1b, y1b])
            else:
                des.desenhar_montantes(dwg, [x1a, zy, y1a], [x1b, zy, y1b])

        # desenha montantes, que não sejam o primeiro 
        if i != 1:
##            print(i)
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
##########################################################
##########################################################
##########################################################


def desenhar_trelica(lista_nos, lista_montantes, lista_meios_de_vao, vento, dwg):
    print(len(lista_nos), len(lista_montantes))

    for j in range(0,len(lista_nos)):
        nos = lista_nos[j][0]
        print(nos)
        for i in range(1, int(lista_montantes[j])):
            # banzo inferior            
            x1a = nos[i][0]
            x2a = nos[i+1][0]
            y1a = nos[i][1]
            y2a = nos[i+1][1]

            des.desenhar_banzos(dwg,[x1a,y1a], [x2a, y2a])
            # banzo superior
            k = i + int(lista_montantes[j])
            x1b = nos[k][0]
            x2b = nos[k+1][0]
            y1b = nos[k][1]
            y2b = nos[k+1][1]

            des.desenhar_banzos(dwg, [x1b,y1b], [x2b, y2b])

            if vento == 1:
                if x1a <= lista_meios_de_vao[j]:
                    des.desenhar_diagonais(dwg, [x1a, y1a], [x2b, y2b])
                else:
                    des.desenhar_diagonais(dwg, [x2a, y2a], [x1b, y1b])
            else:
                if x1a <= meio_vao:
                    des.desenhar_diagonais(dwg, [x2a, y2a], [x1b, y1b])
                else:
                    des.desenhar_diagonais(dwg, [x1a, y1a], [x2b, y2b])
                    

    
##    print(len(nos))
######    for i in range(1,len(nos)-1):
########        print(i)
######        ni = nos[i]
######        for k in range(1,len(nos)-1):
######            nf = nos[k]
########            if ni[0] == nf[0]:
######                
######    # lançamento de banzos
######    for i in range(int(n_v_montantes_i), int(n_v_montantes_i+n_vao_montantes-1)):
######        # banzo inferior
######        x1a = nos[i][0]
######        x2a = nos[i+1][0]
######        y1a = nos[i][1]
######        y2a = nos[i+1][1]
######
######        if len(ponto_i) == 2:
######            des.desenhar_banzos(dwg,[x1a,y1a], [x2a, y2a])
######        else:
######            des.desenhar_banzos(dwg,[x1a, zy,y1a], [x2a, zy, y2a])
######        # banzo superior
######        k = i + int(n_vao_montantes)
######        x1b = nos[k][0]
######        x2b = nos[k+1][0]
######        y1b = nos[k][1]
######        y2b = nos[k+1][1]
######        if len(ponto_i) == 2:
######            des.desenhar_banzos(dwg, [x1b,y1b], [x2b, y2b])
######        else:
######            des.desenhar_banzos(dwg, [x1b, zy, y1b], [x2b, zy, y2b])
########        # montante(s)
########        if len(ponto_i) == 2:
########            des.desenhar_montantes(dwg, [x1a, y1a], [x1b, y1b])
########        else:
########            des.desenhar_montantes(dwg, [x1a, zy, y1a], [x1b, zy, y1b])
######            
######        if i == (n_vao_montantes-1):
######            if len(ponto_i) == 2:
######                des.desenhar_montantes(dwg, [x2a, y2a], [x2b, y2b])
######            else:
######                des.desenhar_montantes(dwg, [x2a, zy, y2a], [x2b, zy, y2b])
######                
######        if vento == 1:
######            if x1a <= meio_vao:
######                if len(ponto_i) == 2:
######                    des.desenhar_diagonais(dwg, [x1a, y1a], [x2b, y2b])
######                else:
######                    des.desenhar_diagonais(dwg, [x1a, zy, y1a], [x2b, zy, y2b])
######            else:
######                if len(ponto_i) == 2:
######                    des.desenhar_diagonais(dwg, [x2a, y2a], [x1b, y1b])
######                else:
######                    des.desenhar_diagonais(dwg, [x2a, zy, y2a], [x1b, zy, y1b])
######        else:
######            if x1a <= meio_vao:
######                if len(ponto_i) == 2:
######                    des.desenhar_diagonais(dwg, [x2a, y2a], [x1b, y1b])
######                else:
######                    des.desenhar_diagonais(dwg, [x2a, zy, y2a], [x1b, zy, y1b])                
######            else:
######                if len(ponto_i) == 2:
######                    des.desenhar_diagonais(dwg, [x1a, y1a], [x2b, y2b])
######                else:
######                    des.desenhar_diagonais(dwg, [x1a, zy, y1a], [x2b, zy, y2b])
######                
######
