"""

This file was a quick code to plot photo-z v.s. spec-z in the folder:

~/90PrimeData/testing/photometry/plots

After running lazy_script.sh or eazy_lazy.sh, all .zall files will be copied to this folder. Then with this code in this folder, run this code without any argument.
Any setting changes need to be done in the code.


"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
import sys
from glob import glob
from astropy.coordinates import SkyCoord

template = 'CWW+Kinney'

z_col = 'z_m2'
# z_col = 'z_p'
ww = 15
hh = 9
elinewidth = 0.4
alpha = 0.6
msize = 8
lim_l = 0.2
lim_u = 0.8
bottom_lim = 0.2

rejection_sig = 2.2
rejection_radius = 15   # rejection radius in arcmin
rejection_nfilt = 8
allwise_nfilt = 1       # minimum number of filters for allwise
calibration_nfilt = 3   # minimum number of filters for panstarrs
rejection_odd = 0.8

colors = {'abell1576': 'dimgray', 'abell611': 'salmon', 'abell370': 'orange', 'zwicky1953': 'mediumslateblue', \
            'macs0717': 'steelblue', 'macs1115': 'darkturquoise', 'macs1149': 'tan', 'rxj1532': 'violet'}

actual_names = {'abell1576': 'ABELL 1576', \
                'abell370': 'ABELL 370', \
                'abell611': 'ABELL 611', \
                'macs1115': 'MACS J1115.2+5320', \
                'macs1149': 'MACS J1149.5+2223', \
                'rxj1532': 'RXJ 1532.9+3021', \
                'zwicky1953': 'ZwCL 1953', \
                'macs0329': 'MACS J0329-0211', \
                'macs0717': 'MACS J0717.5+3745'}

# sdss = glob('*sdss*zout')
# panstarrs = glob('*panstarrs*zout')

sdss = glob('*all_zspecs_sdss.zall')
panstarrs = glob('*all_zspecs_panstarrs.zall')


ra_Dict = {'abell1576': 189.099053938, \
            'abell370': 39.99219214235, \
            'abell611': 120.25462344, \
            'macs1115': 169.0099466108, \
            'macs1149': 177.3902293722, \
            'rxj1532': 233.2581131864, \
            'zwicky1953': 132.5585404261, \
            'macs0329': 52.4258443441, \
            'macs0717': 109.3697495889}

dec_Dict = {'abell1576': 63.18212102636, \
            'abell370': -1.598052185306, \
            'abell611': 36.06793197071, \
            'macs1115': 1.488905550734, \
            'macs1149': 22.37322858283, \
            'rxj1532': 30.33350852445, \
            'zwicky1953': 36.09350845779, \
            'macs0329': -2.195521179422, \
            'macs0717': 37.74853445641}

zs1 = []
zp1 = []
zs2 = []
zp2 = []
zp1sig = []
zp2sig = []
ra1 = []
ra2 = []
dec1 = []
dec2 = []


for i in range(len(sdss)):
    s = ascii.read(sdss[i])
    p = ascii.read(panstarrs[i])
    sra = s['ra']
    sdec = s['dec']
    pra = p['ra']
    pdec = p['dec']
    scoord = SkyCoord(sra, sdec, unit='deg')
    pcoord = SkyCoord(pra, pdec, unit='deg')

    sclustername = sdss[i].split('_')[0]
    pclustername = panstarrs[i].split('_')[0]

    sclustercoord = SkyCoord(ra_Dict[sclustername], dec_Dict[sclustername], unit='deg')
    pclustercoord = SkyCoord(ra_Dict[pclustername], dec_Dict[pclustername], unit='deg')
    szs = s['z_spec']
    pzs = p['z_spec']
    snfilt = s['nfilt']
    pnfilt = p['nfilt']
    sodd = s['odds']
    podd = p['odds']
    szp = s[z_col]
    pzp = p[z_col]
    hs = (szs > 0.25) & (szs < 0.65) & (szp > 0) & (scoord.separation(sclustercoord).arcmin < rejection_radius) & (snfilt >= rejection_nfilt) & (sodd > rejection_odd) \
        & (s['nfilts_narrowband'] >= rejection_nfilt)  & (s['nfilts_allwise'] >= allwise_nfilt) & (s['nfilts_calibration'] >= calibration_nfilt)
    hp = (pzs > 0.25) & (pzs < 0.65) & (pzp > 0) & (pcoord.separation(pclustercoord).arcmin < rejection_radius) & (pnfilt >= rejection_nfilt) & (podd > rejection_odd) \
        & (p['nfilts_narrowband'] >= rejection_nfilt)  & (p['nfilts_allwise'] >= allwise_nfilt) & (p['nfilts_calibration'] >= calibration_nfilt)
    sigs = (s[hs]['u68'] - s[hs]['l68']) / 2 / (1 + szp[hs])
    sigp = (p[hp]['u68'] - p[hp]['l68']) / 2 / (1 + pzp[hp])
    hs_reject = (sigs < rejection_sig)
    hp_reject = (sigp < rejection_sig)

    zs1.extend(list(szs[hs][hs_reject]))
    zp1.extend(list(szp[hs][hs_reject]))
    zs2.extend(list(pzs[hp][hp_reject]))
    zp2.extend(list(pzp[hp][hp_reject]))
    zp1sig.extend(list(sigs[hs_reject]))
    zp2sig.extend(list(sigp[hp_reject]))
    # c1s.extend(scoord[hs][hs_reject])
    # c2s.extend(pcoord[hp][hp_reject])
    ra1.extend(sra[hs][hs_reject])
    ra2.extend(pra[hp][hp_reject])
    dec1.extend(sdec[hs][hs_reject])
    dec2.extend(pdec[hp][hp_reject])




zs1 = np.array(zs1)
zp1 = np.array(zp1)
zs2 = np.array(zs2)
zp2 = np.array(zp2)
diff1 = zp1 - zs1
diff2 = zp2 - zs2
rms_sdss = np.std(diff1 / (1 + zs1))
rms_panstarrs = np.std(diff2 / (1 + zs2))
nmad_sdss = 1.48 * np.median(np.abs((diff1 - np.median(diff1)) / (1 + zs1)))
nmad_panstarrs = 1.48 * np.median(np.abs((diff2 - np.median(diff2)) / (1 + zs2)))
# TEMP
# nmad_sdss = 1.48 * np.median(np.abs((diff1) / (1 + zs1)))
# nmad_panstarrs = 1.48 * np.median(np.abs((diff2) / (1 + zs2)))


fig, axs=plt.subplots(2, 2, figsize=(ww, hh), gridspec_kw={'height_ratios': [3, 1]})
axs[0, 0].set_xlim(lim_l, lim_u)
axs[0, 1].set_xlim(lim_l, lim_u)
axs[0, 0].set_ylim(lim_l, lim_u)
axs[0, 1].set_ylim(lim_l, lim_u)
axs[0, 0].grid()
axs[0, 1].grid()
axs[0, 0].plot([0, 1], [0, 1], '-', alpha=0.7, color='limegreen')
axs[0, 1].plot([0, 1], [0, 1], '-', alpha=0.7, color='limegreen')
axs[0, 0].plot([0.,1],[0.05,1.1],':',alpha=0.5,color='silver',label=r'$\Delta z/(1+z_s)=0.05$')
axs[0, 0].plot([0.,1],[-0.05,0.9],':',alpha=0.5,color='silver')
axs[0, 1].plot([0.,1],[0.05,1.1],':',alpha=0.5,color='silver',label=r'$\Delta z/(1+z_s)=0.05$')
axs[0, 1].plot([0.,1],[-0.05,0.9],':',alpha=0.5,color='silver')
axs[0, 0].plot([0.,1],[0.03,1.06],'-.',alpha=0.5,color='gray',label=r'$\Delta z/(1+z_s)=0.03$')
axs[0, 0].plot([0.,1],[-0.03,0.94],'-.',alpha=0.5,color='gray')
axs[0, 1].plot([0.,1],[0.03,1.06],'-.',alpha=0.5,color='gray',label=r'$\Delta z/(1+z_s)=0.03$')
axs[0, 1].plot([0.,1],[-0.03,0.94],'-.',alpha=0.5,color='gray')
axs[0, 0].set_title(r'Calibrated with SDSS, RMS={:.4f}, $\sigma_{{NMAD}}=${:.4f}'.format(rms_sdss, nmad_sdss))
axs[0, 1].set_title(r'Calibrated with PanSTARRS, RMS={:.4f}, $\sigma_{{NMAD}}=${:.4f}'.format(rms_panstarrs, nmad_panstarrs))
axs[1, 0].set_xlabel('Spec-Z')
axs[1, 1].set_xlabel('Spec-Z')
axs[0, 0].set_ylabel('Photo-Z')
axs[1, 0].set_ylabel(r'$\Delta z/(1+z_s)$')
axs[0, 0].legend()
axs[0, 1].legend()
axs[1, 0].set_xlim(lim_l, lim_u)
axs[1, 1].set_xlim(lim_l, lim_u)
axs[1, 0].set_ylim(-bottom_lim, bottom_lim)
axs[1, 1].set_ylim(-bottom_lim, bottom_lim)
axs[1, 0].grid()
axs[1, 1].grid()
axs[1, 0].plot([0, 1], [0, 0], '-', color='gray')
axs[1, 1].plot([0, 1], [0, 0], '-', color='gray')
# TEMP
# fig.suptitle(r"Template: {},  Within {}' of cluster,  $n_{{narrowband}}\geq${}, $n_{{SDSS/PanSTARRS}}\geq${}, $n_{{ALLWISE}}\geq${}, $\sigma_{{z_p}}/(1+z_p)$<{}, $z_{{EAZY}}$={}".format(template, \
#                 rejection_radius, rejection_nfilt, calibration_nfilt, allwise_nfilt, rejection_sig, z_col))
# fig.suptitle(r"Template: {},  Within {}' of cluster,  $n_{{narrowband}}\geq${}, $n_{{SDSS/PanSTARRS}}\geq${}, $n_{{ALLWISE}}\geq${}, $\sigma_{{z_p}}/(1+z_p)$<{}".format(template, \
#                 rejection_radius, rejection_nfilt, calibration_nfilt, allwise_nfilt, rejection_sig))
fig.suptitle(r"Template: {},  Within {}' of cluster,  $n_{{narrowband}}\geq${}, $n_{{SDSS/PanSTARRS}}\geq${}, $n_{{ALLWISE}}\geq${}".format(template, \
                rejection_radius, rejection_nfilt, calibration_nfilt, allwise_nfilt))
fig.subplots_adjust(top=0.8)
fig.tight_layout()


# If not separating clusters, use this
# axs[0, 0].errorbar(zs1, zp1, zp1sig, fmt='.', c='teal', ms=8, ecolor='lightblue')
# axs[0, 1].errorbar(zs2, zp2, zp2sig, fmt='.', c='tomato', ms=8, ecolor='peachpuff')
# axs[1, 0].errorbar(zs1, (zp1 - zs1) / (1 + zs1), zp1sig, fmt='.', c='teal', ms=8, ecolor='lightblue')
# axs[1, 1].errorbar(zs2, (zp2 - zs2) / (1 + zs2), zp2sig, fmt='.', c='tomato', ms=8, ecolor='peachpuff')

# Use this if you want to separate clusters so that they have different colors
for i in range(len(sdss)):
    s = ascii.read(sdss[i])
    p = ascii.read(panstarrs[i])
    szs = s['z_spec']
    pzs = p['z_spec']
    snfilt = s['nfilt']
    pnfilt = p['nfilt']
    szp = s[z_col]
    pzp = p[z_col]
    sodd = s['odds']
    podd = p['odds']
    sra = s['ra']
    sdec = s['dec']
    pra = p['ra']
    pdec = p['dec']
    scoord = SkyCoord(sra, sdec, unit='deg')
    pcoord = SkyCoord(pra, pdec, unit='deg')
    sclustername = sdss[i].split('_')[0]
    pclustername = panstarrs[i].split('_')[0]
    sclustercoord = SkyCoord(ra_Dict[sclustername], dec_Dict[sclustername], unit='deg')
    pclustercoord = SkyCoord(ra_Dict[pclustername], dec_Dict[pclustername], unit='deg')

    hs = (szs >= 0) & (szp >= 0) & (scoord.separation(sclustercoord).arcmin < rejection_radius) & (snfilt >= rejection_nfilt) & (sodd > rejection_odd) \
        & (s['nfilts_narrowband'] >= rejection_nfilt)  & (s['nfilts_allwise'] >= allwise_nfilt) & (s['nfilts_calibration'] >= calibration_nfilt)
    hp = (pzs >= 0) & (pzp >= 0) & (pcoord.separation(pclustercoord).arcmin < rejection_radius) & (pnfilt >= rejection_nfilt) & (podd > rejection_odd) \
        & (p['nfilts_narrowband'] >= rejection_nfilt)  & (p['nfilts_allwise'] >= allwise_nfilt) & (p['nfilts_calibration'] >= calibration_nfilt)

    hs_reject = ((s[hs]['u68'] - s[hs]['l68']) / 2 / (1 + szp[hs]) < rejection_sig)
    hp_reject = ((p[hp]['u68'] - p[hp]['l68']) / 2 / (1 + pzp[hp]) < rejection_sig)
    s1sig = [szp[hs][hs_reject] - s[hs]['l68'][hs_reject], s[hs]['u68'][hs_reject] - szp[hs][hs_reject]]
    p1sig = [pzp[hp][hp_reject] - p[hp]['l68'][hp_reject], p[hp]['u68'][hp_reject] - pzp[hp][hp_reject]]

    axs[0, 0].errorbar(szs[hs][hs_reject], szp[hs][hs_reject], s1sig, fmt='.', ms=msize, label=actual_names[sdss[i].split('_')[0]], \
        color=colors[sclustername], alpha=alpha, elinewidth=elinewidth)
    axs[0, 1].errorbar(pzs[hp][hp_reject], pzp[hp][hp_reject], p1sig, fmt='.', ms=msize, label=actual_names[panstarrs[i].split('_')[0]], \
        color=colors[pclustername], alpha=alpha, elinewidth=elinewidth)
    axs[1, 0].errorbar(szs[hs][hs_reject], (szp[hs][hs_reject] - szs[hs][hs_reject]) / (1 + szs[hs][hs_reject]), s1sig, \
        color=colors[sclustername], fmt='.', ms=msize, alpha=alpha, elinewidth=elinewidth)
    axs[1, 1].errorbar(pzs[hp][hp_reject], (pzp[hp][hp_reject] - pzs[hp][hp_reject]) / (1 + pzs[hp][hp_reject]), p1sig, \
        color=colors[pclustername], fmt='.', ms=msize, alpha=alpha, elinewidth=elinewidth)
    axs[0, 0].legend()
    axs[0, 1].legend()


plt.show()

