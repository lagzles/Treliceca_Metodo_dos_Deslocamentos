import numpy as np
import math as m

class Barras(object):
    def __init__(self, ni, nf, e, a, gdl, tipo):
        self.ni = ni
        self.nf = nf
        self.e = 20000.0 #kN/cm2 # e
        self.fy = 34.5 #kN/cm2
        self.fu = 41.5 #kN/cm2
        self.a = a
        self.gdl = gdl # graus de liberdade
        self.compressao = 0
        self.tracao = 0
        self.tipo = tipo

##        self.comprimento()
##        self.set_theta()
##        self.set_ki()
    ######################################################
    ## 1 - FUNÇÔES PARA METODO DOS DESLOCAMENTOS!
    def set_gdl(self, gdl):
        self.gdl = gdl
        self.find_kci()

    def comprimento(self):
        x1 = self.ni.x
        x2 = self.nf.x
        y1 = self.ni.y
        y2 = self.nf.y
        self.lb = ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)
        return self.lb

    def set_theta(self):
        x1 = self.ni.x
        x2 = self.nf.x
        y1 = self.ni.y
        y2 = self.nf.y

        if (x1 - x2) == 0: # caso a barra esteja na horizontal
            self.theta = m.acos(0)
        elif (y1 - y2) == 0: # caso a barra esteja na vertical
            self.theta = m.asin(0)
        else:
            # retorna em radianos
            self.theta = m.atan((y2 - y1)/ (x2 - x1))
        
    def set_ki(self):
        e = self.e
        a = self.a
        l = self.lb
        theta = self.theta
        
        kbi = np.zeros((4,4))
        kbi[0][0] = e * a / l
        kbi[2][0] = - e * a / l
        kbi[2][2] = e * a / l
        kbi[0][2] = - e * a / l

        self.kbi = kbi
        
        ti_t = np.zeros((4,4))
        ti_t[0][0] = round(m.cos(theta),4)
        ti_t[0][1] = round(m.sin(theta),4)
        ti_t[1][0] = - round(m.sin(theta),4)
        ti_t[1][1] = round(m.cos(theta),4)

        ti_t[2][2] = round(m.cos(theta),4)
        ti_t[2][3] = round(m.sin(theta),4)
        ti_t[3][2] = - round(m.sin(theta),4)
        ti_t[3][3] = round(m.cos(theta),4)

        self.ti = ti_t

        ki = np.dot(np.dot(np.transpose(ti_t), kbi),ti_t)
        self.ki = ki


    def find_kci(self):
        gdl = self.gdl
        self.comprimento()
        self.set_theta()
        self.set_ki()
        li = np.zeros((4,gdl))

        li[0][self.ni.gx - 1] = 1
        li[1][self.ni.gy - 1] = 1
        li[2][self.nf.gx - 1] = 1
        li[3][self.nf.gy - 1] = 1
        self.li = li
        ki = self.ki
        
        self.kci = np.dot(np.dot(np.transpose(li), ki),li)

    # 1 - FIM
    ######################################################

    def esforcos_nodais(self, u, gdl, liv):
        # gdl graus de liberdade do sistema
        # matriz de deslocamentos nodais
        # matriz com graus de liberdade livres
        ua = np.zeros((gdl,))
        for i in range(len(u)):            
            ua[liv[i]] = u[i]
            
        fbi = np.dot(np.dot(np.dot(self.kbi, self.ti), self.li), ua)
        self.fbi = fbi
        self.compressao = max(fbi[0], self.compressao)
        self.tracao = min(fbi[0], self.tracao)
