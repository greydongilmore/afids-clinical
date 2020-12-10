#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 03:15:24 2020

@author: greydon
"""
import os
import glob
import subprocess
import pandas as pd
import transforms3d
import h5py
import numpy as np

def convertSlicerRASFCSVtoAntsLPSCSV( input_fcsv, output_csv ):
    # convert Slicer RAS oriented FCSV (default) to Ants LPS oriented format (expected orientation)
    # use with CAUTION: orientation flips here

    df = pd.read_csv( input_fcsv, skiprows=2, usecols=['x','y','z'] ) # first 2 rows of fcsv not necessary for header
    df['x'] = -1 * df['x'] # flip orientation in x
    df['y'] = -1 * df['y'] # flip orientation in y
    df.to_csv( output_csv, index=False )

def convertAntsLPSCSVtoSlicerRASFCSV( input_csv, output_fcsv, ref_fcsv ):
    # convert Ants LPS oriented format (ants expected orientation) to Slicer RAS oriented FCSV (for viewing in Slicer)
    # use with CAUTION: orientation flips here

    # extract Slicer header
    f = open( ref_fcsv, 'r' )
    lines = f.readlines()
    f.close()

    # orienting the image image back to RAS from LPS
    input_df = pd.read_csv( input_csv, usecols=['x','y','z'] ) # use reference fcsv as template
    df = pd.read_csv( ref_fcsv, skiprows=2 ) # use reference fcsv as template
    df['x'] = -1 * input_df['x'] # flip orientation in x
    df['y'] = -1 * input_df['y'] # flip orientation in y
    df['z'] = input_df['z'] # normal orientation in z
    df.to_csv( output_fcsv, index=False )

    # add in extracted Slicer header
    with open( output_fcsv, 'r+' ) as f:
        old = f.read() # read all the old csv file info
        f.seek(0) # rewind, start at the top
        f.write( lines[0] + lines[1] + old ) # add expected Slicer header


def run_command(cmdLineArguments):
	process = subprocess.Popen(cmdLineArguments, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
	stdout = process.communicate()[0]
	p_status = process.wait()
		
input_bids_dir=r'/media/veracrypt6/projects/templateProjects/fmriprep/output/fmriprep'
input_fcsv_dir=r'/home/greydon/Documents/GitHub/afids_parkinsons/input/input_fid'
output_dir=r'/home/greydon/Documents/GitHub/afids_parkinsons/input/input_linear_transform'

raters = ['AT','MA','MJ','RC']

if not os.path.exists(output_dir):
	os.makedirs(output_dir)
	

for irate in raters:
	files = [x for x in glob.glob(input_fcsv_dir+f'/{irate}/*/*.fcsv')]
	
	rater_out=os.path.join(output_dir,irate)
	if not os.path.exists(rater_out):
		os.makedirs(rater_out)
	
	for ifile in files:
		subj=os.path.basename(os.path.dirname(ifile))
		
		input_warp_to_MNI152=os.path.join(input_bids_dir, subj, 'anat', f'{subj}_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5')
		input_warp_to_MNI152_dis=os.path.join(input_bids_dir, subj, 'anat', f'{subj}_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm')
		
		affineT=os.path.join(input_bids_dir, subj, "anat",f'00_{subj}_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm_AffineTransform.mat')
		displacement=os.path.join(input_bids_dir, subj, "anat",f'01_{subj}_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm_DisplacementFieldTransform.nii.gz')
		
		output_fcsv=os.path.splitext(os.sep.join([output_dir] + ifile.split(os.sep)[-3:]))[0] + '_lin.fcsv'
		tmp_slicer_to_ants_csv = os.path.dirname(output_fcsv) + "/tmp_slicer_to_ants.csv"
		tmp_slicer_to_ants_transformed_csv = os.path.dirname(output_fcsv) + "/tmp_slicer_to_ants_transformed.csv"
		
		if not os.path.exists(os.path.dirname(output_fcsv)):
			os.makedirs(os.path.dirname(output_fcsv))
		
		
		if not os.path.exists(affineT):
			cmd= f'cd {os.path.join(input_bids_dir, subj, "anat")} && /opt/ANTs/bin/CompositeTransformUtil --disassemble {os.path.basename(input_warp_to_MNI152)} {os.path.basename(input_warp_to_MNI152_dis)}'
			run_command(cmd)
		
		
		convertSlicerRASFCSVtoAntsLPSCSV( ifile, tmp_slicer_to_ants_csv )
		
		
		cmd = ' '.join(['/opt/ANTs/bin/antsApplyTransformsToPoints',
				  '-d', str(3),
				  '-i', '"'+tmp_slicer_to_ants_csv+'"',
				  '-o', '"'+tmp_slicer_to_ants_transformed_csv+'"',
				  '-t', ''.join(['"[', '"', affineT, '"', ",", str(1), ']"']),
				  '-t', displacement])
		
		run_command(cmd)
		
		
		convertAntsLPSCSVtoSlicerRASFCSV( tmp_slicer_to_ants_transformed_csv, output_fcsv, ifile )
		
		
		os.remove(tmp_slicer_to_ants_csv)
		os.remove(tmp_slicer_to_ants_transformed_csv)
		

		