import numpy as np
from astropy.io import fits
from glob import glob
#import matplotlib.pyplot as plt
#from scipy.ndimage import gaussian_filter as gf
# test new mac git

def to_im(fname):
        '''
        > import mydraw as my
        > ims1, ims2, ims3, ims4, imsa = my.to_im('xxxx.fits')

        All returns will be 2d array that can then be drew with plt.imshow(ims1)...etc
        Only input that works are 90Prime mosaic images with 16 tiles.
        '''
        # global ims1, ims2, ims3, ims4, imsa

        f = fits.open(fname)
        nx = f[1].data.shape[0]
        ny = f[1].data.shape[1]
        
        ims1 = np.zeros((2*nx, 2*ny), dtype=float)
        ims2 = np.zeros((2*nx, 2*ny), dtype=float)
        ims3 = np.zeros((2*nx, 2*ny), dtype=float)
        ims4 = np.zeros((2*nx, 2*ny), dtype=float)

        imsa = np.zeros((4*nx, 4*ny), dtype=float)

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

        f1i = np.flip(f1,0)
        f2i = np.flip(np.flip(f2,0),1)
        f3i = f3
        f4i = np.flip(f4,1)

        f5i = np.flip(f5,0)
        f6i = np.flip(np.flip(f6,0),1)
        f7i = f7
        f8i = np.flip(f8,1)

        f9i = np.flip(f9,1)
        f10i = f10
        f11i = np.flip(np.flip(f11,0),1)
        f12i = np.flip(f12,0)

        f13i = np.flip(f13,1)
        f14i = f14
        f15i = np.flip(np.flip(f15,0),1)
        f16i = np.flip(f16,0)

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
        return ims1, ims2, ims3, ims4, imsa




