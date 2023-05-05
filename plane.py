from cena_objeto import scene_object
from normalização import normalized
import numpy
from rayhit import rayhit

class plane(scene_object):
    def __init__(self, position = [0,0,0], normal = [0,1,0], color = (255,0,0), ka=1, kd=1, ks=1, phongN=1, kr=0, kt=0, refN = 1):
        self.normal = normalized(normal)
        super().__init__(position, color, ka, kd, ks, phongN, kr, kt, refN)
    
    def getNormal(self, p):
        return self.normal
    
    def getColor(self, p):
        return super().getColor(p)

    def intersection(self, origin, direction):       
        ldotn = numpy.dot(normalized(direction),normalized(self.normal))

        if ldotn >= 0.000:
            return 0
        
        t = numpy.dot((self.position - origin), self.normal) / ldotn
        
        if t<0:
            return 0
        else:
            hitPoint = origin + direction * t
            normal = self.getNormal(hitPoint)
            color = self.getColor(hitPoint)
            return rayhit(self, hitPoint, normal, t, color, hitPoint - origin)