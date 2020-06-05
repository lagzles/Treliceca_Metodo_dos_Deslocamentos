from operator import attrgetter
import barras_001 as bar

class Pecas(bar.Barras):
    def __init__(self, barra_i, barra_f, tipo,
                 d, bf, tw, tf, lx, ly):
        self.tipo = tipo
        #self.lista_barras = lista_barras

        self.d = d
        self.bfs = bf
        self.bfi = bf
        self.tw = tw
        self.tfs = tf
        self.tfi = tf

        self.lx = lx
        self.ly = ly
        
        self.set_propriedades()
        
        self.ni_x = barra_i.ni.x
        self.nf_x = barra_f.nf.x

        self.barra_i = barra_i
        self.barra_f = barra_f
        #self.tracao = min(barra_i.tracao, barra_f.tracao)
        #self.compressao = max(barra_i.tracao, barra_f.tracao)
        self.get_tracao()
        self.get_compressao()
        # pegar os objetos barras, que possuirem os maiores valores
        # de tração

    def set_propriedades(self):
        self.set_area()
        self.set_j()
        self.set_ix()
        self.set_iy()
        self.set_it()
        self.set_rx()
        self.set_ry()
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
##
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

#######################################################
               
    def get_tracao(self):
        self.tracao = min(self.barra_i.tracao, self.barra_f.tracao)
        return min(self.barra_i.tracao, self.barra_f.tracao)
        #return min(barra.tracao for barra in self.lista_barras)
    
    def get_compressao(self):
        self.compressao = max(self.barra_i.compressao, self.barra_f.compressao)
        return min(self.barra_i.compressao, self.barra_f.compressao)
        #return max(barra.compressao for barra in self.lista_barras)

    def get_ni_id(self):
        return self.barra_i.ni.id

    def get_nf_id(self):
        return self.barra_f.nf.id

    ## TODO ajustar para funções de classe
    ## funções para calculo de compressão axial
    ## Verificacao a compressao axial

    def r_o(self): #rx, ry, xo, yo):
        rx = self.rx
        ry = self.ry
        xo = self.xo
        yo = self.yo
        self.ro = (rx ** 2 + ry ** 2 + xo ** 2 + yo ** 2) ** 0.5
        return self.ro # (rx ** 2 + ry ** 2 + xo ** 2 + yo ** 2) ** 0.5


    def ne_x(self): #e, ix, kx, lx):
        e = self.e
        ix = self.ix
        lx = self.lx
        kx = self.kx
        self.ne_x = (3.14 ** 2) * e * ix / ((kx * lx) ** 2)
        return self.ne_x # (3.14 ** 2) * e * ix / ((kx * lx) ** 2)


    def ne_y(self): #e, iy, ky, ly):
        e = self.e
        iy = self.iy
        ly = self.ly
        ky = self.ky
        self.ne_y = (3.14 ** 2) * e * iy / ((ky * ly) ** 2)
        return self.ne_y # (3.14 ** 2) * e * iy / ((ky * ly) ** 2)


    def ne_z(self): # e, g, j, cw, kz, lz, ro):
        e = self.e
        g = self.g
        j = self.j
        cw = self.cw
        kz = self.kz
        lz = self.lz
        ro = self.ro
        ne = (1 / ro ** 2) * (((3.14 ** 2) * e * cw) / ((kz * lz) ** 2) + g * j)
        self.ne_z = ne
        return ne #(1 / ro ** 2) * (((3.14 ** 2) * e * cw) / ((kz * lz) ** 2) + g * j)


    def n_e(self):  # e, ix, kx, lx, iy, ky, ly, g, j, cw, kz, lz, ro):
        nex = self.ne_x() #(e, ix, kx, lx)
        ney = self.ne_y() #(e, iy, ky, ly)
        nez = self.ne_z() #(e, g, j, cw, kz, lz, ro)    
        n_e = max(nex, ney, nez)
        self.ne = n_e
        return n_e


    def detlambZero(fatorQ, area, fy, ne):
        detlambZero = (fatorQ * area * fy / ne) ** 0.5
        return detlambZero


    def detfatorX(lambZero):
        if lambZero <= 1.5:
            detfatorX = (0.658 ** (lambZero ** 2))
        else:
            detfatorX = 0.877 / (lambZero ** 2)
        return detfatorX


    def nc_rd(e, d, tw, bfs, tfs, bfi, tfi, ix, kx, lx, iy, ky, ly, g, j, cw, kz, lz, ro, area, fy):
        fatorXi = 1
        fatorQ = detfatorQ(e, d, tw, bfs, tfs, bfi, tfi, fatorXi, fy)
        ne = n_e(e, ix, kx, lx, iy, ky, ly, g, j, cw, kz, lz, ro)
        lambZero = detlambZero(fatorQ, area, fy, ne)
        
        fatorXf = fatorXi
        fatorXi = detfatorX(lambZero)
        
        while fatorXf != fatorXi:
        
            fatorQ = detfatorQ(e, d, tw, bfs, tfs, bfi, tfi, fatorXi, fy)
            ne = n_e(e, ix, kx, lx, iy, ky, ly, g, j, cw, kz, lz, ro)
            lambZero = detlambZero(fatorQ, area, fy, ne)
            
            fatorXf = fatorXi
            fatorXi = detfatorX(lambZero)
        
        fatorX = fatorXf
        
        nc_rd = fatorX * fatorQ * area * fy / 1.15
        return nc_rd



    def detfatorQ(e, d, tw, bfs, tfs, bfi, tfi, fatorX, fy):
        area_bruta = prop.area(d, tw, bfs, tfs, bfi, tfi)
        
        ca = 0.34
        
        sigma = fatorX * fy
        
        b = d - tfs - tfi
        
        largura_efetiva = 1.92 * tw * ((e / sigma) ** 0.5) * (1 - ca / (b / tw) * ((e / sigma) ** 0.5))
            
        if largura_efetiva >= b:
            fatorQa = 1
        else:
            area_efetiva = area_bruta - (b - largura_efetiva) * tw
            fatorQa = area_efetiva / area_bruta
            
        b = bfs / 2
        t = tfs
        kc = 4 / ((d - tfs / 2 - tfi / 2) / tw) ** 0.5
        if kc <= 0.35:
            kc = 0.35
        elif kc >= 0.76:
            kc = 0.76
               
        btlimite = 0.64 * (e / (fy / kc)) ** 0.5
        btminimo = 1.17 * ((e / (fy * kc)) ** 0.5)
        
        bt = b / (2 * t)

        if bt <= btlimite:
            fatorQs = 1.0    
        elif bt > btlimite and bt <= btminimo:        
            fatorQs = 1.415 - 0.65 * bt * (fy / (kc * e)) ** 0.5
    ##        print fatorQs
    ##        print "bt = {0}     btlim = {1}     btmin = {2}".format(bt, btlimite, btminimo)
            
        elif bt > btminimo:
            fatorQs = 0.9 * e * kc / (fy * (bt ** 2))
                  
        if fatorQs < 0:        
            fatorQs = 0
            
        detfatorQ = fatorQs * fatorQa
        return detfatorQ


    
