import barras_001 as b
import nos
import numpy as np


e = 300
a = 400


def analise_matriz_carregamentos(noss, barras, carregamentos):
    gdl = len(noss) * 2
    liv = []
    ap = []
    fa = []
    print(carregamentos)

    for carregamento in carregamentos:
        liv = []
        ap = []
        fa = []
        k = np.zeros((gdl,gdl))
##        jj = 0
        
        for b in barras:
            tipo_barra = b.tipo.split("-")[-1]
            if tipo_barra == 'superior':
                dx = abs(b.nf.x - b.ni.x)
                b.ni.fy = carregamento * dx
                b.nf.fy = carregamento * dx
               
        
        for no in noss:
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

        ##k = None
        ##k = b1.kci + b2.kci + b3.kci + b4.kci + b5.kci + b6.kci
        for barra in barras:
            barra.set_gdl(gdl)
            k = k + barra.kci

        # para pegar deslocamentos nodais
        ka = np.delete(np.delete(k, ap, axis=0), ap, axis=1)

        # para pegar as reações
        kb = np.delete(np.delete(k, liv, axis=0), ap,axis=1)

        # deslocamentos nodais
        ua = np.dot( np.linalg.inv(ka),fa)

        # reações nos apoios
        fb = np.dot(kb, ua)
        
        print('================================================')
        print('fb', 'Reações nos Apoios')
        print(np.round(fb, decimals=2))

        for barra in barras:
            barra.esforcos_nodais(ua, gdl, liv)

    return barras


####def analise_matriz(noss, barras):
####    gdl = len(noss) * 2
####    liv = []
####    ap = []
####    fa = []
####    
####    for no in noss:
####        if no.fx != 'x':
####            liv = liv + [no.gx - 1]
####            fa = fa + [no.fx]
####        else:
####            ap = ap + [no.gx - 1]
####        if no.fy != 'x':
####            liv = liv + [no.gy - 1]
####            fa = fa + [no.fy]
####        else:
####            ap = ap + [no.gy - 1]
####
####    k = np.zeros((gdl,gdl))
####    
####    ##k = None
####    ##k = b1.kci + b2.kci + b3.kci + b4.kci + b5.kci + b6.kci
####    for barra in barras:
####        barra.set_gdl(gdl)
####        k = k + barra.kci
####
####    # para pegar deslocamentos nodais
####    ka = np.delete(np.delete(k, ap, axis=0), ap, axis=1)
####
####    # para pegar as reações
####    kb = np.delete(np.delete(k, liv, axis=0), ap,axis=1)
####
####    # deslocamentos nodais
####    ua = np.dot( np.linalg.inv(ka),fa)
####
####    # reações nos apoios
####    fb = np.dot(kb, ua)
####
####    print('================================================')
####    print('fb', 'Reações nos Apoios')
####    print(np.round(fb, decimals=2))
####
####    c = 0
####    for barra in barras:
####        c += 1
####        barra.esforcos_nodais(ua, gdl, liv)
####        esf = ''
####        if barra.fbi[0] > 0:
####            esf = 'Compressão'
####        else:
####            esf = 'Tração'



