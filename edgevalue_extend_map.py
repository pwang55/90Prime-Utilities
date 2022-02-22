'''

Usage:
    python edgevalue_extend_map.py optic_flat_asu1_filtermask_1500.fits


This code takes optic filter masks, calculate the center of each filters, 
create regions with different angles and label them with numbers, create a edge region map.
It doesn't matter what radius the given file is (but it has to be a filtermask file), this code always makes edge regions with radius = 1400~1500


'''
import numpy as np
from astropy.io import fits
import mydraw as my
import sys
from astropy.stats import sigma_clipped_stats

sep = 10    # separation in degree, has to be able to satisfy 360/sep = integar
if 360 % sep != 0:
    print('Use a separation that makes 360/separation = integar!')
    sys.exit()

r1 = 1400
r2 = 1500

nintervals = int(360 / sep)
file = sys.argv[1]

o = fits.open(file)
hdrs = []
hdrs.append(o[0].header)
for i in range(16):
    hdrs.append(o[i+1].header)


oms1, oms2, oms3, oms4, omsa = my.to_im(file)
omss = [oms1, oms2, oms3, oms4]

final_omss = []

for i in range(4):
    oms = omss[i]
    t= oms.copy()
    h = oms > 0.5
    # t[~h] = 0.0
    coord = np.array(np.nonzero(h)).T
    cx = (max(coord[:,0])+min(coord[:,0]))/2.0
    cy = (max(coord[:,1])+min(coord[:,1]))/2.0
    nx = t.shape[0]
    ny = t.shape[1]

    x=np.linspace(0, nx-1, nx, dtype=int)
    y=np.linspace(0, ny-1, ny, dtype=int)
    x,y = np.meshgrid(x,y)
    X=x.T
    Y=y.T

    hr = (((X-cx)**2+(Y-cy)**2) > r1 ** 2) & (((X-cx)**2+(Y-cy)**2) < r2 ** 2)
    hrout = (((X-cx)**2+(Y-cy)**2) > r2 ** 2)

    t[~hr] = 0.0

    all_sin = (Y - cy) / np.sqrt((X - cx) ** 2+(Y - cy) ** 2)

    for j in range(nintervals):
        ang1 = 10 * j
        ang2 = 10 * (j + 1)
        ave = (ang1 + ang2) / 2
        sin1 = np.sin(ang1 * np.pi/180)
        sin2 = np.sin(ang2 * np.pi/180)
        diff_x = X - cx
        if ave >= 0 and ave <= 90:
           ha = (all_sin >= sin1) & (all_sin <= sin2) & (diff_x >= 0)
        elif ave >= 90 and ave <= 180:
            ha = (all_sin >= sin2) & (all_sin <= sin1) & (diff_x <= 0)
        elif ave >= 180 and ave <= 270:
            ha = (all_sin >= sin2) & (all_sin <= sin1) & (diff_x <= 0)
        elif ave >= 270 and ave <= 360:
            ha = (all_sin >= sin1) & (all_sin <= sin2) & (diff_x >= 0)
        t[hr & ha] = j + 1
        t[hrout & ha] = -j - 1

    final_omss.append(t)

finalfile = my.to_file(final_omss[0], final_omss[1], final_omss[2], final_omss[3], o)

name_chars = file.split('filtermask')
finalname = name_chars[0] + 'edgeregionmap_{}.fits'.format(str(int(sep)))
finalfile.writeto(finalname, overwrite=True)

o.close()
