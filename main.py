import numpy
from PIL import Image
from multiprocessing import Process, Array
from rayhit import rayhit
from normalização import normalized
from esfera import sphere
from plane import plane
from piso import piso
from color_fuctions import colorDenormalize,colorMul,colorNormalize,colorScale,colorSum
from reflexão_e_refração import reflect,refract
    

class scene_main:
    def __init__(self):
        
        self.objs = []
        self.lights = []
        self.bg_color = (0,0,0)
        self.ambientLight = (0,0,0)
    
    def setBackground_Color(self, color):
        self.bg_color = color
    
    def getBackground_Color(self):
        return self.bg_color

    def addSphere(self, position, radius, color, ka, kd, ks, phongN, kr, kt, refN):
        self.objs.append(sphere(position, radius, color, ka, kd, ks, phongN, kr, kt, refN))
    
    def addPlane(self, position, normal, color, ka, kd, ks, phongN, kr, kt, refN):
        self.objs.append(plane(position, normal, color, ka, kd, ks, phongN, kr, kt, refN))

    def addPiso(self, position, normal, color, ka, kd, ks, phongN, kr, kt, refN):
        self.objs.append(piso(position, normal, color, ka, kd, ks, phongN, kr, kt, refN))

    def addPointLight(self, position, color):
        self.lights.append(pointLight(position, color))
    
    def setAmbientLight(self, color):
        self.ambientLight = color
    

class light:
    def __init__(self, position, color):
        self.position = position
        self.color = color


class pointLight(light):

    def __init__(self, position, color):
        super().__init__(position, color)


def render(res_h, res_v, pxl_size,d,cam_pos,cam_forward,cam_up, scene, max_depth):

    img = Image.new('RGB', (res_h,res_v), color = (0,0,0))
    

    cam_right = numpy.asarray(numpy.cross(cam_up, cam_forward))
    
 
    topleft = cam_pos + cam_forward * d + (cam_up *  (res_v - 1) - cam_right * (res_h - 1)) * pxl_size * 0.5
    

    thread_count = 12
    
   
    xranges = []

    for i in range(thread_count):
        xranges.append(int(i * (res_h / thread_count)))
    xranges.append(res_h)
    

    all_threads = []

    ars = []


    for t in range(thread_count):
        ars.append(Array("i", range(res_v * (xranges[t + 1] - xranges[t]))))
        ars.append(Array("i", range(res_v * (xranges[t + 1] - xranges[t]))))
        ars.append(Array("i", range(res_v * (xranges[t + 1] - xranges[t]))))

        all_threads.append(Process(target=thread_render, args=(cam_pos,cam_up,cam_right,topleft,pxl_size,scene,xranges[t],xranges[t+1],0,res_v, 
            max_depth, ars[t*3],ars[t*3+1], ars[t*3+2]),daemon=True))
    

    for x in all_threads:
        x.start()
    

    for x in all_threads:
        x.join()


    for i in range(thread_count):
        for x in range(xranges[i + 1] - xranges[i]):
            for y in range(res_v):
                c = (ars[i * 3 + 0][x * res_v + y] ,ars[i * 3 + 1][x * res_v + y] ,ars[i * 3 + 2][x * res_v + y])              
                img.putpixel((xranges[i] + x, y),c)       

    img.save('test3.png')
    print("imagem salva")


# Essa função é responsável por renderizar uma parte da imagem em uma cena 3D, usando o
# método de raycasting para determinar a cor de cada pixel. Os argumentos de entrada
# incluem a posição da câmera, as dimensões da imagem, a cena, o intervalo de pixel a ser 
# renderizado, a profundidade máxima da recursão, e três listas vazias que serão preenchidas
# com os valores dos componentes vermelho, verde e azul de cada pixel renderizado.

# A função itera sobre cada pixel dentro do intervalo especificado (dado pelos parâmetros x0,
# x1, y0, y1) e calcula a direção do raio a partir da câmera. Em seguida, utiliza o método "cast"
# para calcular a cor do pixel correspondente com base na interseção do raio com os objetos
# da cena. O resultado é normalizado e salvo nas listas correspondentes. Por fim, a função
# imprime uma mensagem informando que a execução da thread foi concluída.
def thread_render(cam_pos, cam_up, cam_right, topleft, pxl_size, scene, x0, x1, y0, y1, max_depth, arsR,arsG,arsB):
    
    for x_ in range(x1-x0):
        x = x_ + x0
        
        for y_ in range(y1-y0):
            y = y_ + y0

            ray_dir = normalized((topleft + (cam_up * -y + cam_right * x) * pxl_size) - cam_pos)
            c = colorDenormalize(cast(cam_pos,ray_dir, scene, max_depth))
            arsR[x_ * y1 + y_] = c[0]
            arsG[x_ * y1 + y_] = c[1]
            arsB[x_ * y1 + y_] = c[2]
    
    print("thread end")



def cast(origin, direction,scene, counter):
    color = colorNormalize(scene.getBackground_Color())
    hit = trace(origin,direction,scene)
    if hit:
        color = shade(hit, scene, counter)
        
    return (color)


def trace(origin, direction, scene:scene_main):
    hit = 0

    
    for i in range(len(scene.objs)):

        hitCheck = scene.objs[i].intersection(origin,direction)
         
        if hitCheck != 0 and (hit == 0 or hitCheck.hitDistance < hit.hitDistance):
            hit = hitCheck
    
    return hit


def shade(hit:rayhit, scene:scene_main, counter):
    
    color_difuse = colorNormalize(hit.color)
   
    color =  colorScale(colorMul(color_difuse, colorNormalize(scene.ambientLight)), hit.hitObj.ka)

    
    for light in scene.lights:
        color_light = colorNormalize(light.color)
        l = light.position - hit.hitPoint
        lDist = numpy.linalg.norm(l)
        l = normalized(l)

        ndotl = numpy.dot(hit.hitNormal, l).real
        
        
       
        if ndotl > 0:
            shadowHit = trace(hit.hitPoint + l *0.00001, l, scene)
            if shadowHit !=0 and shadowHit.hitDistance < lDist:
                continue
            
            
            color = colorSum(color, colorScale(colorMul(color_light, color_difuse), ndotl * hit.hitObj.kd))
            
            rj = 2 * ndotl * hit.hitNormal - l

            view = normalized(-hit.ray)
            rjdotview = numpy.dot(rj,view).real
            if rjdotview < 0:
                rjdotview = 0
            
            
            color = colorSum(color, colorScale(color_light , hit.hitObj.ks * numpy.power(rjdotview, hit.hitObj.phongN)))


    if counter > 0:
      
        kr = hit.hitObj.kr
        if hit.hitObj.kt > 0:
            view = normalized(hit.ray)
            rayDir = refract(view, normalized(hit.hitNormal), hit.hitObj.refN)
            
            if numpy.isscalar(rayDir) == False:
                
                refColor = cast(hit.hitPoint + rayDir * 0.00001, rayDir, scene, counter-1)
                
                color = colorSum(color,colorScale(refColor, hit.hitObj.kt))
            else: 
                kr = 1
        
       
        if kr > 0:
            view = normalized(hit.ray)
            rayDir = reflect(view, hit.hitNormal)
            
            refColor = cast(hit.hitPoint + rayDir * 0.00001, rayDir, scene, counter-1)
           
            color = colorSum(color,colorScale(refColor, kr))
    

    return color

if __name__ == '__main__':

    new_scene = scene_main()


    xyz_coord = (1,-1,1)

   
    with open("input.txt") as f:
        inputs = f.read().split()

    index = 0

    res_vertical = int(inputs[index])
    index +=1
    res_horizontal = int(inputs[index])
    index +=1
    size_pixel = float(inputs[index])
    index +=1
    cam_dist = float(inputs[index])
    index +=1
    cam_pos_x = float(inputs[index])
    index +=1
    cam_pos_y = float(inputs[index])
    index +=1
    cam_pos_z = float(inputs[index])
    index +=1
    cam_forward_x = float(inputs[index])
    index +=1
    cam_forward_y = float(inputs[index])
    index +=1
    cam_forward_z = float(inputs[index])
    index +=1
    cam_up_x = float(inputs[index])
    index +=1
    cam_up_y = float(inputs[index])
    index +=1
    cam_up_z = float(inputs[index])
    index +=1
    bg_color_r = int(inputs[index])
    index +=1
    bg_color_g = int(inputs[index])
    index +=1
    bg_color_b = int(inputs[index])
    index +=1
    max_depth = int(inputs[index])
    index +=1
    k_obj = int(inputs[index])
    index +=1

    new_scene.setBackground_Color((bg_color_r,bg_color_g,bg_color_b))

    cam_pos = numpy.array([cam_pos_x  * xyz_coord[0], cam_pos_y  * xyz_coord[1], cam_pos_z * xyz_coord[2]])
    cam_forward = numpy.array([cam_forward_x * xyz_coord[0], cam_forward_y * xyz_coord[1], cam_forward_z * xyz_coord[2]]) - cam_pos
    cam_up = numpy.array([cam_up_x * xyz_coord[0], cam_up_y * xyz_coord[1], cam_up_z * xyz_coord[2]])

    cam_forward = normalized(cam_forward)
    cam_up = normalized(cam_up - numpy.dot(cam_forward, cam_up) * cam_forward)

    for i in range(k_obj):
        color_r = int(inputs[index])
        index +=1
        color_g = int(inputs[index])
        index +=1
        color_b = int(inputs[index])
        index +=1
        color = (color_r, color_g, color_b)

        ka = float(inputs[index])
        index +=1
        kd = float(inputs[index])
        index +=1
        ks = float(inputs[index])
        index +=1
        phongN = float(inputs[index])
        index +=1

        kr = float(inputs[index])
        index +=1
        kt = float(inputs[index])
        index +=1
        refN = float(inputs[index])
        index +=1

        obj_select = inputs[index]
        index +=1

        pos_x = float(inputs[index])
        index +=1
        pos_y = float(inputs[index])
        index +=1
        pos_z = float(inputs[index])
        index +=1

        position = numpy.array([pos_x * xyz_coord[0], pos_y * xyz_coord[1], pos_z * xyz_coord[2]])

        if obj_select == '*':
            radius = float(inputs[index])
            index +=1

            new_scene.addSphere(position, radius, color, ka, kd, ks, phongN, kr, kt, refN)
        elif obj_select == '/':
            normal_x = float(inputs[index])
            index +=1
            normal_y = float(inputs[index])
            index +=1
            normal_z = float(inputs[index])
            index +=1

            normal = normalized([normal_x * xyz_coord[0], normal_y * xyz_coord[1], normal_z * xyz_coord[2]])

            new_scene.addPlane(position, normal, color, ka, kd, ks, phongN, kr, kt, refN)
        else:
            normal_x = float(inputs[index])
            index +=1
            normal_y = float(inputs[index])
            index +=1
            normal_z = float(inputs[index])
            index +=1

            normal = normalized([normal_x * xyz_coord[0], normal_y * xyz_coord[1], normal_z * xyz_coord[2]])

            new_scene.addPiso(position, normal, color, ka, kd, ks, phongN, kr, kt, refN)


    cAmb_r = int(inputs[index])
    index +=1
    cAmb_g = int(inputs[index])
    index +=1
    cAmb_b = int(inputs[index])
    index +=1

    new_scene.setAmbientLight((cAmb_r,cAmb_g,cAmb_b))

    k_pl = int(inputs[index])
    index +=1

    for i in range(k_pl):
        color_r = int(inputs[index])
        index +=1
        color_g = int(inputs[index])
        index +=1
        color_b = int(inputs[index])
        index +=1
        color = (color_r, color_g, color_b)

        pos_x = float(inputs[index])
        index +=1
        pos_y = float(inputs[index])
        index +=1
        pos_z = float(inputs[index])
        index +=1

        position = numpy.array([pos_x * xyz_coord[0], pos_y * xyz_coord[1], pos_z * xyz_coord[2]])

        new_scene.addPointLight(position, color)



    
    if (cam_forward[0] == 0 and cam_forward[1] == 0 and cam_forward[2] == 0) or (cam_up[0] == 0 and cam_up[1] == 0 and cam_up[2] == 0):
        print('cam_forward e cam_up não podem ser [0,0,0] ou paralelas')
    else: 
        print('gerando imagem...')
        render(res_horizontal, res_vertical, size_pixel,cam_dist, cam_pos, cam_forward, cam_up, new_scene, max_depth)