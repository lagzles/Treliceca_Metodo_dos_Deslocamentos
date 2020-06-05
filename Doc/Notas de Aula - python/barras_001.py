import numpy as np
import math as m

#### TODO
#### metodos de verificação, propriedades
#### ajuste de comprimentos de flambagem nas duas direções

class Barras(object):
    def __init__(self, ni, nf, gdl, tipo):
        self.ni = ni
        self.nf = nf
        self.e = 20000.0 #kN/cm2 # e
        self.fy = 34.5 #kN/cm2
        self.fu = 41.5 #kN/cm2

        # seção default para barras
        self.d = 30
        self.tw = 0.375
        self.bfs = 15.0
        self.tfs = 0.635
        self.bfi = 15.0
        self.tfi = 0.635

        self.ly = self.comprimento()
        self.lx = self.comprimento()

        self.set_propriedades()
         
        #self.a = a
        self.gdl = gdl # graus de liberdade
        self.compressao = 0
        self.tracao = 0
        self.tipo = tipo


    ######################################################
    ## 1 - FUNÇÔES PARA METODO DOS DESLOCAMENTOS!
    def set_gdl(self, gdl):
        self.gdl = gdl
        self.set_kci()


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
        
        self.theta = m.atan((y2 - y1)/ (x2 - x1))
        
#        if (x1 - x2) == 0: # caso a barra esteja na horizontal
#            self.theta = m.acos(0)
#            #self.theta = m.asin(0)
#        elif (y1 - y2) == 0: # caso a barra esteja na vertical
#            self.theta = m.asin(0)
#            #self.theta = m.acos(0)
#        else:
#            # retorna em radianos            
#            self.theta = m.atan((y2 - y1)/ (x2 - x1))
#            #self.theta = m.atan((x2 - x1)/ (y2 - y1))


    def set_ki(self):
        e = self.e
        a = self.area
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
        ti_t[0][2] = 0
        ti_t[0][3] = 0
        
        ti_t[1][0] = - round(m.sin(theta),4)
        ti_t[1][1] = + round(m.cos(theta),4)
        ti_t[1][2] = 0
        ti_t[1][3] = 0

        ti_t[2][0] = 0
        ti_t[2][2] = 0
        ti_t[2][2] = round(m.cos(theta),4)
        ti_t[2][3] = round(m.sin(theta),4)
        
        ti_t[3][0] = 0
        ti_t[3][1] = 0
        ti_t[3][2] = - round(m.sin(theta),4)
        ti_t[3][3] = + round(m.cos(theta),4)

        self.ti = ti_t
        
        a = np.transpose(ti_t)        
        b = np.dot(a, kbi)
        c = np.dot(b, ti_t)
        self.ki = c #ki
        #ki = np.dot(np.dot(np.transpose(ti_t), kbi),ti_t)


    def set_kci(self):
        gdl = self.gdl
        self.comprimento()
        self.set_theta()
        self.set_ki()
        li = np.zeros((4, gdl))

        li[0][self.ni.gx - 1] = 1
        li[1][self.ni.gy - 1] = 1
        li[2][self.nf.gx - 1] = 1
        li[3][self.nf.gy - 1] = 1
        self.li = li
        ki = self.ki
        a = np.transpose(li)
        b = np.dot(a, ki)
        c = np.dot(b, li)
        self.kci = c
        #self.kci = np.dot(np.dot(np.transpose(li), ki),li)


    # 1 - FIM
    ######################################################

    def esforcos_nodais(self, ua_list, gdl, liv):
        # gdl graus de liberdade do sistema
        # matriz de deslocamentos nodais
        # matriz com graus de liberdade livres
        # ua_list - lista com deslocamentos nodais gravitacionais e de vento
        #print(self.tipo)
        for u in ua_list:
            # cria uma matriz de 'zeros' de dimensões gdl x gdl
            ua = np.zeros((gdl,))
            for i in range(len(u)):
                # para nó livre, atribuir o valor na matriz de zeros
                ua[liv[i]] = u[i]
            
            # print(ua)
            fbi = np.dot(np.dot(np.dot(self.kbi, self.ti), self.li), ua)
            self.fbi = fbi
            # print(fbi)
            self.compressao = max(fbi[0], self.compressao)
            self.tracao = min(fbi[0], self.tracao)
        #print()


    def set_propriedades(self):
        self.set_area()
        self.set_j()
        self.set_ix()
        self.set_iy()
        self.set_it()
        self.set_rx()
        self.set_ry()
        self.set_peso()
        self.fy = 35

        self.set_rt()
        self.set_wx()
        self.set_wy()
        self.self_cgx()
        self.self_cgy()
        self.set_zx()
        self.set_zy()
        self.set_tensaor()
        self.set_cw()
        self.set_kc()
        self.set_lambda_y()
        self.set_lambda_x()        


    def set_peso(self):
        a = self.area # cm²
        lb = self.comprimento() # m

        peso = 7850 *(lb) * (a / 10000)
        self.peso = peso
        return peso
 
 
    def set_it(self):
        d = self.d
        bfs = self.bfs
        bfi = self.bfi
        
        tw = self.tw
        tfs = self.tfs
        tfi = self.tfi
        i_t = (((2 * bfs * (tfs ** 3))) + ((d - tfs) * (tw ** 3))) / 3.0
        self.it = i_t
        return i_t    


    def set_area(self):
        d = self.d
        bfs = self.bfs
        bfi = self.bfi
        
        tw = self.tw
        tfs = self.tfs
        tfi = self.tfi
        area = (((d) * tw) + (bfs * tfs) + (bfi * tfi))
        self.area = area
        return area


    def set_rx(self):
        ix = self.ix
        area = self.area
        r_x = (ix / area) ** (0.5)
        self.rx = r_x
        return r_x


    def set_ry(self):
        iy = self.iy
        area = self.area
        r_y = ((iy / area) ** (0.5))
        self.ry = r_y
        return r_y


    def set_j(self):
        d = self.d
        bfs = self.bfs
        bfi = self.bfi
        
        tw = self.tw
        tfs = self.tfs
        tfi = self.tfi
        
        h = (d - tfs * 0.5 - tfi * 0.5)
        j = 1 / 3.0 * (bfs * tfs ** 3 + bfi * tfi ** 3 + h * tw ** 3) / 1.0
        self.j = j
        return j


    def set_ix(self):
        d = self.d
        bfs = self.bfs
        bfi = self.bfi
        
        tw = self.tw
        tfs = self.tfs
        tfi = self.tfi

        i_x = (bfs * tfs * ((d / 2.0 - tfs / 2.0) ** 2) + bfi * tfi * (d / 2.0 - tfi / 2.0) ** 2 + tw * ((d - tfs - tfi) ** 3) / 12.0) / 1
        self.ix = i_x
        return i_x


    def set_iy(self):
        d = self.d
        bfs = self.bfs
        bfi = self.bfi
        
        tw = self.tw
        tfs = self.tfs
        tfi = self.tfi
        i_y = (tfs * bfs ** 3.0 / 12.0 + tfi * bfi ** 3 / 12.0 + (d - tfs - tfi) * tw ** 3 / 12.0) / 1
        self.iy = i_y
        return i_y
###################################

    def set_rt(self):
        it = self.it
        area = self.area

        r_t = ((it / area) ** (0.5))
        self.rt = r_t
        return r_t


    def set_wx(self):
        ix = self.ix
        d = self.d

        wx = (2 * ix) / d
        self.wx = wx
        return wx


    def set_wy(self):
        iy = self.iy
        d = self.d

        wy = (2 * iy) / d
        self.wy = wy
        return wy


    def self_cgx(self):
        d = self.d

        cgx = d / 2.0
        self.cgx = cgx
        return cgx


    def self_cgy(self):
        bfs = self.bfs        

        cgy = bfs / 2.0
        self.cgy = cgy
        return cgy


    def set_zx(self):
        bf = self.bfs
        tf = self.tfs
        d = self.d
        tw = self.tw
        
        hw = d - 2 * tf
        zx1 = bf * (d * d - hw * hw)
        zx2 = tw * hw * hw
        zx = (zx1 + zx2) / 4.0
        self.zx = zx
        return zx


    def set_zy(self):
        bf = self.bfs
        tf = self.tfs
        d = self.d
        tw = self.tw
        
        hw = d - 2 * tf
        zy = ((bf ** 2) * tf * 0.5) + (0.25 * hw * tw ** 2)
        self.zy = zy
        return zy


    def set_tensaor(self):
        fy = self.fy
        tr = 0.3 * fy

        self.tr = tr
        return tr


    def set_cw(self):
        d = self.d
        tf = self.tfs
        bf = self.bfs
        
        h = (d - tf * 0.5 - tf * 0.5)
        cw = ((bf ** 3)* tf / 12.0) * (((d - tf) ** 2) / 2.0)
        self.cw = cw
        return cw


    def set_kc(self):
        tf = self.tfs
        d = self.d
        tw = self.tw
        
        hw = d - 2 * tf
        kc = 4 / ((hw / tw)**0.5)
        self.kc = kc
        return kc


    def set_lambda_y(self):
        ly = self.ly
        ry = self.ry
        
        lambda_y = ly / ry
        self.lambda_y = lambda_y
        return lambda_y


    def set_lambda_x(self):
        lx = self.lx
        rx = self.rx
        
        lambda_x = lx / rx
        self.lambda_x = lambda_x
        return lambda_x


