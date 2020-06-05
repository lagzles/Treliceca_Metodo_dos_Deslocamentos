import barras as b
import nos
import numpy as np


e = 300
a = 400

# nó nos.Nos(x, y, gx, gy)

no1 = nos.Nos(0, 3, 1, 2)
no2 = nos.Nos(4, 3, 3, 4)
no3 = nos.Nos(4, 0, 5, 6)
no4 = nos.Nos(0, 0, 7, 8)


##b1 = b.Barras([0,3],[4,3],e,a)
##b2 = b.Barras([0,0],[4,0],e,a)
##b3 = b.Barras([0,0],[0,3],e,a)
##b4 = b.Barras([4,0],[4,3],e,a)
##b5 = b.Barras([0,0],[4,3],e,a)
##b6 = b.Barras([0,3],[4,0],e,a)

b1 = b.Barras(no1, no2, e, a)
b2 = b.Barras(no4, no3, e, a)
b3 = b.Barras(no4, no1, e, a)
b4 = b.Barras(no3, no2, e, a)
b5 = b.Barras(no4, no2, e, a)
b6 = b.Barras(no1, no3, e, a)


##b1.find_kci(1,2,3,4,8)
##b2.find_kci(7,8,5,6,8)
##b3.find_kci(1,2,7,8,8)
##b4.find_kci(5,6,3,4,8)
##b5.find_kci(7,8,3,4,8)
##b6.find_kci(1,2,5,6,8)

b1.find_kci(8)
b2.find_kci(8)
b3.find_kci(8)
b4.find_kci(8)
b5.find_kci(8)
b6.find_kci(8)

b1.kci + b2.kci + b3.kci + b4.kci + b5.kci + b6.kci
# para pegar deslocamentos nodais
kaa = np.delete(np.delete(k,range(5,8), axis=0),range(5,8),axis=1)

# para pegar as reações
kbb = np.delete(np.delete(k,range(0,5), axis=0),range(5,8),axis=1)

# forças externas
faa = np.array([48,-48,00,0,0])

# deslocamentos nodais
uaa =np.dot( np.linalg.inv(kaa),faa)

# reações nos apoios
fb = np.dot(kbb, uaa)

print('k')
print(k)



