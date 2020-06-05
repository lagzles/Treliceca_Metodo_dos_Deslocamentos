# from operator import attrgetter
import barras_002 as bar
import verificar_001 as verificar

class Section():
    def __init__(self, tipo, d, bf, tw, tf, e, fy):
        self.tipo = tipo

        self.d = d
        self.bfs = bf
        self.bfi = bf
        self.tw = tw
        self.tfs = tf
        self.tfi = tf
        self.e = e
        self.g = 77000.0
        self.fy = fy
        
        self.set_propriedades()

    def set_propriedades(self):
        # self.fy = 35 * 100 # 35 kN/cm² * 100 => 3500 kgf/cm²
        if self.tipo == 'soldado':
            self.set_area()
            self.set_peso_linear()
        elif self.tipo == 'dobrado':
            if self.tw == 0.3 and self.d == 29.20: # '292x3.00'
                self.area = 14.691 # cm²
                self.peso_linear = 0.01152 * 1000  #  kg/mm * mm/m
            elif self.tw == 0.265 and self.d == 29.20: # '292x2.65':
                self.area = 12.969 # cm²
                self.peso_linear = 0.010171 * 1000
            elif self.tw == 0.225 and self.d == 29.20: # '292x2.25':
                self.area = 10.965 # cm²
                self.peso_linear = 0.0085995 * 1000
            else: # self.tw == 2.00 and self.d == 292.0: # '292x2.00':
                self.area = 9.7310 # cm²
                self.peso_linear = 0.00763 * 1000 # kgf / m
        
        self.set_j()
        self.set_ix()
        self.set_iy()
        self.set_it()
        self.set_rx()
        self.set_ry()
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


    def get_area(self):
        return self.area

    def get_peso_linear(self):
        return self.peso_linear

    def get_rx(self):
        return self.rx

    def get_ry(self):
        return self.ry

    def set_section(self, dicionario):
        self.d = dicionario['d']
        self.tw = dicionario['tw']
        self.bfs = dicionario['bf']
        self.tfs = dicionario['tf']
        self.bfi = dicionario['bf']
        self.tfi = dicionario['tf']
        self.tipo = dicionario['tipo']

        self.set_propriedades()


    def set_ly(self, ly, ky):
        self.ly = ly*ky
        self.set_lambda_y()
        return ly*ky
    
    def set_lx(self, lx, kx):
        self.lx = lx*kx
        self.set_lambda_x()
        return lx*kx


    def set_peso_linear(self):
        self.peso_linear = ((self.get_area() / 10000) * 7850)
        return self.peso_linear

    ###################################
    # PROPRIEDADES GEOMETRICAS
    ###################################

    def set_it(self):
        d = self.d
        bfs = self.bfs
        
        tw = self.tw
        tfs = self.tfs
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

        area = ((d-tfs-tfi) * tw) + (bfs * tfs) + (bfi * tfi)
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
        
        # h = (d - tf * 0.5 - tf * 0.5)
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
    
    ###########################################################
    ############### PROPRIEDADES PARA CALCULO #################
    ###########################################################
    def verificar_compressao(self):
        if self.tipo == 'soldado':
            return verificar.compressao_soldado(self)
        else:
            return verificar.compressao_dobrado(self)

    def verificar_tracao(self):
        if self.tipo == 'soldado':
            return verificar.tracao_soldado(self)
        else: 
            return verificar.tracao_dobrado(self)
