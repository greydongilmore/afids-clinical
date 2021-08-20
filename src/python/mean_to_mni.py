#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 16:01:34 2021

@author: greydon
"""

import os
import numpy as np
import pandas as pd
import csv
import glob

fid_dic = {1: 'AC',
		   2: 'PC',
		   3: 'ICS',
		   4: 'PMJ',
		   5: 'SIPF',
		   6: 'RSLMS',
		   7: 'LSLMS',
		   8: 'RILMS',
		   9: 'LILMS',
		   10: 'CUL',
		   11: 'IMS',
		   12: 'RMB',
		   13: 'LMB',
		   14: 'PG',
		   15: 'RLVAC',
		   16: 'LLVAC',
		   17: 'RLVPC',
		   18: 'LLVPC',
		   19: 'GENU',
		   20: 'SPLE',
		   21: 'RALTH',
		   22: 'LALTH',
		   23: 'RSAMTH',
		   24: 'LSAMTH',
		   25: 'RIAMTH',
		   26: 'LIAMTH',
		   27: 'RIGO',
		   28: 'LIGO',
		   29: 'RVOH',
		   30: 'LVOH',
		   31: 'ROSF',
		   32: 'LOSF'
		   }

def writeFCSV(data,fcsv_fname,coord_sys='RAS'):
	with open(fcsv_fname, 'w') as fid:
		fid.write("# Markups fiducial file version = 4.11\n")
		fid.write(f"# CoordinateSystem = {coord_sys}\n")
		fid.write("# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n")
	
	data_fcsv={
		'id':[],'x':[],'y':[],'z':[],'ow':[],'ox':[],'oy':[],'oz':[],'vis':[],'sel':[],'lock':[],'label':[],'desc':[],'associatedNodeID':[]
	}
	
	for ifid in data:
		fid_label=fid_dic[ifid[0]]
		data_fcsv['id'].append(int(ifid[0]))
		data_fcsv['x'].append(ifid[1])
		data_fcsv['y'].append(ifid[2])
		data_fcsv['z'].append(ifid[3])
		data_fcsv['ow'].append(0)
		data_fcsv['ox'].append(0)
		data_fcsv['oy'].append(0)
		data_fcsv['oz'].append(1)
		data_fcsv['vis'].append(1)
		data_fcsv['sel'].append(1)
		data_fcsv['lock'].append(1)
		data_fcsv['label'].append(fid_label)
		data_fcsv['desc'].append('')
		data_fcsv['associatedNodeID'].append('')
	
	with open(fcsv_fname, 'a') as out_file:
		writer = csv.writer(out_file, delimiter = ",")
		writer.writerows(zip(*data_fcsv.values()))

def sorted_nicely(data, reverse = False):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	
	return sorted(data, key = alphanum_key, reverse=reverse)

#%%

fname=r'/home/greydon/Documents/GitHub/afids-clinical/data/input_fid_native/sub-093_FID32_T1w_mean.csv'
out_name=os.path.splitext(fname)[0]+'.fcsv'
df = pd.read_csv(fname,header=None).to_numpy()

writeFCSV(df,out_name)

in_dir=r'/home/greydon/Documents/GitHub/afids-clinical/data/input_fid_native'

raters=[x for x in os.listdir(in_dir) if all(y not in x for y in ('mean','subjects'))]
subjects=[x for x in os.listdir(os.path.join(in_dir,'GG')) if 'mean' not in x]

for isub in sorted_nicely([x for x in os.listdir(os.path.join(in_dir,'GG'))]):
	avg_rater=[]
	for irate in raters:
		fname=glob.glob(os.path.join(in_dir, f'{irate}/{isub}/*.fcsv'))
		df=pd.read_csv(fname[0],skiprows=2)
		df=df.sort_values(by='label', ascending=True)
		df.insert(0,'rater',np.repeat(irate,df.shape[0]))
		
		avg_rater.append(df[['rater','x','y','z','label']].to_numpy())
	
	avg_rater=pd.DataFrame(np.vstack(avg_rater))
	avg_rater = avg_rater.rename(columns={0:'rater',1: 'x', 2: 'y',3:'z',4:'label'})
	
	avg_rater['x'] = pd.to_numeric(avg_rater['x'], downcast="float")
	avg_rater['y'] = pd.to_numeric(avg_rater['y'], downcast="float")
	avg_rater['z'] = pd.to_numeric(avg_rater['z'], downcast="float")
	
	out_fname=os.path.join(in_dir,'mean',isub,f'{isub}_FID32_T1w_mean.fcsv')
	if not os.path.exists(os.path.dirname(out_fname)):
		os.makedirs(os.path.dirname(out_fname))
		
		out_data=avg_rater[['x','y','z','label']].groupby('label').mean().to_numpy()
		out_data=np.c_[avg_rater['label'].unique(),out_data]
		
		writeFCSV(out_data, out_fname)



output_fcsv = f'/home/greydon/Documents/GitHub/afids-clinical/data/input_fid_MNI_linear_combined/sub-{str(isub).zfill(3)}_FID32_T1w_mnimean.csv'

avg_rater[['x','y','z','label']].groupby('label').mean().to_csv( output_fcsv, index=False )










