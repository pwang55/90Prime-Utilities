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
select o.objID, o.raMean, o.decMean, o.nDetections,
m.gMeanPSFMag, m.gMeanPSFMagErr, m.gMeanKronMag, m.gMeanKronMagErr, m.gQfPerfect, m.rMeanPSFMag, m.rMeanPSFMagErr, m.rMeanKronMag, m.rMeanKronMagErr, m.rQfPerfect,
m.iMeanPSFMag, m.iMeanPSFMagErr, m.iMeanKronMag, m.iMeanKronMagErr, m.iQfPerfect, m.zMeanPSFMag, m.zMeanPSFMagErr, m.zMeanKronMag, m.zMeanKronMagErr, m.zQfPerfect,
m.yMeanPSFMag, m.yMeanPSFMagErr, m.yMeanKronMag, m.yMeanKronMagErr, m.yQfPerfect, s.primaryDetection, s.gPSFMag, s.gPSFMagErr, s.gKronMag, s.gKronMagErr, s.rPSFMag,
s.rPSFMagErr, s.rKronMag, s.rKronMagErr, s.iPSFMag, s.iPSFMagErr, s.iKronMag, s.iKronMagErr, s.zPSFMag, s.zPSFMagErr, s.zKronMag, s.zKronMagErr,
s.yPSFMag, s.yPSFMagErr,
s.yKronMag, s.yKronMagErr, s.gpsfMajorFWHM, s.gpsfMinorFWHM, s.gpsfLikelihood, s.gpsfQf, s.gpsfQfPerfect, s.gmomentR1, s.gmomentRH, s.rpsfMajorFWHM, s.rpsfMinorFWHM,
s.rpsfLikelihood, s.rpsfQf, s.rpsfQfPerfect, s.rmomentR1, s.rmomentRH, s.ipsfMajorFWHM, s.ipsfMinorFWHM, s.ipsfLikelihood, s.ipsfQf, s.ipsfQfPerfect, s.imomentR1,
s.imomentRH, s.zpsfMajorFWHM, s.zpsfMinorFWHM, s.zpsfLikelihood, s.zpsfQf, s.zpsfQfPerfect, s.zmomentR1, s.zmomentRH,
s.ypsfMajorFWHM, s.ypsfMinorFWHM, s.ypsfLikelihood, s.ypsfQf, s.ypsfQfPerfect, s.ymomentR1, s.ymomentRH
from fGetNearbyObjEq(ra,dec,radius) nb
inner join ObjectThin o on o.objid=nb.objid
inner join MeanObject m on o.objid=m.objid and o.uniquePspsOBid=m.uniquePspsOBid
inner join StackObjectView s on o.objid=s.objid and s.primaryDetection=1 and o.uniquePspsOBid=s.uniquePspsOBid



"""
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



query="""select o.objID, o.raMean, o.decMean, o.nDetections,
m.gMeanPSFMag, m.gMeanPSFMagErr, m.gMeanKronMag, m.gMeanKronMagErr, m.gQfPerfect, m.rMeanPSFMag, m.rMeanPSFMagErr, m.rMeanKronMag, m.rMeanKronMagErr, m.rQfPerfect,
m.iMeanPSFMag, m.iMeanPSFMagErr, m.iMeanKronMag, m.iMeanKronMagErr, m.iQfPerfect, m.zMeanPSFMag, m.zMeanPSFMagErr, m.zMeanKronMag, m.zMeanKronMagErr, m.zQfPerfect,
m.yMeanPSFMag, m.yMeanPSFMagErr, m.yMeanKronMag, m.yMeanKronMagErr, m.yQfPerfect, s.primaryDetection, s.gPSFMag, s.gPSFMagErr, s.gKronMag, s.gKronMagErr, s.rPSFMag,
s.rPSFMagErr, s.rKronMag, s.rKronMagErr, s.iPSFMag, s.iPSFMagErr, s.iKronMag, s.iKronMagErr, s.zPSFMag, s.zPSFMagErr, s.zKronMag, s.zKronMagErr,
s.yPSFMag, s.yPSFMagErr,
s.yKronMag, s.yKronMagErr, s.gpsfMajorFWHM, s.gpsfMinorFWHM, s.gpsfLikelihood, s.gpsfQf, s.gpsfQfPerfect, s.gmomentR1, s.gmomentRH, s.rpsfMajorFWHM, s.rpsfMinorFWHM,
s.rpsfLikelihood, s.rpsfQf, s.rpsfQfPerfect, s.rmomentR1, s.rmomentRH, s.ipsfMajorFWHM, s.ipsfMinorFWHM, s.ipsfLikelihood, s.ipsfQf, s.ipsfQfPerfect, s.imomentR1,
s.imomentRH, s.zpsfMajorFWHM, s.zpsfMinorFWHM, s.zpsfLikelihood, s.zpsfQf, s.zpsfQfPerfect, s.zmomentR1, s.zmomentRH,
s.ypsfMajorFWHM, s.ypsfMinorFWHM, s.ypsfLikelihood, s.ypsfQf, s.ypsfQfPerfect, s.ymomentR1, s.ymomentRH
from fGetNearbyObjEq({},{},{}) nb
inner join ObjectThin o on o.objid=nb.objid
inner join MeanObject m on o.objid=m.objid and o.uniquePspsOBid=m.uniquePspsOBid
inner join StackObjectView s on o.objid=s.objid and s.primaryDetection=1 and o.uniquePspsOBid=s.uniquePspsOBid""".format(ra,dec,radius)

jobs = mastcasjobs.MastCasJobs(username='pwang55', password='4a552d', context=context)
results = jobs.quick(query,task_name='python cone search')
#tab = PC.fixcolnames(PC.ascii.read(results))

results_tab = Table(results, meta={'ra': ra,'dec': dec,'radius': radius})

ascii.write(results_tab, datapath+clustername+'_panstarrs_radec.csv',format='ecsv')



