import numpy

def normalized(vec):
    n = numpy.linalg.norm(vec)
    if n ==0:
        return vec
    else:
        return vec / n