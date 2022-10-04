#!/bin/env
from utils import *
import numpy as np

HPBW_theta0 = deg2rad(5.0)
mm = 1e-3
cm = 1e-2

def gauss2D(r, L, HPBW_theta=HPBW_theta0):
    theta = np.arctan(r/L)
    return np.exp( -4.*np.log(2.) * (theta/HPBW_theta)**2. )

def gauss2DXY(x, y, L, HPBW_theta=HPBW_theta0):
    return gauss2D(np.sqrt(x**2.+y**2.), L, HPBW_theta)

def scan2Dgauss(
        x_min = -50.*mm, x_max=50.*mm, 
        y_min = -50.*mm, y_max=50.*mm,
        r_min = 0., r_max = 50.*mm, 
        dx = 1.*mm, dy = 1.*mm,
        L = 100.*mm, HPBW_theta=HPBW_theta0,
        verbose = 0
        ):
    x_list = np.arange(x_min, x_max+dx, dx)
    y_list = np.arange(y_min, y_max+dy, dy)
    x_2Dlist, y_2Dlist = np.meshgrid(x_list, y_list)
    x_2Dlist = x_2Dlist.ravel()
    y_2Dlist = y_2Dlist.ravel()
    r2_2Dlist = x_2Dlist ** 2. + y_2Dlist ** 2.
    r2_min = r_min ** 2.
    r2_max = r_max ** 2.
    if verbose >= 0:
        print('x', x_2Dlist.shape, x_2Dlist)
        print('y', y_2Dlist.shape, y_2Dlist)
        print('r**2', r2_2Dlist.shape, r2_2Dlist)
        pass

    in_range = (r2_2Dlist >= r2_min) & (r2_2Dlist <= r2_max)
    x_2Dlist = x_2Dlist[in_range]
    y_2Dlist = y_2Dlist[in_range]

    z_2Dlist = gauss2DXY(x_2Dlist, y_2Dlist, L, HPBW_theta)
    if verbose >= 0:
        print('z', z_2Dlist.shape, z_2Dlist)
        pass

    return x_2Dlist, y_2Dlist, z_2Dlist

def integral2Dgauss(
        x_min = -50.*mm, x_max=50.*mm, 
        y_min = -50.*mm, y_max=50.*mm,
        r_min = 0., r_max = 50.*mm, 
        dx = 1.*mm, dy = 1.*mm,
        L = 100.*mm, HPBW_theta=HPBW_theta0,
        verbose = 0
    ):
    x, y, z = scan2Dgauss(
            x_min, x_max, y_min, y_max, r_min, r_max,
            dx, dy, L, HPBW_theta,
            verbose = verbose
            )
    return np.sum(z)*dx*dy

if __name__ == '__main__':
    scan2Dgauss()
    pass



