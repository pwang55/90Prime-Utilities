"""

Usage:
    Copy this code to working folder that has the optic files you want to mask, and do
    $ python making_mask.py optic_flat_asu1.fits type

    type can be "skymask" or "filtermask".

filtermask is the mask of whole filter, radius=1855; skymask is the central flat part of the filter, radius=950.
This code has to be run in the same folder as the optic files.

"""
from numpy import *
from astropy.io import fits
#from glob import glob
import sys
sys.dont_write_bytecode=True
import mydraw as my


if len(sys.argv)==1:
    print(__doc__)
    exit()



file0 = sys.argv[1]     # optic flat
masktype = sys.argv[2]  # mask type
op = fits.open(file0)



if masktype == 'skymask':
    fname = file0.replace('.fits','_skymask.fits')
    radius = 950
elif masktype == 'filtermask':
    fname = file0.replace('.fits','_filtermask.fits')
    radius = 1855



my.to_im(file0)

t1 = my.ims1.copy()
t2 = my.ims2.copy()
t3 = my.ims3.copy()
t4 = my.ims4.copy()

tlist = [t1, t2, t3, t4]

hlist = []

for i in range(4):
    t = tlist[i]
    t2 = t.copy()
    h = t > 0.5
#       h = t > 0.2
    t[~h] = 0
    coord = array(nonzero(h)).T
    cx = (max(coord[:,0])+min(coord[:,0]))/2.0
    cy = (max(coord[:,1])+min(coord[:,1]))/2.0
    nx = t.shape[0]
    ny = t.shape[1]

    x=linspace(0, nx-1, nx, dtype=int)
    y=linspace(0, ny-1, ny, dtype=int)
    x,y = meshgrid(x,y)
    X=x.T
    Y=y.T
    hr = ((X-cx)**2+(Y-cy)**2) < radius**2
    t2[~hr]=0

    if i < 2:
        ti1 = t2[nx//2:nx,:ny//2]
        ti2 = t2[nx//2:nx,ny//2:ny]
        ti3 = t2[:nx//2,:ny//2]
        ti4 = t2[:nx//2,ny//2:ny]

        ti1 = flip(ti1, 0)
        ti2 = flip(flip(ti2, 0), 1)
        ti4 = flip(ti4, 1)
    else:
        ti4 = t2[nx//2:nx,:ny//2]
        ti3 = t2[nx//2:nx,ny//2:ny]
        ti2 = t2[:nx//2,:ny//2]
        ti1 = t2[:nx//2,ny//2:ny]

        ti1 = flip(ti1, 1)      
        ti3 = flip(flip(ti3, 0), 1)
        ti4 = flip(ti4, 0)

    tilist = [ti1, ti2, ti3, ti4]
    for j in range(4):
        hduI = fits.ImageHDU()
        hduI.data = tilist[j]           
        hduI.header = op[i*4+j+1].header
        hduI.header['BZERO']=0.0
        hlist.append(hduI)


hdu0 = fits.PrimaryHDU()
hdu0.header = op[0].header
hlist.insert(0,hdu0)
hduA = fits.HDUList(hlist)
hduA.writeto(fname)



op.close()


