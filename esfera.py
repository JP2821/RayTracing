from cena_objeto import scene_object
from normalização import normalized
import numpy
from cmath import sqrt
from rayhit import rayhit
from PIL import Image

class sphere(scene_object):

    def __init__(self, position = [0,0,0], radius = 1, color = (255,0,0), ka=1, kd=1, ks=1, phongN=1, kr=0, kt=0, refN = 1, texture_file=None):
        self.radius = radius
        self.texture = None
        
        super().__init__(position, color, ka, kd, ks, phongN, kr, kt, refN)
        
        if texture_file is not None:
            print("ola mundo")
            self.texture = Image.open(texture_file)
        else: 
            self.texture = None
    
    def getNormal(self, p):
        return normalized(p - self.position)
    
    def getColor(self, p):
        if self.texture:
            # Mapeando as coordenadas de textura para as coordenadas 3D da esfera
            # utilizando a fórmula da esfera paramétrica
            u, v = self.getTextCoords(p)
            x = self.radius * numpy.sin(u) * numpy.cos(v)
            y = self.radius * numpy.sin(u) * numpy.sin(v)
            z = self.radius * numpy.cos(u)
            tex_x = int((v / (2 * numpy.pi)) * self.texture.width) % self.texture.width
            tex_y = int((u / numpy.pi) * self.texture.height) % self.texture.height
            color = self.texture.getpixel((tex_x, tex_y))
        else:
            color = super().getColor(p)
        return color
    
    def intersection(self, origin, direction):
        # formula para interseção demonstrada no stratchapixel.com
        l = self.position - origin

        tca = numpy.dot(l, direction)

        if tca < 0:
            return 0

        pitagoras = pow(numpy.linalg.norm(l), 2) - pow(tca, 2)
        if pitagoras < 0:
            return 0
        d = sqrt(pitagoras)

        if d.real < 0.0:
            return 0
        elif d.real > self.radius:
            return 0
        else:
            thc = sqrt(pow(self.radius, 2) - pow(d, 2))

            # buscamos a colisao mais proxima
            hitDist = numpy.minimum(tca - thc, tca + thc)

            # mas, se estamos dentro da esfera significa que o raio acabou de entrar na esfera,
            # logo usamos a colisao mais distance
            if numpy.linalg.norm(l) < self.radius:
                hitDist = numpy.maximum(tca - thc, tca + thc)

            hitPoint = origin + direction * hitDist

            normal = self.getNormal(hitPoint)

            color = self.getColor(hitPoint)

            return rayhit(self, hitPoint, normal, hitDist, color, hitPoint - origin)

    def getTextCoords(self, p):
        x, y, z = p - self.position
        r = numpy.linalg.norm([x, y, z])
        if r == 0:
            return 0, 0
        u = numpy.arccos(z / r).astype(float)
        v = (numpy.arctan(x / y) + numpy.pi).astype(float)
        
        return u / numpy.pi, v / (2 * numpy.pi)
