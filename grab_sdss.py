"""
Usage:

    In script folder:
    $ python grab_sdss.py [path] [clustername] [ra] [dec] [radius(arcmins)]

    In data folder:
    $ pytohn path_to_script/grab_sdss.py [clustername] [ra] [dec] [radius(arcmins)]

Output four files as ecsv file in data folder:
    clustername_star_sdss_radec.ecsv
    clustername_gal_sdss_radec.ecsv
    clustername_star_sdss_radec.csv     (For DS9 catalog tool to plot)
    clustername_gal_sdss_radec.csv      (For DS9 catalog tool to plot)


Stars Query:
    SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z, clean FROM fGetNearbyObjEq(ra, dec, radius) n, Star p WHERE n.objID=p.objID

Galaxies Query:
    SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z, clean FROM fGetNearbyObjEq(ra, dec, radius) n, Star p WHERE n.objID=p.objID


"""
from numpy import *
from SciServer import Authentication, CasJobs
from SciServer import Config
import urllib3
import pandas as pd
import sys
import os
from astropy.io import ascii
from astropy.table import Table

urllib3.disable_warnings()

token = '27d25960dc5f4f0aa838612a18897e23'
#Authentication.setToken(token)
Authentication.login('pwang55', '4a552d')
Config.CasJobsRESTUri = 'http://skyserver.sdss.org/CasJobs/RestApi'
context = 'DR16'

# SDSS query code will create anohter argv so argv number check number has to +1
# If path is given, there will be total 7 args, and the first arg split by / should have multiple length
if (len(sys.argv) == 7) and (len(sys.argv[1].split('/')) > 1):
    datapath = sys.argv[1]
    clustername = sys.argv[2]
    ra = sys.argv[3]
    dec = sys.argv[4]
    radius = sys.argv[5]

    # if path argument doesn't end in /, add it
    if datapath[-1:] != '/':
        datapath = datapath+'/'

elif len(sys.argv) == 6:
    datapath=''
    clustername = sys.argv[1]
    ra = sys.argv[2]
    dec = sys.argv[3]
    radius = sys.argv[4]

else:
    print(__doc__)
    exit()




# Query for stars with psfMag and extinctions
q_star = 'SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z, clean FROM fGetNearbyObjEq('+ra+','+dec+','+radius+') n, Star p WHERE n.objID=p.objID'

# Query for galaxy with modelMag and cmodelMag and extinctions
q_gal = 'SELECT p.ra, p.dec, p.modelMag_u, p.modelMagErr_u, p.modelMag_g, p.modelMagErr_g, p.modelMag_r, p.modelMagErr_r, p.modelMag_i, p.modelMagErr_i, p.modelMag_z, p.modelMagErr_z, p.cmodelMag_u, p.cmodelMagErr_u, p.cmodelMag_g, p.cmodelMagErr_g, p.cmodelMag_r, p.cmodelMagErr_r, p.cmodelMag_i, p.cmodelMagErr_i, p.cmodelMag_z, p.cmodelMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z, clean FROM fGetNearbyObjEq('+ra+','+dec+','+radius+') n, Galaxy p WHERE n.objID=p.objID'

star_data = CasJobs.executeQuery(q_star, context=context, format='pandas')
gal_data = CasJobs.executeQuery(q_gal, context=context, format='pandas')



star_tab = Table(star_data.values, names=star_data.columns, meta={'clustername': clustername, 'ra': ra, 'dec': dec, 'radius': radius})
gal_tab = Table(gal_data.values, names=gal_data.columns, meta={'clustername': clustername, 'ra': ra, 'dec': dec, 'radius': radius})

ascii.write(star_tab, datapath+clustername+'_star_sdss_radec.csv', format='ecsv')
ascii.write(gal_tab, datapath+clustername+'_gal_sdss_radec.csv', format='ecsv')

# ALso save files as csv so that ds9 catalog tools can use them
# ascii.write(star_tab, datapath+clustername+'_star_sdss_radec.csv', format='csv')
# ascii.write(gal_tab, datapath+clustername+'_gal_sdss_radec.csv', format='csv')


