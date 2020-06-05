from dxfwrite import DXFEngine as dxf
import desenhar as des
##import trelica_002 as coord
import trelica_003 as trel
import rigidez_001 as rig

c_esq = 1
c_dir = 1
c_cob_e = 1
c_cob_d = 1


def analisar(file, n_vaos, lista_vaos, cumeeira, pe_direito, tipo, trelica,
             n_porticos, vao_secundaria, vento):
##    dwg = dxf.drawing('3d.dxf')
    if file != "":
        dwg = dxf.drawing(file)

    inc = 3
    largura_oitao = 0
    #tipo é 2D ou 3D

    h_cumeeira = 0
    h_cumeeira = pe_direito + (cumeeira * inc / 100.)
    
    pontos_base = []
    pontos_topo = []
    pontos_viga = []

    cumeeira_alinhada_com_pilar = False

####    # pontos 1 e 2, do primeiro pilar
####    pontos_base.append([0, 0])
####    pontos_topo.append([0, pe_direito])
####    pontos_viga.append([0, pe_direito])
####
####
####
####    for vao in lista_vaos:
####        largura_oitao += vao
####        if largura_oitao < cumeeira:
####            cota_trecho = pe_direito + largura_oitao * 3 / 100.
####            pontos_topo.append([largura_oitao, cota_trecho])
####            pontos_base.append([largura_oitao, 0])
####                    
####        elif largura_oitao == cumeeira:
####            cumeeira_alinhada_com_pilar = True            
####            cota_trecho = h_cumeeira
####            pontos_topo.append([largura_oitao, cota_trecho])
####            pontos_base.append([largura_oitao, 0])
####            
####        elif  largura_oitao > cumeeira:
####            cota_trecho = h_cumeeira - (largura_oitao - cumeeira) * 3 / 100.
####            pontos_topo.append([largura_oitao, cota_trecho])
####            pontos_base.append([largura_oitao, 0])
####
####        if largura_oitao > cumeeira and (largura_oitao-vao) < cumeeira:
####            pontos_viga.append([cumeeira, h_cumeeira])
####            
####        pontos_viga.append([largura_oitao, cota_trecho])
####
####    
####    if cumeeira_alinhada_com_pilar == False and cumeeira != 0:
####        ponto_cumeeira = [cumeeira, h_cumeeira]
####
####    # criar pilares
####    if file != "": 
####        for p in range(n_porticos):
####            #if tipo == 1:
####            if len(pontos_topo) == len(pontos_base):
####                for i in range(len(pontos_base)):
####                    if tipo != 1: # se for desenho 3D
####                        pontos_base[i][1] = p * vao_secundaria
####                        pontos_topo[i][1] = p * vao_secundaria
####                        des.desenhar_montantes(dwg, pontos_base[i], pontos_topo[i])
####                    else:  # se for desenho 2D
####    ##                    print(pontos_base[i])
####                        xi = [pontos_base[i][0], pontos_base[i][1]]
####                        xf = [pontos_topo[i][0], pontos_topo[i][1]]
####                        des.desenhar_montantes(dwg, xi, xf)

#####   criar vigas
####    primeiro_vao = True
####    nos_objetos = []
####    barras_objetos = []
####    pre_gdl = 4
####    
####    for p in range(n_porticos):
####        for i in range(len(pontos_viga)-1):
####            print('desenhando / analisando')
####            if tipo != 1: # se for desenho 3D
####                pontos_viga[i][1] = p * vao_secundaria
####                pontos_viga[i+1][1] = p * vao_secundaria
####                if trelica == 1:
####                    # altura viga treliçada
####                    h_viga = round(max(lista_vaos)/15,2)
####                    #coord.trelica(dwg, h_viga, pontos_viga[i], pontos_viga[i+1], vento, primeiro_vao, pre_gdl, cumeeira)
####                    trel.desenhar_trelica(dwg, h_viga, pontos_viga[i], pontos_viga[i+1], vento, primeiro_vao, pre_gdl, cumeeira)
####                    primeiro_vao = False
####                else:
####                    des.desenhar_linhas(dwg, pontos_viga[i], pontos_viga[i+1])
####            else: # se for desenho 2D
####                xi = [pontos_viga[i][0], pontos_viga[i][1]]
####                xf = [pontos_viga[i+1][0], pontos_viga[i+1][1]]
####                if trelica == 1:
####                    # altura viga treliçada
####                    h_viga = round(max(lista_vaos)/15,2)
####                    if file != "":
####                        trel.desenhar_trelica(dwg, h_viga, xi, xf, vento, primeiro_vao, pre_gdl, cumeeira)
####                        print("desenhado")
####                    if file == "":
####                        retorno = trel.rigidez_trelica( h_viga, xi, xf, vento, primeiro_vao, pre_gdl, cumeeira)
####                        print("rigidez")
####
####                    indice_inicial = 0
####                    if primeiro_vao == False:
####                        indice_inicial = 2
####
####                    for nn in range(indice_inicial, len(retorno[0])):
####                        n = retorno[0][nn]
####                        nos_objetos.append(n)
####                    pre_gdl = nos_objetos[-1].gy
####
####                    for b in retorno[1]:
####                        barras_objetos.append(b)
####
####                    primeiro_vao = False
####                else:                
####                    des.desenhar_linhas(dwg, xi, xf)
####
######        print(nos_objetos)
####        print('portico ', p)
####        if file == "":
####            rig.analise_matriz(nos_objetos, barras_objetos)
####            print('analise')


    ########################################

    # pontos 1 e 2, do primeiro pilar
    pontos_base.append([0,0, 0])
    pontos_topo.append([0, 0, pe_direito])
    pontos_viga.append([0, 0, pe_direito])

    #############################################
    
    for vao in lista_vaos:
        largura_oitao += vao
        if largura_oitao < cumeeira:
            cota_trecho = pe_direito + largura_oitao * 3 / 100.
            pontos_topo.append([largura_oitao, 0, cota_trecho])
            pontos_base.append([largura_oitao, 0.0, 0])
                    
        elif largura_oitao == cumeeira:
            cumeeira_alinhada_com_pilar = True            
            cota_trecho = h_cumeeira
            pontos_topo.append([largura_oitao, 0, cota_trecho])
            pontos_base.append([largura_oitao, 0.0,  0])
            
        elif  largura_oitao > cumeeira:
            cota_trecho = h_cumeeira - (largura_oitao - cumeeira) * 3 / 100.
            pontos_topo.append([largura_oitao, 0, cota_trecho])
            pontos_base.append([largura_oitao, 0.0,  0])

        if largura_oitao > cumeeira and (largura_oitao-vao) < cumeeira:
            pontos_viga.append([cumeeira, 0, h_cumeeira])
            
        pontos_viga.append([largura_oitao, 0, cota_trecho])

    
    if cumeeira_alinhada_com_pilar == False and cumeeira != 0:
        ponto_cumeeira = [cumeeira, 0, h_cumeeira]

    # criar pilares
    if file != "":
        for p in range(n_porticos):
            #if tipo == 1:
            if len(pontos_topo) == len(pontos_base):
                for i in range(len(pontos_base)):
                    if tipo != 1: # se for desenho 3D
                        pontos_base[i][1] = p * vao_secundaria
                        pontos_topo[i][1] = p * vao_secundaria
                        des.desenhar_montantes(dwg, pontos_base[i], pontos_topo[i])
                    else:  # se for desenho 2D
                        xi = [pontos_base[i][0], pontos_base[i][2]]
                        xf = [pontos_topo[i][0], pontos_topo[i][2]]
                        des.desenhar_montantes(dwg, xi, xf)




    # criar vigas
    primeiro_vao = True
    nos_objetos = []
    barras_objetos = []
    pre_gdl = 4
    
    if file == "":
        p = 1
    
    for p in range(n_porticos):
        for i in range(len(pontos_viga)-1):
            print('desenhando / analisando')
            if tipo != 1: # se for desenho 3D
                pontos_viga[i][1] = p * vao_secundaria
                pontos_viga[i+1][1] = p * vao_secundaria
                if trelica == 1:
                    # altura viga treliçada
                    h_viga = round(max(lista_vaos)/15,2)
                    #coord.trelica(dwg, h_viga, pontos_viga[i], pontos_viga[i+1], vento, primeiro_vao, pre_gdl, cumeeira)
                    trel.desenhar_trelica(dwg, h_viga, pontos_viga[i], pontos_viga[i+1], vento, primeiro_vao, pre_gdl, cumeeira)
                    primeiro_vao = False
                else:
                    des.desenhar_linhas(dwg, pontos_viga[i], pontos_viga[i+1])
            else: # se for desenho 2D
                xi = [pontos_viga[i][0], pontos_viga[i][2]]
                xf = [pontos_viga[i+1][0], pontos_viga[i+1][2]]
                if trelica == 1:
                    # altura viga treliçada
                    h_viga = round(max(lista_vaos)/15,2)
                    if file != "":
                        trel.desenhar_trelica(dwg, h_viga, xi, xf, vento, primeiro_vao, pre_gdl, cumeeira)
                        print("desenhado")
                    if file == "":
                        retorno = trel.rigidez_trelica( h_viga, xi, xf, vento, primeiro_vao, pre_gdl, cumeeira)
                        print("rigidez")

                        indice_inicial = 0
                        if primeiro_vao == False:
                            indice_inicial = 2

                        for nn in range(indice_inicial, len(retorno[0])):
                            n = retorno[0][nn]
                            nos_objetos.append(n)
                        pre_gdl = nos_objetos[-1].gy

                        for b in retorno[1]:
                            barras_objetos.append(b)

                    primeiro_vao = False
                else:                
                    des.desenhar_linhas(dwg, xi, xf)

##        print(nos_objetos)
        print('portico ', p)
        if file == "":
            rig.analise_matriz(nos_objetos, barras_objetos)
            print('analise')
    
    print('fim')
    return barras_objetos

    
