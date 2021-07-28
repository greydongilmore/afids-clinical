#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 01:10:42 2021

@author: greydon
"""
import pandas as pd
import numpy as np
import matplotlib
import re
import matplotlib.pyplot as plt
from nilearn import plotting


input_fcsv=r'/home/greydon/Documents/GitHub/afids-clinical/data/fid_standards/MNI152NLin2009cAsym_standard_afids/MNI152NLin2009cAsym_standard.fcsv'


df = pd.read_table(input_fcsv,sep=',',header=2)
midline_fids=[1,2,3,4,5,10,11,14,19,20]


fid_color= np.array([(0, 0, 255)]*df.shape[0])/255
update_idx=np.array([i for i, j in enumerate(df['label']) if any(y == j for y in midline_fids)])
fid_color[update_idx]=np.array((0, 255, 0))/255

fid_color[df['label'] == midline_fids]

cmap = plt.get_cmap('viridis')
colors=cmap(fid_color)

coords = df[['x','y','z']].to_numpy()


html_view = plotting.view_markers(coords, marker_size=6.0, marker_color=fid_color, marker_labels=df['label'].tolist())
html_view.open_in_browser()

html_view.save_as_html('/home/greydon/Downloads/connectome.html')
