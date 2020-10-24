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
    SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, 
    extinction_u, extinction_g,extinction_r, extinction_i, extinction_z, clean, s.z, s.zerr, pz.z as photoz, pz.zerr as photozerr 
    FROM fGetNearbyObjEq(ra, dec, radius) n, Star p 
    LEFT OUTER JOIN specObj s ON s.bestObjID=p.objID
    LEFT OUTER JOIN photoz pz ON pz.objid=p.objid
    WHERE n.objID=p.objID AND (s.class IS NULL or s.class = "STAR")

Galaxies Query:
    SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, 
    extinction_u, extinction_g,extinction_r, extinction_i, extinction_z, clean, s.z, s.zerr, pz.z as photoz, pz.zerr as photozerr 
    FROM fGetNearbyObjEq(ra, dec, radius) n, Galaxy p 
    LEFT OUTER JOIN specObj s ON s.bestObjID=p.objID
    LEFT OUTER JOIN photoz pz ON pz.objid=p.objid 
    WHERE n.objID=p.objID AND (s.class IS NULL or s.class = "GALAXY")


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


# Query for stars with psfMag and extinctions
q_star = "SELECT p.ra, p.dec, p.psfMag_u, p.psfMagErr_u, p.psfMag_g, p.psfMagErr_g, p.psfMag_r, p.psfMagErr_r, p.psfMag_i, p.psfMagErr_i, p.psfMag_z, p.psfMagErr_z, \
    extinction_u, extinction_g, extinction_r, extinction_i, extinction_z, clean, s.z, s.zerr, pz.z as photoz, pz.zerr as photozerr \
    FROM fGetNearbyObjEq("+ra+", "+dec+", "+radius+") n, Star p \
    LEFT OUTER JOIN specObj s ON s.bestObjID = p.objID \
    LEFT OUTER JOIN photoz pz ON pz.objid = p.objid \
    WHERE n.objID = p.objID AND(s.class IS NULL or s.class='STAR') "


# Query for galaxy with modelMag and cmodelMag and extinctions
q_gal = "SELECT p.ra, p.dec, p.modelMag_u, p.modelMagErr_u, p.modelMag_g, p.modelMagErr_g, p.modelMag_r, p.modelMagErr_r, p.modelMag_i, p.modelMagErr_i, p.modelMag_z, p.modelMagErr_z, \
    p.cmodelMag_u, p.cmodelMagErr_u, p.cmodelMag_g, p.cmodelMagErr_g, p.cmodelMag_r, p.cmodelMagErr_r, p.cmodelMag_i, p.cmodelMagErr_i, p.cmodelMag_z, p.cmodelMagErr_z, \
    extinction_u, extinction_g, extinction_r, extinction_i, extinction_z, clean, s.z, s.zerr, pz.z as photoz, pz.zerr as photozerr \
    FROM fGetNearbyObjEq("+ra+", "+dec+", "+radius+") n, Galaxy p \
    LEFT OUTER JOIN specObj s ON s.bestObjID = p.objID \
    LEFT OUTER JOIN photoz pz ON pz.objid = p.objid \
    WHERE n.objID = p.objID AND(s.class IS NULL or s.class='GALAXY') "
    

star_data = CasJobs.executeQuery(q_star, context=context, format='pandas')
gal_data = CasJobs.executeQuery(q_gal, context=context, format='pandas')

star_tab = Table(star_data.values, names=star_data.columns, meta={'clustername': clustername, 'ra': ra, 'dec': dec, 'radius': radius}, dtype=[ float for x in range(len(star_data.columns))])
gal_tab = Table(gal_data.values, names=gal_data.columns, meta={'clustername': clustername, 'ra': ra, 'dec': dec, 'radius': radius}, dtype=[ float for x in range(len(gal_data.columns))])


snospec = isnan(star_tab['z'])
gnospec = isnan(gal_tab['z'])

star_tab['z'][snospec] = -1.0
star_tab['zerr'][snospec] = -1.0
gal_tab['z'][gnospec] = -1.0
gal_tab['zerr'][gnospec] = -1.0

snophotoz = isnan(star_tab['photoz'])
star_tab['photoz'][snophotoz] = -99.0
star_tab['photozerr'][snophotoz] = -99.0

gnophotoz = gal_tab['photoz'] == -9999
gal_tab['photoz'][gnophotoz] = -99.0
gal_tab['photozerr'][gnophotoz] = -99.0

gnanphotoz = isnan(gal_tab['photoz'])
gal_tab['photoz'][gnanphotoz] = -99.0
gal_tab['photozerr'][gnanphotoz] = -99.0


ascii.write(star_tab, clustername+'_star_sdss_radec.csv', format='ecsv')
ascii.write(gal_tab, clustername+'_gal_sdss_radec.csv', format='ecsv')


