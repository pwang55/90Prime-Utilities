"""
Usage:

    In script folder:
    $ python grab_panstarrs.py [path] [clustername] [ra] [dec] [radius(arcmins)]

    In data folder:
    $ pytohn path_to_script/grab_panstarrs.py [clustername] [ra] [dec] [radius(arcmins)]

Outputs:
    clustername_panstarrs_radec.ecsv

Output files will be saved in data directory.

Query:
select o.raMean, o.decMean, o.raStack, o.decStack, o.nDetections,
m.gMeanPSFMag, m.gMeanPSFMagErr, m.gMeanKronMag, m.gMeanKronMagErr,
m.rMeanPSFMag, m.rMeanPSFMagErr, m.rMeanKronMag, m.rMeanKronMagErr,
m.iMeanPSFMag, m.iMeanPSFMagErr, m.iMeanKronMag, m.iMeanKronMagErr,
m.zMeanPSFMag, m.zMeanPSFMagErr, m.zMeanKronMag, m.zMeanKronMagErr,
m.yMeanPSFMag, m.yMeanPSFMagErr, m.yMeanKronMag, m.yMeanKronMagErr,
s.gPSFMag, s.gPSFMagErr, s.gKronMag, s.gKronMagErr, 
s.rPSFMag, s.rPSFMagErr, s.rKronMag, s.rKronMagErr, 
s.iPSFMag, s.iPSFMagErr, s.iKronMag, s.iKronMagErr, 
s.zPSFMag, s.zPSFMagErr, s.zKronMag, s.zKronMagErr,
s.yPSFMag, s.yPSFMagErr, s.yKronMag, s.yKronMagErr, 
s.gpsfMajorFWHM, s.gpsfMinorFWHM, s.gpsfLikelihood, 
s.rpsfMajorFWHM, s.rpsfMinorFWHM, s.rpsfLikelihood, 
s.ipsfMajorFWHM, s.ipsfMinorFWHM, s.ipsfLikelihood,
s.zpsfMajorFWHM, s.zpsfMinorFWHM, s.zpsfLikelihood,
s.ypsfMajorFWHM, s.ypsfMinorFWHM, s.ypsfLikelihood,
psc.ps_score, o.qualityFlag, o.objinfoFlag, s.primaryDetection, 
m.gFlags, s.ginfoFlag, s.ginfoFlag2, s.ginfoFlag3,
m.rFlags, s.rinfoFlag, s.rinfoFlag2, s.rinfoFlag3,
m.iFlags, s.iinfoFlag, s.iinfoFlag2, s.iinfoFlag3,
m.zFlags, s.zinfoFlag, s.zinfoFlag2, s.zinfoFlag3,
m.yFlags, s.yinfoFlag, s.yinfoFlag2, s.yinfoFlag3
from fGetNearbyObjEq(ra, dec, radius) nb
join ObjectThin o on o.objid=nb.objid
join MeanObject m on o.objid=m.objid and o.uniquePspsOBid=m.uniquePspsOBid
join StackObjectView s on o.objid=s.objid and s.primaryDetection=1 and o.uniquePspsOBid=s.uniquePspsOBid
join HLSP_PS1_PSC.pointsource_scores psc on psc.objid=o.objid



"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from numpy import *
from astropy.io import ascii
from astropy.table import Table
import json
import sys
import os
import re
import mastcasjobs
import subprocess


context='PanSTARRS_DR2'

sys.dont_write_bytecode=True
import PanstarrsCasjobfx as PC

# If path is given, there will be total 6 args, and the first arg split by / should have multiple length
if (len(sys.argv) == 6) and (len(sys.argv[1].split('/')) > 1):
    datapath = sys.argv[1]
    clustername = sys.argv[2]
    ra = sys.argv[3]
    dec = sys.argv[4]
    radius = sys.argv[5]

    # if path argument doesn't end in /, add it
    if datapath[-1:] != '/':
        datapath = datapath+'/'

elif len(sys.argv) == 5:
    datapath=''
    clustername = sys.argv[1]
    ra = sys.argv[2]
    dec = sys.argv[3]
    radius = sys.argv[4]

else:
    print(__doc__)
    exit()



query="""select o.raMean, o.decMean, o.nDetections,
m.gMeanPSFMag, m.gMeanPSFMagErr, m.gMeanKronMag, m.gMeanKronMagErr,
m.rMeanPSFMag, m.rMeanPSFMagErr, m.rMeanKronMag, m.rMeanKronMagErr,
m.iMeanPSFMag, m.iMeanPSFMagErr, m.iMeanKronMag, m.iMeanKronMagErr,
m.zMeanPSFMag, m.zMeanPSFMagErr, m.zMeanKronMag, m.zMeanKronMagErr,
m.yMeanPSFMag, m.yMeanPSFMagErr, m.yMeanKronMag, m.yMeanKronMagErr,
s.gPSFMag, s.gPSFMagErr, s.gKronMag, s.gKronMagErr, 
s.rPSFMag, s.rPSFMagErr, s.rKronMag, s.rKronMagErr, 
s.iPSFMag, s.iPSFMagErr, s.iKronMag, s.iKronMagErr, 
s.zPSFMag, s.zPSFMagErr, s.zKronMag, s.zKronMagErr,
s.yPSFMag, s.yPSFMagErr, s.yKronMag, s.yKronMagErr, 
s.gpsfMajorFWHM, s.gpsfMinorFWHM, s.gpsfLikelihood, 
s.rpsfMajorFWHM, s.rpsfMinorFWHM, s.rpsfLikelihood, 
s.ipsfMajorFWHM, s.ipsfMinorFWHM, s.ipsfLikelihood,
s.zpsfMajorFWHM, s.zpsfMinorFWHM, s.zpsfLikelihood,
s.ypsfMajorFWHM, s.ypsfMinorFWHM, s.ypsfLikelihood,
psc.ps_score, o.qualityFlag, o.objinfoFlag, s.primaryDetection, 
m.gFlags, s.ginfoFlag, s.ginfoFlag2, s.ginfoFlag3,
m.rFlags, s.rinfoFlag, s.rinfoFlag2, s.rinfoFlag3,
m.iFlags, s.iinfoFlag, s.iinfoFlag2, s.iinfoFlag3,
m.zFlags, s.zinfoFlag, s.zinfoFlag2, s.zinfoFlag3,
m.yFlags, s.yinfoFlag, s.yinfoFlag2, s.yinfoFlag3
from fGetNearbyObjEq({},{},{}) nb
join ObjectThin o on o.objid=nb.objid
join MeanObject m on o.objid=m.objid and o.uniquePspsOBid=m.uniquePspsOBid
join StackObjectView s on o.objid=s.objid and s.primaryDetection=1 and o.uniquePspsOBid=s.uniquePspsOBid
join HLSP_PS1_PSC.pointsource_scores psc on psc.objid=o.objid""".format(ra,dec,radius)

jobs = mastcasjobs.MastCasJobs(username='pwang55', password='4a552d', context=context)
results = jobs.quick(query,task_name='python cone search')
#tab = PC.fixcolnames(PC.ascii.read(results))

results_tab = Table(results, meta={'clustername': clustername, 'ra': ra,'dec': dec,'radius': radius})

# # Convert all -999 entry to -99 for easier table handling in other scripts
# for c in range(len(results_tab.colnames)):
#     colname = results_tab.colnames[c]
#     h = results_tab[colname] == -999
#     results_tab[colname][h] = -99.0


ascii.write(results_tab, datapath+clustername+'_panstarrs_radec.csv',format='ecsv', overwrite=True)



