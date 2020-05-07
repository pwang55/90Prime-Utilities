"""
Usage:

    $ python grab_sdss.py ra dec radius(arcmins)

Output two files:
    star_sdss_radec.txt
    gal_sdss_radec.txt

Stars Query:
    SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq(ra,dec,radius) n, Star p WHERE n.objID=p.objID'

Galaxies Query:
    SELECT p.ra, p.dec, p.modelMag_u, p.modelMagErr_u, p.modelMag_g, p.modelMagErr_g, p.modelMag_r, p.modelMagErr_r, p.modelMag_i, p.modelMagErr_i, p.modelMag_z, p.modelMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq(ra,dec,radius) n, Galaxy p WHERE n.objID=p.objID'


"""
from numpy import *
from SciServer import Authentication, CasJobs
from SciServer import Config
import urllib3
import pandas as pd
import sys

urllib3.disable_warnings()

token = '27d25960dc5f4f0aa838612a18897e23'
#Authentication.setToken(token)
Authentication.login('pwang55', '4a552d')
Config.CasJobsRESTUri = 'http://skyserver.sdss.org/CasJobs/RestApi'

print(sys.argv)

if len(sys.argv)!=5:
    print(__doc__)
    exit()



ra = sys.argv[1]
dec = sys.argv[2]
radius = sys.argv[3]


# Query for stars with psfMag
q_star = 'SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq('+ra+','+dec+','+radius+') n, Star p WHERE n.objID=p.objID'

# Query for galaxy with modelMag
q_gal = 'SELECT p.ra, p.dec, p.modelMag_u, p.modelMagErr_u, p.modelMag_g, p.modelMagErr_g, p.modelMag_r, p.modelMagErr_r, p.modelMag_i, p.modelMagErr_i, p.modelMag_z, p.modelMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq('+ra+','+dec+','+radius+') n, Galaxy p WHERE n.objID=p.objID'

star_data = CasJobs.executeQuery(q_star, context='DR16', format='pandas')
gal_data = CasJobs.executeQuery(q_gal, context='DR16', format='pandas')

savetxt('star_sdss_radec.txt', star_data.values, fmt = '%f', delimiter='\t')
savetxt('gal_sdss_radec.txt', gal_data.values, fmt = '%f', delimiter='\t')




