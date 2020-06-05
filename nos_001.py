

class Nos(object):
    def __init__(self, x, y, gx, gy, fx, fy, apoio):
        self.x = x
        self.y = y
        
        self.gx = gx
        self.gy = gy

        self.fx = fx
        self.fy = fy

        self.id = gy / 2

        self.apoio = apoio
    
    def __str__(self):
        return "nó " + str(self.id)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_fx(self):
        return self.fx
    
    def get_fy(self):
        return self.fy
    
    def get_gx(self):
        return self.gx
    
    def get_gy(self):
        return self.gy
    
    def get_id(self):
        return self.id

    def set_fy(self, fy):
        self.fy = fy
        return fy
                                
    def set_fx(self, fx):
        self.fx = fx
        return fx
    
    def add_fy(self, a):
        self.set_fy(self.get_fy() + a)
        return self.fy
    
    def add_fx(self, a):
        self.set_fx(self.get_fx() + a)
        return self.fy
