#!/bin/bash

# need to create R/G/B_list.txt and R/G/B_scamp_list.txt

for file in `cat R_scamp_list.txt`; do name=`echo $file | sed -e 's/\.cat//g'`; scamp -MOSAIC_TYPE SAME_CRVAL -ASTREF_CATALOG ALLWISE -POSITION_MAXERR 1.0 -c default.scamp $file; name2=`echo $name | sed -e 's/_scamp_cal//g'`; mv ${name}.head ${name2}.head; done

for file in `cat G_scamp_list.txt`; do name=`echo $file | sed -e 's/\.cat//g'`; scamp -MOSAIC_TYPE SAME_CRVAL -ASTREF_CATALOG ALLWISE -POSITION_MAXERR 1.0 -c default.scamp $file; name2=`echo $name | sed -e 's/_scamp_cal//g'`; mv ${name}.head ${name2}.head; done

for file in `cat B_scamp_list.txt`; do name=`echo $file | sed -e 's/\.cat//g'`; scamp -MOSAIC_TYPE SAME_CRVAL -ASTREF_CATALOG ALLWISE -POSITION_MAXERR 1.0 -c default.scamp $file; name2=`echo $name | sed -e 's/_scamp_cal//g'`; mv ${name}.head ${name2}.head; done



swarp @R_list.txt -c default.swarp -IMAGEOUT_NAME R_stack.fits -WEIGHTOUT_NAME R_stack.wt.fits -COMBINE_TYPE WEIGHTED
swarp @G_list.txt -c default.swarp -IMAGEOUT_NAME G_stack.fits -WEIGHTOUT_NAME G_stack.wt.fits -COMBINE_TYPE WEIGHTED
swarp @B_list.txt -c default.swarp -IMAGEOUT_NAME B_stack.fits -WEIGHTOUT_NAME B_stack.wt.fits -COMBINE_TYPE WEIGHTED

