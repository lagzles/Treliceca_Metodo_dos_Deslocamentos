import matplotlib.pyplot as plt
#from anastruct.fem.system import SystemElements as struct



### Plotagem do diagrama de Cortante
##plt.subplot(311)
##for valor in listaCortantes:
##    plt.text(valor[0], valor[1], '%.2f kN' % valor[1], fontsize=7)
##
##
##plt.plot(xp, ypv, 'b')
##plt.plot([x,xn],[0., 0.],'k')
##plt.xlabel('x')
##plt.ylabel('y')
##plt.ylim(min(ypv)*1.5, max(ypv)*1.5)
##plt.legend(['V[x]'])
##plt.title('Cortante [kN], Momento [kN.m] Flecha [cm]')
##plt.grid()

# valor do vao em metros
vao = 27
vaos = [27,37,12]
meio_vao = round(vao / 2, 2)
espacamento_padrao = 1.5

# altura viga treliçada
h_viga = round(vao/15,2)

print(h_viga)
               

espacamento_calc = 2.1

n_vao_montantes = round(vao / espacamento_padrao,0)
while espacamento_calc > 2:
    espacamento_calc = vao / n_vao_montantes
    n_vao_montantes +=1 # round(vao / espacamento_padrao,0)
##    print('n_vao_montantes',n_vao_montantes)
##    print('espacamento_calc',espacamento_calc)

print('espacamento_calc',espacamento_calc)
coord_x = {}
x = 0
i = 1
coord_x[i] = x
print('n_vao_montantes',n_vao_montantes)
##print('x', x, i)
while x < vao:
    x += espacamento_calc
    i += 1
    coord_x[i] = x
    
##    print('x', x, i)
print('valores de x', len(coord_x))
print('chaves', coord_x.keys())
##print(coord_x)

coord_y = {}
y = 0
i = 0
coord_y[i] = y
dy = 0
for k in range(1, int(n_vao_montantes)+1):
    dy = h_viga*3/100
    y += dy
    i += 1
    coord_y[i] = y
##    print('y', y, 'dy', dy, i, k)
    
##print(coord_y)

nos = {}
for i in range(1, int(n_vao_montantes) + 1):
    nos[i]=[coord_x[i], round(coord_y[i],2)]
    nos[i+n_vao_montantes]=[coord_x[i], round(coord_y[i]+h_viga,2)]


##print(nos)

def apoios(plot, x, y):
    plt.plot([x + .5, x - .5],[y - .5,y - .5],'k')
    plt.plot([x + .5, x],[y - .5, y],'k')
    plt.plot([x, x - .5],[y, y - .5],'k')
    

    
plt.subplot(111)



# lançamento de banzos
for i in range(1, int(n_vao_montantes)):
    # lançamento apoios
    if i == 1:
        apoios(plt, nos[i][0], nos[i][1])
    elif i == (n_vao_montantes-1):
        apoios(plt, nos[i+1][0], nos[i+1][1])
    # banzo inferior
    x1a = nos[i][0]
    x2a = nos[i+1][0]
    y1a = nos[i][1]
    y2a = nos[i+1][1]
    plt.plot([x1a, x2a], [y1a, y2a],'b')
    plt.text(x1a, y1a, i, fontsize=7)
    plt.text(x2a, y2a, i+1, fontsize=7)
    # banzo superior
    k = i + int(n_vao_montantes)
    x1b = nos[k][0]
    x2b = nos[k+1][0]
    y1b = nos[k][1]
    y2b = nos[k+1][1]
    plt.plot([x1b, x2b], [y1b, y2b],'b')
    plt.text(x1b, y1b, k, fontsize=7)
    plt.text(x2b, y2b, k+1, fontsize=7)
    # montantes
    plt.plot([x1a, x1b], [y1a, y1b],'b')
    if i == (n_vao_montantes-1):
        plt.plot([x2a, x2b], [y2a, y2b],'b')    
    # diagonais
    if x1a >= meio_vao:
        plt.plot([x1a, x2b], [y1a, y2b],'b')
    else:
        plt.plot([x2a, x1b], [y2a, y1b],'b')
    #plt.plot([nos[k][0],nos[k+1][0]],[nos[k][1],nos[k+1][1]],'b')

#lançamento de montantes


plt.xlabel('x')
plt.ylabel('y')
plt.ylim(-vao/2, vao/2)
plt.grid()

plt.show()

##n_vao_montantes = round(vao / espacamento_padrao,0)
##
##espacamento_calc = vao / n_vao_montantes
##
##print('n_vao_montantes',n_vao_montantes)
##print('espacamento_calc',espacamento_calc)


e = 2.0 * (10 ** 12) # MPa - 10 x kN/m2
a = 100 * (100**-2)# m2
i = 0.000997543

#ss = SystemElements(EA=e*a/10)

