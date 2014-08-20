""" Mandelbrot Set example

Code from the Tentative Numpy Tutorial

url: http://wiki.scipy.org/Tentative_NumPy_Tutorial/Mandelbrot_Set_Example

"""

from numpy import *
import pylab


def mandelbrot(h, w, maxit=20):
    '''Returns an image of the Mandelbrot fractal of size (h,w).
    '''
    y,x = ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
    c = x+y*1j
    z = c
    divtime = maxit + zeros(z.shape, dtype=int)

    for i in xrange(maxit):
       z = z**2 + c
       diverge = z*conj(z) > 2**2            # who is diverging
       div_now = diverge & (divtime==maxit)  # who is diverging now
       divtime[div_now] = i                  # note when
       z[diverge] = 2                        # avoid diverging too much

    return divtime


if __name__ == '__main__':
    pylab.imshow(mandelbrot(400,400))
    pylab.show()
