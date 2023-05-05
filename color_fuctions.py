
def colorMul(color1, color2):
    r1 = color1[0]
    g1 = color1[1]
    b1 = color1[2]
    
    r2 = color2[0]
    g2 = color2[1]
    b2 = color2[2]

    return (r1 * r2, g1 * g2, b1 * b2)


def colorScale(color, f):
    return (color[0] * f, color[1] * f, color[2] * f)


def colorSum(color1, color2):
    r1 = color1[0]
    g1 = color1[1]
    b1 = color1[2]
    
    r2 = color2[0]
    g2 = color2[1]
    b2 = color2[2]

    return (r1+r2, g1+g2, b1+b2)

def colorNormalize(color):
    return (float(color[0]) / 255.0, float(color[1]) / 255.0, float(color[2]) / 255.0)


def colorDenormalize(color):
    f = max(1,*color)
    return (int(color[0] * 255.0/f), int(color[1] * 255.0/f), int(color[2] * 255.0/f))