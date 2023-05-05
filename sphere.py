from cmath import sqrt
from cena_objeto import scene_object
from rayhit import rayhit
import numpy

def normalized(vec):
    n = numpy.linalg.norm(vec)
    if n ==0:
        return vec
    else:
        return vec / n

class sphere(scene_object):

    def __init__(self, position = [0,0,0], radius = 1, color = (255,0,0), ka=1, kd=1, ks=1, phongN=1, kr=0, kt=0, refN = 1):
        self.radius = radius
        super().__init__(position, color, ka, kd, ks, phongN, kr, kt, refN)
    
    def getNormal(self, p):
        return normalized(p - self.position)
    
    def getColor(self, p):
        return super().getColor(p)
    
    def intersection(self, origin, direction):
        #formula para interseção demonstrada no stratchapixel.com
        l = self.position - origin
        
        tca = numpy.dot(l,direction)

        if tca < 0:
            return 0
        
        pitagoras = pow(numpy.linalg.norm(l) ,2) - pow(tca,2)
        if pitagoras < 0:
            return 0
        d = sqrt(pitagoras)
        
        if d.real < 0.0:
            return 0
        elif d.real > self.radius:
            return 0
        else:
            thc = sqrt(pow(self.radius,2) - pow(d,2))

            # buscamos a colisao mais proxima
            hitDist = numpy.minimum(tca - thc, tca + thc)
            
            # mas, se estamos dentro da esfera significa que o raio acabou de entrar na esfera, logo usamos a colisao mais distance
            if numpy.linalg.norm(l) < self.radius: 
                hitDist = numpy.maximum(tca-thc,tca+thc)

            hitPoint = origin + direction * hitDist

            normal = self.getNormal(hitPoint)

            color = self.getColor(hitPoint)
            
            return rayhit(self, hitPoint, normal, hitDist, color, hitPoint - origin)