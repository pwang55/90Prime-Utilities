"""
Usage:

    $ python grab_panstarrs.py [clustername] [ra] [dec] [radius(arcmins)]

Outputs:
    clustername_panstarrs_radec.txt

This code is intended to put in sub folder in scripts that needs this, or run directly in local folder.


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
from fGetNearbyObjEq({},{},{}) nb
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

sys.dont_write_bytecode=True
import PanstarrsCasjobfx as PC


context='PanSTARRS_DR2'

if len(sys.argv)!=5:
    print(__doc__)
    exit()


clustername = sys.argv[1]
ra = sys.argv[2]
dec = sys.argv[3]
radius = sys.argv[4]


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

results.write(clustername+'_panstarrs_radec.txt',format='ascii.ecsv')



