import barras as b
import nos
import numpy as np


e = 300
a = 400

# nó nos.Nos(x, y, grau de liberdade x, grau de liberdade y, força nodal x, y )

####no1 = nos.Nos(0, 3, 1, 2, 48, -48)
####no2 = nos.Nos(4, 3, 3, 4, 0, 0)
####no3 = nos.Nos(4, 0, 5, 6, 0, 'x')
####no4 = nos.Nos(0, 0, 7, 8, 'x', 'x')
####nos = [no1, no2, no3, no4]
noss = []
####noss.append(no1)
####noss.append(no2)
####noss.append(no3)
####noss.append(no4)
no1 = nos.Nos(0, 3, 1, 2, 0, -15)
noss.append(no1)

no2 = nos.Nos(3, 3, 3, 4, 0, -15)
noss.append(no2)

no3 = nos.Nos(6, 3, 5, 6, 0, -15)
noss.append(no3)

no4 = nos.Nos(0, 0, 7, 8, 'x', 'x')
noss.append(no4)

no5 = nos.Nos(3, 0, 9, 10, 0, 0)
noss.append(no5)

no6 = nos.Nos(6, 0, 11, 12, 0, 'x')
noss.append(no6)


gd = []
for no in noss:
    gd.append(no.gx)
    gd.append(no.gy)
    
gdl = max(gd)
print('gdl', gdl)

##b1 = b.Barras(no1, no3, e, a, gdl)
barras = []
# banzo sup
######b1 = b.Barras(no1, no2, e, a, gdl)
######b2 = b.Barras(no3, no4, e, a, gdl)
######b3 = b.Barras(no4, no1, e, a, gdl)
######b4 = b.Barras(no3, no2, e, a, gdl)
######b5 = b.Barras(no4, no2, e, a, gdl)
######b6 = b.Barras(no1, no3, e, a, gdl)
######barras.append(b1)
######barras.append(b2)
######barras.append(b3)
######barras.append(b4)
######barras.append(b5)
######barras.append(b6)
b1 = b.Barras(no1, no2, e, a, gdl)
barras.append(b1)

b2 = b.Barras(no2, no3, e, a, gdl)
barras.append(b2)

# banzo inf
b3 = b.Barras(no4, no5, e, a, gdl)
barras.append(b3)

b4 = b.Barras(no5, no6, e, a, gdl)
barras.append(b4)

#montante
b5 = b.Barras(no4, no1, e, a, gdl)
barras.append(b5)

b6 = b.Barras(no5, no2, e, a, gdl)
barras.append(b6)

b7 = b.Barras(no6, no3, e, a, gdl)
barras.append(b7)

# diagonais
b8 = b.Barras(no4, no2, e, a, gdl)
barras.append(b8)

b9 = b.Barras(no1, no5, e, a, gdl)
barras.append(b9)

b10 = b.Barras(no5, no3, e, a, gdl)
barras.append(b10)

b11 = b.Barras(no2, no6, e, a, gdl)
barras.append(b11)


liv = []
ap = []
fa = []
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

print('graus livres - liv')
print(liv)
print('graus apoios - ap')
print(ap)
print('fa')
print(fa)
k = np.zeros((gdl,gdl))

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
print('fb')
print(np.round(fb, decimals=2))
print('ua')
print(np.round(ua, decimals=2))
print('================================================')

c = 0
for barra in barras:
    c += 1
    print(c, "barra i({0},{1})  f({2},{3})".format(barra.ni.x, barra.ni.y, barra.nf.x, barra.nf.y))
    barra.esforcos_nodais(ua, gdl, liv)
    esf = ''
    if barra.fbi[0] > 0:
        esf = 'Compressão'
    else:
        esf = 'Tração'
    print(np.round(barra.fbi, decimals=2), esf)
    print('')


def analise_matriz(noss, barras):
    gdl = len(noss) * 2
    liv = []
    ap = []
    fa = []
    
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

    k = np.zeros((gdl,gdl))

    ##k = None
    ##k = b1.kci + b2.kci + b3.kci + b4.kci + b5.kci + b6.kci
    for barra in barras:
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
    print('fb')
    print(np.round(fb, decimals=2))
    print('ua')    
    print(np.round(ua, decimals=2))

    c = 0
    for barra in barras:
        c += 1
        print(c,"barra i({0},{1})  f({2},{3})".format(barra.ni.x, barra.ni.y, barra.nf.x, barra.nf.y))
        barra.esforcos_nodais(ua, gdl, liv)
        esf = ''
        if barra.fbi[0] > 0:
            esf = 'Compressão'
        else:
            esf = 'Tração'
        print(np.round(barra.fbi, decimals=2), esf)
        print('')
    
    
##    for barra in barras:
##        barra.esforcos_nodais(ua)
##        print(barra.fbi)
