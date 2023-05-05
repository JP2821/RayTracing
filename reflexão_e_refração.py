import numpy
from normalização import normalized


def reflect(vec, normal):
    n = normalized(normal)
    return numpy.dot(vec, n) * n * -2 + vec

def refract(vec, normal, n):

    w = -vec

    if numpy.dot(w,normal)>0:   
        ndotw = numpy.dot(normal,w)

        delta = 1 - (1/(n*n)) *(1-ndotw*ndotw)

        if delta < 0:
            return -1
        else:
            t = - (1/n) * w - (numpy.sqrt(delta) - (1/n) * ndotw) * normal
            return t
    else:                         
        normal1 = -normal
        ndotw = numpy.dot(normal1,w)
        
        n1 = 1/n

        delta = 1 - (1/(n1*n1)) *(1-ndotw*ndotw)

        if(delta<0):
            return -1
        else:
            t =  - (1/n1) * w - (numpy.sqrt(delta)-(1/n1) * ndotw) * normal1
            return t