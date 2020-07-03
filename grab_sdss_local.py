"""
Usage:

    In data folder, copy the script to here, then
    $ python grab_sdss_local.py [clustername] [ra] [dec] [radius(arcmins)]

Output four files as ecsv file in data folder:
    clustername_star_sdss_radec.ecsv
    clustername_gal_sdss_radec.ecsv
    clustername_star_sdss_radec.csv     (For DS9 catalog tool to plot)
    clustername_gal_sdss_radec.csv      (For DS9 catalog tool to plot)

The output files will be saved at the same directory as the script.

Stars Query:
    SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq(ra,dec,radius) n, Star p WHERE n.objID=p.objID'

Galaxies Query:
    SELECT p.ra, p.dec, p.cmodelMag_u, p.cmodelMagErr_u, p.cmodelMag_g, p.cmodelMagErr_g, p.cmodelMag_r, p.cmodelMagErr_r, p.cmodelMag_i, p.cmodelMagErr_i, p.cmodelMag_z, p.cmodelMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq(ra,dec,radius) n, Galaxy p WHERE n.objID=p.objID'


"""
from numpy import *
from SciServer import Authentication, CasJobs
from SciServer import Config
import urllib3
import pandas as pd
import sys
from astropy.io import ascii
from astropy.table import Table

urllib3.disable_warnings()

token = '27d25960dc5f4f0aa838612a18897e23'
#Authentication.setToken(token)
Authentication.login('pwang55', '4a552d')
Config.CasJobsRESTUri = 'http://skyserver.sdss.org/CasJobs/RestApi'
context = 'DR16'

# SDSS query code will create anohter argv so argv number check number has to +1
if len(sys.argv)!=6:
    print(__doc__)
    exit()


clustername = sys.argv[1]
ra = sys.argv[2]
dec = sys.argv[3]
radius = sys.argv[4]


# Query for stars with psfMag
q_star = 'SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq('+ra+','+dec+','+radius+') n, Star p WHERE n.objID=p.objID'

# Query for galaxy with cmodelMag
q_gal = 'SELECT p.ra, p.dec, p.cmodelMag_u, p.cmodelMagErr_u, p.cmodelMag_g, p.cmodelMagErr_g, p.cmodelMag_r, p.cmodelMagErr_r, p.cmodelMag_i, p.cmodelMagErr_i, p.cmodelMag_z, p.cmodelMagErr_z, extinction_u, extinction_g,extinction_r, extinction_i, extinction_z FROM fGetNearbyObjEq('+ra+','+dec+','+radius+') n, Galaxy p WHERE n.objID=p.objID'

star_data = CasJobs.executeQuery(q_star, context=context, format='pandas')
gal_data = CasJobs.executeQuery(q_gal, context=context, format='pandas')


star_tab = Table(star_data.values, names=star_data.columns, meta={'clustername': clustername, 'ra': ra, 'dec': dec, 'radius': radius})
gal_tab = Table(gal_data.values, names=gal_data.columns, meta={'clustername': clustername, 'ra': ra, 'dec': dec, 'radius': radius})

ascii.write(star_tab, clustername+'_star_sdss_radec.ecsv', format='ecsv')
ascii.write(gal_tab, clustername+'_gal_sdss_radec.ecsv', format='ecsv')

# ALso save files as csv so that ds9 catalog tools can use them
ascii.write(star_tab, clustername+'_star_sdss_radec.csv', format='csv')
ascii.write(gal_tab, clustername+'_gal_sdss_radec.csv', format='csv')

