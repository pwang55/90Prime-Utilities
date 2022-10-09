"""

Usage:
    Copy this code to working folder that has the optic files you want to mask, and do
    $ python making_mask.py optic_flat_asu1.fits [type/radius]

    Type can be "skymask" or radius (in which case it will be labeled "filtermask_radius")

    Typical radius I use:
    950     Skymask, central flat part
    1855    Whole filter
    1700    Whole filter, trim a bit
    1500    Even smaller cut to avoid edge regions

This code has to be run in the same folder as the optic files.

"""
from numpy import *
from astropy.io import fits
#from glob import glob
import sys
import mydraw as my

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit()

file0 = sys.argv[1]     # optic flat
type_or_radius = sys.argv[2]
op = fits.open(file0)

#fname = file0.replace('.fits','_skymask.fits')
#fname = file0.replace('.fits','_filtermask_1855.fits')
#fname = file0.replace('.fits','_filtermask_1500.fits')
#fname = file0.replace('.fits','_calibrationmask.fits')

#radius = 950    # sky, the central part of filter that are really flat
#radius = 1855   # whole filter
#radius = 1700  # whole filter, trim a bit of edge
#radius = 1500   # Even smaller cut to avoid edge region

if type_or_radius == 'skymask':
    fname = file0.replace('.fits','_skymask.fits')
    radius = 950
else:
    radius = int(type_or_radius)
    fname = file0.replace('.fits','_filtermask_{}.fits'.format(radius))


ims1, ims2, ims3, ims4, imsa = my.to_im(file0)

t1 = ims1.copy()
t2 = ims2.copy()
t3 = ims3.copy()
t4 = ims4.copy()

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
hduA.writeto(fname, overwrite=True)



op.close()


