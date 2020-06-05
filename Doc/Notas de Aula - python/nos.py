

class Nos(object):
    def __init__(self, x, y, gx, gy, fx, fy):
        self.x = x
        self.y = y
        
        self.gx = gx
        self.gy = gy

        self.fx = fx
        self.fy = fy

        self.id = gy / 2
        
    
    def set_fy(self, fy):
        self.fy = fy
        return fy
                
                
    def set_fx(self, fx):
        self.fx = fx
        return fx
