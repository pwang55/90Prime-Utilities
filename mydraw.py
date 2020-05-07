from numpy import *
#import matplotlib.pyplot as plt
from astropy.io import fits
#from scipy.ndimage import gaussian_filter as gf
from glob import glob

def myimport_names():
        
        global file1, file2, file3, file4
        global op1, op2, op3, op4


        file1 = glob('ASU1_*compare.fits')
        file2 = glob('ASU2_*compare.fits')
        file3 = glob('ASU3_*compare.fits')
        file4 = glob('ASU4_*compare.fits')

#       op1 = fits.open('optic_flat_asu1_feb.fits')
#       op2 = fits.open('optic_flat_asu2_feb.fits')
#       op3 = fits.open('optic_flat_asu3_feb.fits')
#       op4 = fits.open('optic_flat_asu4_feb.fits')

#       opt_list = [op1,op2,op3,op4]
#       opt_out = []

#       for x in range(len(opt_list)):

#               nx = opt_list[x][1].data.shape[0]
#               ny = opt_list[x][1].data.shape[1]

#               oims1 = zeros((2*nx, 2*ny), dtype=float)
#               oims2 = zeros((2*nx, 2*ny), dtype=float)
#               oims3 = zeros((2*nx, 2*ny), dtype=float)
#               oims4 = zeros((2*nx, 2*ny), dtype=float)

#               oimsa = zeros((4*nx, 4*ny), dtype=float)




        op1 = 'optic_flat_asu1_feb.fits'
        op2 = 'optic_flat_asu2_feb.fits'
        op3 = 'optic_flat_asu3_feb.fits'
        op4 = 'optic_flat_asu4_feb.fits'


def to_im(fname='test.fits'):

        global ims1, ims2, ims3, ims4, imsa

        f = fits.open(fname)
        nx = f[1].data.shape[0]
        ny = f[1].data.shape[1]
        
        ims1 = zeros((2*nx, 2*ny), dtype=float)
        ims2 = zeros((2*nx, 2*ny), dtype=float)
        ims3 = zeros((2*nx, 2*ny), dtype=float)
        ims4 = zeros((2*nx, 2*ny), dtype=float)

        imsa = zeros((4*nx, 4*ny), dtype=float)

        f1 = f[1].data
        f2 = f[2].data
        f3 = f[3].data
        f4 = f[4].data
        f5 = f[5].data
        f6 = f[6].data
        f7 = f[7].data
        f8 = f[8].data
        f9 = f[9].data
        f10 = f[10].data
        f11 = f[11].data
        f12 = f[12].data
        f13 = f[13].data
        f14 = f[14].data
        f15 = f[15].data
        f16 = f[16].data

        f1i = flip(f1,0)
        f2i = flip(flip(f2,0),1)
        f3i = f3
        f4i = flip(f4,1)

        f5i = flip(f5,0)
        f6i = flip(flip(f6,0),1)
        f7i = f7
        f8i = flip(f8,1)

        f9i = flip(f9,1)
        f10i = f10
        f11i = flip(flip(f11,0),1)
        f12i = flip(f12,0)

        f13i = flip(f13,1)
        f14i = f14
        f15i = flip(flip(f15,0),1)
        f16i = flip(f16,0)

        ims1[nx:2*nx,:ny] = f1i
        ims1[nx:2*nx,ny:2*ny] = f2i
        ims1[:nx,:ny] = f3i
        ims1[:nx,ny:2*ny] = f4i

        ims2[nx:2*nx,:ny] = f5i
        ims2[nx:2*nx,ny:2*ny] = f6i
        ims2[:nx,:ny] = f7i
        ims2[:nx,ny:2*ny] = f8i

        ims3[nx:2*nx,:ny] = f12i
        ims3[nx:2*nx,ny:2*ny] = f11i
        ims3[:nx,:ny] = f10i
        ims3[:nx,ny:2*ny] = f9i

        ims4[nx:2*nx,:ny] = f16i
        ims4[nx:2*nx,ny:2*ny] = f15i
        ims4[:nx,:ny] = f14i
        ims4[:nx,ny:2*ny] = f13i

        imsa[:2*nx,2*ny:4*ny] = ims1
        imsa[:2*nx,:2*ny] = ims2
        imsa[2*nx:4*nx,2*ny:4*ny] = ims3
        imsa[2*nx:4*nx,:2*ny] = ims4

        f.close()

def myclose():

        op1.close()
        op2.close()
        op3.close()
        op4.close()

#       f.close()


