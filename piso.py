from cena_objeto import scene_object
from normalização import normalized
import numpy
from rayhit import rayhit
from PIL import Image        
import cmath

class piso(scene_object):
    def __init__(self, position = [0,0,0], normal = [0,1,0], color = (255,0,0), ka=1, kd=1, ks=1, phongN=1, kr=0, kt=0, refN = 1, texture_file = None):
        self.normal = normalized(normal)
        super().__init__(position, (255,255,255), ka, kd, ks, phongN, kr, kt, refN)
        self.texture_scale = 0.05
        if texture_file:
            self.texture = Image.open(texture_file)
        else:
            self.texture = None
    
    def getNormal(self, p):
        return self.normal
    
    def getColor(self, p):
        if self.texture is None:
            f = .025
            p_int = tuple(map(int, p.real * f))
            if numpy.floor(p_int[0]) % 2 == numpy.floor(p_int[1]) % 2:
                return (0,0,0)
            else:
                return (255,255,255)
        else:
            # Obter as coordenadas da textura
            f = 1.0 / self.texture_scale
            x = int((p[0] - self.position[0]) * f) % self.texture.width
            y = int((p[1] - self.position[1]) * f) % self.texture.height

            # Obter a cor da textura nessa coordenada
            color = self.texture.getpixel((x, y))
            return color

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
