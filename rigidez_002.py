import barras_002 as b
import nos_001 as nos
import numpy as np
from tkinter import messagebox


def analise_matriz_carregamentos(trelica):
    noss = trelica.nos_objetos
    barras = trelica.barras_objetos
    gdl = len(noss) * 2

    liv = []
    ap = []
    k = np.zeros((gdl,gdl))
    
    ##k = None
    ##k = b1.kci + b2.kci + b3.kci + b4.kci + b5.kci + b6.kci
    liv = trelica.liv
    ap = trelica.ap
    fa_grav = trelica.fa_grav
    fa_cv = trelica.fa_cv
    k = trelica.k

    fa_cv = np.delete(fa_cv, ap, axis=0)
    fa_grav = np.delete(fa_grav, ap, axis=0)

    # para pegar deslocamentos nodais
    ka = np.delete(np.delete(k, ap, axis=0), ap, axis=1)
    # para pegar as reações
    kb = np.delete(np.delete(k, liv, axis=0), ap, axis=1)

    # deslocamentos nodais
    try:
        ka_inv = np.linalg.inv(ka)
    except Exception as e:
        print('det(k)=0 (zero)', e)
        messagebox.showinfo("DANGER DANGER", """Devido limitações intelectuais, o programa não realizou analise corretamente da viga.
É recomendado que altere a geometria. 
Sugestão: aumentar o(s) vão(s), ou arredondar os valores.
Em caso de dúvida:
    - disque 0800-socorro-deus,
    - ramal 611 3356
    - email: leandro.gonzales@medabil.com.br.
    """)
        ka_inv = ka

    ua_grav = ka_inv.dot((fa_grav))
    ua_cv = ka_inv.dot(fa_cv)

    trelica.ua_grav = ua_grav
    trelica.ua_cv = ua_cv
    # reações nos apoios
    fb_grav = np.dot(kb, ua_grav)
    fb_cv = np.dot(kb, ua_cv)
    
    print('='*45)
    print('fb', 'Reações nos Apoios - Gravitacionais')
    print(np.round(fb_grav, decimals=2))
    trelica.reacoes_grav = np.round(fb_grav, decimals=2)
    print('='*45)
    print('fb', 'Reações nos Apoios - Vento')
    print(np.round(fb_cv, decimals=2))
    trelica.reacoes_cv = np.round(fb_cv, decimals=2)
    print('='*45)
    print("...")

    for barra in barras:
        barra.esforcos_nodais([ua_cv, ua_grav], gdl, liv)

    return barras

