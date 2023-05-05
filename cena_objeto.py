class scene_object:
    def __init__(self, position = [0,0,0], color = (255,0,0), ka=1, kd=1, ks=1, phongN=1, kr=0, kt=0, refN = 1):
        self.position = position
        self.color = color        
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.phongN = phongN
        self.kr = kr
        self.kt = kt
        self.refN = refN
    
    def getColor(self,p):
        return self.color

    # retorna a normal no ponto p
    def getNormal(self, p):
        return
    
    # retorna 0 se não houver hit, se houver retorna um rayhit
    def intersection(self, origin, direction):
        return
