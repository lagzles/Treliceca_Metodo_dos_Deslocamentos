import desenhar as des
import trelica_010 as trel5


def geometrizar(file, n_vaos, lista_vaos, cumeeira, vao_secundaria, altura_viga, vento, vt, banzo_reto):
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

    trelica = trel5.Trelica(h_viga, pontos_viga, cumeeira, cumeeira_alinhada_com_pilar, vento, vt, banzo_reto)
    
    return trelica

    
