import barras_001 as b
import nos
import numpy as np


e = 300
a = 400


def analise_matriz_carregamentos(trelica):
    noss = trelica.nos_objetos
    barras = trelica.barras_objetos
    gdl = len(noss) * 2
    liv = []
    ap = []
    fa = []
    carregamentos = trelica.carregamentos
    print('carregamentos \n',carregamentos)
    
    liv = []
    ap = []
    fa = []
    k = np.zeros((gdl,gdl))
    
    
    
    ##k = None
    ##k = b1.kci + b2.kci + b3.kci + b4.kci + b5.kci + b6.kci
    liv = trelica.liv
    ap = trelica.ap
    fa_grav = trelica.fa_grav
    fa_cv = trelica.fa_cv
    k = trelica.k
    print("\n linha 34 - rigidez - determinante K")
    print(np.linalg.det(k))
    
    print("\n linha 32 - rigidez - fa_grav")
    print(fa_grav)


    # para pegar deslocamentos nodais
    ka = np.delete(np.delete(k, ap, axis=0), ap, axis=1)

    # para pegar as reações
    kb = np.delete(np.delete(k, liv, axis=0), ap,axis=1)

    # deslocamentos nodais
    ua_grav = np.dot( np.linalg.inv(ka),fa_grav)
    trelica.ua_grav = ua_grav
    
    ua_cv = np.dot( np.linalg.inv(ka),fa_cv)
    trelica.ua_cv = ua_cv

    # reações nos apoios
    fb_grav = np.dot(kb, ua_grav)
    fb_cv = np.dot(kb, ua_cv)
    
    print('================================================')
    print('fb', 'Reações nos Apoios - Gravitacionais')
    print(np.round(fb_grav, decimals=2))
    print('fb', 'Reações nos Apoios - Vento')
    print(np.round(fb_cv, decimals=2))

    for barra in barras:
        barra.esforcos_nodais([ua_cv, ua_grav], gdl, liv)

    return barras



