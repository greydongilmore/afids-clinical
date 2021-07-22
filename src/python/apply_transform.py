# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:18:55 2019

@author: User
"""

import os
logic = slicer.vtkSlicerTransformLogic()
output_dir = r'D:\projects\templateProject\coreg'
github_out = r'C:\Users\Greydon\Documents\GitHub\afids_parkinsons\input\input_mniTransform'
input_dir = r'D:\projects\templateProject'
raters = ['AT','MA','MJ','RC','GG']


subjects = [x.split('-')[1] for x in os.listdir(r'C:\Users\Greydon\Documents\GitHub\afids_parkinsons\input\input_fid\GG')]
for isub in subjects:
	mni_transform(isub)

def mni_transform(subject):
	isub = 'sub-' + subject.zfill(3)
	transform_file = [x for x in os.listdir(os.path.join(input_dir, 'coreg', isub)) if x.endswith('mniTransform.tfm')][0]
	transform = slicer.util.loadTransform(os.path.join(input_dir, 'coreg', isub, transform_file))
	study_id = 'sub-P' + subject
	for irater in raters:
		try:
			markup_file = [x for x in os.listdir(os.path.join(input_dir, 'input_fid', irater, study_id)) if 'fid32' in x.lower()][0]
			slicer.util.loadMarkupsFiducialList(os.path.join(input_dir, 'input_fid', irater, study_id, markup_file))
		except:
			markup_file = [x for x in os.listdir(os.path.join(input_dir, 'input_fid', irater, isub)) if 'fid32' in x.lower()][0]
			slicer.util.loadMarkupsFiducialList(os.path.join(input_dir, 'input_fid', irater, isub, markup_file))
	
	markups = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')
	for imarkup in markups:
		if 'fid32' in imarkup.GetName().lower():
			imarkup.SetAndObserveTransformNodeID(transform.GetID())
			logic.hardenTransform(imarkup)
			slicer.util.saveNode(imarkup, os.path.join(output_dir, isub, imarkup.GetName() + '_mniTransform.fcsv'))
			slicer.util.saveNode(imarkup, os.path.join(github_out, imarkup.GetName() + '_mniTransform.fcsv'))
			slicer.mrmlScene.RemoveNode(slicer.util.getNode(imarkup.GetName()))
	
	transforms = slicer.util.getNodesByClass('vtkMRMLLinearTransformNode')
	for inode in transforms:        
		slicer.mrmlScene.RemoveNode(slicer.util.getNode(inode.GetName()))