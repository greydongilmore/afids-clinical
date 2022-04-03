# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import random
import matplotlib
from collections import OrderedDict
import seaborn as sns
import matplotlib.gridspec as gridspec
from matplotlib.font_manager import FontProperties

plt.rcdefaults()
plt.rc('xtick.major', size = 0, width=0)
plt.rc('ytick.major', size = 0, width=0)

data_dir = r'/home/greydon/Documents/GitHub/afids-clinical/data/input_fid_native'
data_mni_dir = r'/home/greydon/Documents/GitHub/afids-clinical/data/input_fid_MNI_linear_combined'
#data_dir = r'C:\Users\greydon\Documents\github\afids_parkinsons\input\input_fid'

show_only = True

sub_ignore = [146]

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

fid_desc = {1: 'AC',
		   2: 'PC',
		   3: 'Infracollicular Sulcus',
		   4: 'PMJ',
		   5: 'Superior IPF',
		   6: 'Right Superior LMS',
		   7: 'Left Superior LMS',
		   8: 'Right Inferior LMS',
		   9: 'Left Inferior LMS',
		   10: 'Culmen',
		   11: 'Intermammillary Sulcus',
		   12: 'Right Mammilary Body',
		   13: 'Left Mammilary Body',
		   14: 'Pineal Gland',
		   15: 'Right LV at AC',
		   16: 'Left LV at AC',
		   17: 'Right LV at PC',
		   18: 'Left LV at PC',
		   19: 'Genu of CC',
		   20: 'Splenium of CC',
		   21: 'Right AL Temporal Horn',
		   22: 'Left AL Tempral Horn',
		   23: 'R. Sup. AM Temporal Horn',
		   24: 'L. Sup. AM Temporal Horn',
		   25: 'R Inf. AM Temp Horn',
		   26: 'L Inf. AM Temp Horn',
		   27: 'Right IG Origin',
		   28: 'Left IG Origin',
		   29: 'R Ventral Occipital Horn',
		   30: 'L Ventral Occipital Horn',
		   31: 'R Olfactory Fundus',
		   32: 'L Olfactory Fundus'
		   }

def plot_fiducials(data_plot, expert_mean, data_dir,analysis=2, showOnly=False):
	random.seed(1)
	color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(raters))]
	
	min_val = -2.5
	max_val = 2.5
	major_ticks = np.linspace(min_val,max_val, 7)
	
	fig = plt.figure(figsize=(18,8))
	handles = {}
	data_cnt = 1
	for ifid in range(4):
		for jfid in range(8):
			ax = plt.subplot2grid((4,8),(ifid,jfid), projection='3d')
			tempData = data_plot[data_plot['fid'].isin([data_cnt])]
			rater_labels = tempData['rater'].values
			if analysis == 1:
				plot_title = 'Distance from the average of expert raters'
				file_name = 'distance_from_expert_mean'
				tempData = tempData.loc[:,'x':'z'].values - expert_mean.loc[expert_mean['fid'].isin([data_cnt]),'x':'z'].values
			elif analysis == 2:
				plot_title = 'Distance from the average of all raters'
				file_name = 'distance_from_all_raters_mean'
				tempData = tempData.loc[:,'x':'z'].values - tempData.loc[:,'x':'z'].mean().values
			elif analysis == 3:
				plot_title = 'Distance from average MCP'
				file_name = 'distance_from_avg_mcp'
				tempData = tempData.loc[:,'x':'z'].values - tempData.loc[:,'x':'z'].mean().values
			
			nov_cnt = 1
			exp_cnt = 1
			rater_labels_final_tmp = {}
			for i in range(len(rater_labels)): #plot each point + it's index as text above
				if rater_labels[i] in ('AT','RC','MJ'):
					rate_label = f"Novice 0{nov_cnt}"
					nov_cnt += 1
				else:
					rate_label = f"Expert 0{exp_cnt}"
					exp_cnt += 1
				rater_labels_final_tmp[rate_label] = rater_labels[i]
			
			rater_labels_final = {}
			for irate in sorted(list(rater_labels_final_tmp)):
				rater_labels_final[irate]=rater_labels_final_tmp[irate]
			print(rater_labels_final)
			for irate in list(rater_labels_final):
				rater_idx = [i for i,x in enumerate(rater_labels) if x == rater_labels_final[irate]][0]
				l1 = ax.scatter(tempData[rater_idx,0], tempData[rater_idx,1], tempData[rater_idx,2], marker='o', c=color[rater_idx],edgecolors='black', s=50, label=irate)
				handles[irate] = l1
			
			ax.plot((min_val,min_val), (min_val,min_val), (min_val-0.1,max_val+0.1), 'black', linewidth=1.0)
			
			ax.set_xlim([min_val,max_val])
			ax.set_ylim([min_val,max_val])
			ax.set_zlim([min_val,max_val])
			
			ax.set_xlabel('x',labelpad=-15, fontweight='bold', fontsize=14)
			ax.set_ylabel('y',labelpad=-15, fontweight='bold', fontsize=14)
			ax.set_zlabel('z',labelpad=-15, fontweight='bold', fontsize=14)
			
			ax.get_xaxis().set_ticklabels([])
			ax.get_yaxis().set_ticklabels([])
			ax.zaxis.set_ticklabels([])
			ax.zaxis.set_major_locator(matplotlib.ticker.NullLocator())
			
			ax.set_xticks(major_ticks)
			ax.set_yticks(major_ticks)
			ax.set_zticks(major_ticks)
			
			ax.grid(which='major', alpha=0.5)
			
			ax.xaxis.pane.set_edgecolor('black')
			ax.yaxis.pane.set_edgecolor('black')
			ax.zaxis.pane.set_edgecolor('black')
			ax.xaxis.pane.set_alpha(1)
			ax.yaxis.pane.set_alpha(1)
			ax.zaxis.pane.set_alpha(1)
			ax.xaxis.pane.fill = False
			ax.yaxis.pane.fill = False
			ax.zaxis.pane.fill = False
					
			ax.view_init(elev=25, azim=44)
			
			ax.set_title(str(data_cnt) + ': ' + fid_dic[data_cnt], pad=2, fontweight='bold', fontsize=16)
			
			data_cnt += 1
			
	fig.subplots_adjust(hspace=0.15, wspace=0.05, top=0.90, bottom=0.06, left=0.02,right=0.9) 
	plt.legend(handles=handles.values(), fontsize=12, bbox_to_anchor=[2.1, 2.7], handletextpad=0.05)
	fig.suptitle(plot_title, y = 0.98, fontsize=22, fontweight='bold')
	
	if not showOnly:
		output_dir = os.path.join(data_dir,'plots')
		
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		plt.savefig(os.path.join(output_dir, f"{file_name}.svg"),transparent=True)
		plt.savefig(os.path.join(output_dir, f"{file_name}.png"),transparent=True,dpi=450)
		plt.savefig(os.path.join(output_dir, f"{file_name}_white.png"),transparent=False,dpi=450)
		plt.close()


#%%

data_dir_out = r'/home/greydon/Documents'

sub_ignore = [146]

raters = [x for x in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, x)) and 'mean' not in x]

rater_final = pd.DataFrame({})
iter_cnt = 0
for irater in raters:
	patient_files = os.listdir(os.path.join(data_dir, irater))
	for isub in patient_files:
		sub_num = int(''.join([s for s in isub if s.isdigit()]))
		fileN = os.path.join(data_dir, irater,isub, os.listdir(os.path.join(data_dir, irater,isub))[0])
		data_table = pd.read_csv(fileN, skiprows=3, header=None)
		data_table['rater'] = np.repeat(irater,data_table.shape[0])
		data_table['subject'] = np.repeat(sub_num,data_table.shape[0])
		rater_final = pd.concat([rater_final, data_table], axis = 0, ignore_index=True)

rater_final.rename(columns={0:'node_id', 1:'x', 2:'y', 3:'z', 4:'ow', 5:'ox',
							6:'oy', 7:'oz', 8:'vis', 9:'sel', 10:'lock',
							11:'fid', 12:'description', 13:'associatedNodeID'}, inplace=True)


Sub = pd.DataFrame({})
size = []
for r in raters:
	sub_temp = np.unique(rater_final[rater_final['rater']==r]['subject'])
	if sub_ignore:
		sub_temp = [x for x in sub_temp if x not in sub_ignore]
	data_table = pd.DataFrame({'rater': np.repeat(r,len(sub_temp)), 'subject':sub_temp})
	Sub = pd.concat([Sub, data_table], axis = 0, ignore_index=True)
	size.append((r,len(sub_temp)))

full_subs = set(Sub[Sub['rater']==size[0][0]]['subject'].values)

size = sorted(size, key=lambda tup: tup[1], reverse=True)
Sub_Comp = list(set(Sub[Sub['rater']==size[0][0]]['subject'].values) & 
				set(Sub[Sub['rater']==size[1][0]]['subject'].values))

for irate in range(2,len(raters)):
	Sub_Comp = list(set(Sub_Comp) & set(Sub[Sub['rater']==size[irate][0]]['subject'].values))

Sub_Comp = sorted(Sub_Comp)
#set(full_subs).difference(Sub[Sub['rater']==size[4][0]]['subject'].values)

Data_comp = rater_final[rater_final['subject'].isin(Sub_Comp)]
Data_comp = Data_comp.sort_values(['rater','subject', 'fid'], ascending=[True, True,True])

Tot_Data = np.zeros((32,5,len(Sub_Comp),len(raters)))
for irate in range(len(raters)):
	for isub in range(len(Sub_Comp)):
		Tot_Data[:,:,isub,irate] = Data_comp[(Data_comp['rater']==raters[irate]) & (Data_comp['subject']==Sub_Comp[isub])].sort_values(['fid']).loc[:,['fid','x','y','z','subject']]

Tot_mean = np.mean(Tot_Data,3)

N = Tot_mean[:,:,:,np.newaxis]
Tot_diff = Tot_Data - np.tile(N,[1,1,1,len(raters)])
Tot_eudiff = np.sqrt(Tot_diff[:,1,:,:]**2 + Tot_diff[:,2,:,:]**2 + Tot_diff[:,3,:,:]**2)
Rater_AFLE = np.mean(Tot_eudiff,2).T

Rater_AFLE_mean = np.mean(Tot_eudiff,1)
Rater_AFLE_SD = np.std(Tot_eudiff,1)
Total_AFLE_mean = np.mean(Rater_AFLE_mean,1)
Total_AFLE_SD = np.std(Tot_eudiff,1)


mcp_point = pd.DataFrame({})
for r in raters:
	for s in Sub_Comp:
		ac = Data_comp.loc[(Data_comp['rater']==r) & (Data_comp['subject']==s) & (Data_comp['fid']==1),'x':'z'].values[0]
		pc = Data_comp.loc[(Data_comp['rater']==r) & (Data_comp['subject']==s)& (Data_comp['fid']==2),'x':'z'].values[0]
		mcp = (ac + pc)/2
		data_table = pd.DataFrame({'rater': r, 'subject': s, 'x': mcp[0], 'y': mcp[1],'z': mcp[2]}, index=[0] )
		mcp_point = pd.concat([mcp_point, data_table], axis = 0, ignore_index=True)

mcp_point_mean = mcp_point.groupby(['subject'])['x','y','z'].mean()

data_from_mcp = pd.DataFrame({})
for r in raters:
	for s in Sub_Comp:
		for f in range(1,33):
			point = Data_comp.loc[(Data_comp['rater']==r) & (Data_comp['subject']==s) & (Data_comp['fid']==f),'x':'z'].values[0]
			di = point - mcp_point_mean.loc[s,:].values
			euclidean = np.sqrt(di[0]**2 + di[1]**2 + di[2]**2)
			data_table = pd.DataFrame({'rater': r, 'subject': s, 'fid': f, 'distance': euclidean,'x': di[0], 'y': di[1],'z': di[2]}, index=[0] )
			data_from_mcp = pd.concat([data_from_mcp, data_table], axis = 0, ignore_index=True)
			
data_from_mcp_avg = data_from_mcp.groupby(['rater','fid'])['x','y','z'].mean().reset_index()


#%%	

sub_ignore = [146]


rater_mni_final = pd.DataFrame({})
iter_cnt = 0
for irater in raters:
	patient_files = os.listdir(os.path.join(data_mni_dir, irater))
	for isub in patient_files:
		sub_num = int(''.join([s for s in isub if s.isdigit()]))
		fileN = os.path.join(data_mni_dir, irater,isub, [x for x in os.listdir(os.path.join(data_mni_dir, irater,isub)) if x.endswith('_nlin.fcsv')][0])
		data_table = pd.read_csv(fileN, skiprows=3, header=None)
		data_table['rater'] = np.repeat(irater,data_table.shape[0])
		data_table['subject'] = np.repeat(sub_num,data_table.shape[0])
		rater_mni_final = pd.concat([rater_mni_final, data_table], axis = 0, ignore_index=True)

rater_mni_lin_final = pd.DataFrame({})
iter_cnt = 0
for irater in raters:
	patient_files = os.listdir(os.path.join(data_mni_dir, irater))
	for isub in patient_files:
		sub_num = int(''.join([s for s in isub if s.isdigit()]))
		fileN = os.path.join(data_mni_dir, irater,isub, [x for x in os.listdir(os.path.join(data_mni_dir, irater,isub)) if x.endswith('_lin.fcsv')][0])
		data_table = pd.read_csv(fileN, skiprows=3, header=None)
		data_table['rater'] = np.repeat(irater,data_table.shape[0])
		data_table['subject'] = np.repeat(sub_num,data_table.shape[0])
		rater_mni_lin_final = pd.concat([rater_mni_lin_final, data_table], axis = 0, ignore_index=True)

rater_mni_final.rename(columns={0:'node_id', 1:'x', 2:'y', 3:'z', 4:'ow', 5:'ox',
							6:'oy', 7:'oz', 8:'vis', 9:'sel', 10:'lock',
							11:'fid', 12:'description', 13:'associatedNodeID'}, inplace=True)


rater_mni_lin_final.rename(columns={0:'node_id', 1:'x', 2:'y', 3:'z', 4:'ow', 5:'ox',
							6:'oy', 7:'oz', 8:'vis', 9:'sel', 10:'lock',
							11:'fid', 12:'description', 13:'associatedNodeID'}, inplace=True)


Sub = pd.DataFrame({})
size = []
for r in raters:
	sub_temp = np.unique(rater_mni_final[rater_mni_final['rater']==r]['subject'])
	if sub_ignore:
		sub_temp = [x for x in sub_temp if x not in sub_ignore]
	data_table = pd.DataFrame({'rater': np.repeat(r,len(sub_temp)), 'subject':sub_temp})
	Sub = pd.concat([Sub, data_table], axis = 0, ignore_index=True)
	size.append((r,len(sub_temp)))

full_subs = set(Sub[Sub['rater']==size[0][0]]['subject'].values)

size = sorted(size, key=lambda tup: tup[1], reverse=True)
Sub_Comp = list(set(Sub[Sub['rater']==size[0][0]]['subject'].values) & 
				set(Sub[Sub['rater']==size[1][0]]['subject'].values))

for irate in range(2,len(raters)):
	Sub_Comp = list(set(Sub_Comp) & set(Sub[Sub['rater']==size[irate][0]]['subject'].values))

Sub_Comp = sorted(Sub_Comp)

Data_mni_comp = rater_mni_final[rater_mni_final['subject'].isin(Sub_Comp)]
Data_mni_comp = Data_mni_comp.sort_values(['rater','subject', 'fid'], ascending=[True, True,True])

Data_mni_lin_comp = rater_mni_lin_final[rater_mni_lin_final['subject'].isin(Sub_Comp)]
Data_mni_lin_comp = Data_mni_lin_comp.sort_values(['rater','subject', 'fid'], ascending=[True, True,True])

Tot_Data = np.zeros((32,5,len(Sub_Comp),len(raters)))
Tot_Data_lin = np.zeros((32,5,len(Sub_Comp),len(raters)))
for irate in range(len(raters)):
	for isub in range(len(Sub_Comp)):
		Tot_Data[:,:,isub,irate] = Data_mni_comp[(Data_mni_comp['rater']==raters[irate]) & (Data_mni_comp['subject']==Sub_Comp[isub])].sort_values(['fid']).loc[:,['fid','x','y','z','subject']]
		Tot_Data_lin[:,:,isub,irate] = Data_mni_lin_comp[(Data_mni_lin_comp['rater']==raters[irate]) & (Data_mni_lin_comp['subject']==Sub_Comp[isub])].sort_values(['fid']).loc[:,['fid','x','y','z','subject']]


MNI152NLin2009cAsym_standard = pd.read_csv('/home/greydon/Documents/GitHub/afids-clinical/data/fid_standards/MNI152NLin2009bAsym_rater_standard/MNI152NLin2009bAsym_desc-raterstandard_afids.fcsv', skiprows=2)[['label','x','y','z']].to_numpy()
N = MNI152NLin2009cAsym_standard[:,:,np.newaxis, np.newaxis]
MNI_Diff = Tot_Data[:,:4,:,:] - np.tile(N,[1,1,len(Sub_Comp),len(raters)])
MNI_AFLE = np.sqrt(MNI_Diff[:,1,:,:]**2 + MNI_Diff[:,2,:,:]**2 + MNI_Diff[:,3,:,:]**2)
MNI_Diff_lin = Tot_Data_lin[:,:4,:,:] - np.tile(N,[1,1,len(Sub_Comp),len(raters)])
MNI_AFLE_lin = np.sqrt(MNI_Diff_lin[:,1,:,:]**2 + MNI_Diff_lin[:,2,:,:]**2 + MNI_Diff_lin[:,3,:,:]**2)



MNI_AFLE_rater = np.mean(MNI_AFLE,2).T
MNI_AFLE_scan = np.mean(MNI_AFLE,1)
MNI_AFLE_total = np.mean(MNI_AFLE_rater,0)
MNI_AFLE_std = np.std(MNI_AFLE_rater,0)
np.mean(MNI_AFLE_total)
np.std(MNI_AFLE_total)

MNI_AFLE_lin_rater = np.mean(MNI_AFLE_lin,2).T
MNI_AFLE_lin_scan = np.mean(MNI_AFLE_lin,1)
MNI_AFLE_lin_total = np.mean(MNI_AFLE_lin_rater,0)
MNI_AFLE_lin_std = np.std(MNI_AFLE_lin_rater,0)
np.mean(MNI_AFLE_lin_total)
np.std(MNI_AFLE_lin_total)


df=pd.DataFrame(np.c_[
					  [N + P for N,P in zip([f'{x:.2f}' for x in MNI_AFLE_lin_total ],[f' ({x:.2f})' for x in MNI_AFLE_lin_std])]+[f'{np.mean(MNI_AFLE_lin_total):.2f} ({np.std(MNI_AFLE_lin_total):.2f})'],
					  [N + P for N,P in zip([f'{x:.2f}' for x in MNI_AFLE_total ],[f' ({x:.2f})' for x in MNI_AFLE_std])]+[f'{np.mean(MNI_AFLE_total):.2f} ({np.std(MNI_AFLE_total):.2f})']
					  ])
print(df.to_csv(index=None, header=None))

#%%
goldStandard = "MA"
rater = 1

gold_stand_data = Data_comp[Data_comp['rater'].isin([goldStandard])].reset_index()
single_rater_data = Data_comp[Data_comp['rater'].isin([raters[rater]])].reset_index()

Coor_Diff = gold_stand_data.loc[:,'x':'z'].values - (single_rater_data.loc[:,'x':'z'].values)
	
rater_error = np.sqrt(Coor_Diff[:,0]**2 + Coor_Diff[:,1]**2 + Coor_Diff[:,2]**2)
single_rater_data['rater_error'] = rater_error

error_idx = single_rater_data['rater_error'] > 5.0
check_data = pd.DataFrame({'subject': single_rater_data.loc[error_idx,'subject'].values,
							   'fid': single_rater_data.loc[error_idx,'fid'].values,
							   'x': single_rater_data.loc[error_idx,'x'].values,
							   'y': single_rater_data.loc[error_idx,'y'].values,
							   'z': single_rater_data.loc[error_idx,'z'].values,
							   'x_diff': Coor_Diff[error_idx,0],
							   'y_diff': Coor_Diff[error_idx,1],
							   'z_diff': Coor_Diff[error_idx,2]})
		
check_data = check_data.sort_values(['subject', 'fid'], ascending=[True, True])


#%%
GS_raters = ["GG", "MA"]
NGS_raters = [x for x in raters if x not in GS_raters]

GS_mean = Data_comp[Data_comp['rater'].isin(GS_raters)].groupby(['subject','fid'])['x','y','z'].mean().reset_index()
NGS_mean = Data_comp[Data_comp['rater'].isin(NGS_raters)].groupby(['subject','fid'])['x','y','z'].mean().reset_index()

GS_Diff = GS_mean.loc[:,'x':'z'].values - NGS_mean.loc[:,'x':'z'].values
GS_error_rate = np.sqrt(GS_Diff[:,0]**2 + GS_Diff[:,1]**2 + GS_Diff[:,2]**2)

GS_Diff_mean = pd.DataFrame(np.c_[GS_Diff, GS_mean['subject'].values, GS_mean['fid'].values]).groupby([4])[0,1,2].mean()

GS_total_mean = GS_mean.groupby(['fid'])['x','y','z'].mean().reset_index()
rater_mean = Data_comp.groupby(['rater','fid'])['x','y','z'].mean().reset_index()

#%%

plot_fiducials(rater_mean, GS_total_mean, data_dir_out, 1, False)
plot_fiducials(rater_mean, GS_total_mean, data_dir_out, 2, False)
plot_fiducials(data_from_mcp_avg, None, data_dir_out, 3, False)

#%%

comparisons = [("GG", 'MA'),("GG", 'AT'),("GG", 'RC'),("GG", 'MJ'),("MA", 'AT'),
			   ("MA", 'RC'),("MA", 'MJ'),("AT", 'RC'),("AT", 'MJ'),("RC", 'MJ')]

max_val = 8.0

fig, axes = plt.subplots(4, 2)
plot_cnt = 0
for irow in range(4):
	for icol in range(2):
		rater_1 = comparisons[plot_cnt][0]
		rater_2 = comparisons[plot_cnt][1]
		
		rater_1_data = Data_comp[Data_comp['rater'].isin([rater_1])].reset_index()
		rater_2_data = Data_comp[Data_comp['rater'].isin([rater_2])].reset_index()
		
		rater_coor_Diff = rater_1_data.loc[:,'x':'z'].values.astype(float) - rater_2_data.loc[:,'x':'z'].values.astype(float)
				
		rater_coor_error = pd.DataFrame(np.sqrt(rater_coor_Diff[:,0]**2 + rater_coor_Diff[:,1]**2 + rater_coor_Diff[:,2]**2))
		rater_coor_error.rename(columns={0:'error'}, inplace=True)
		fid_names = [fid_dic[x] for x in np.unique(rater_1_data['fid'].values.astype(int))]
		rater_coor_error['name']= fid_names*int(len(rater_coor_Diff)/len(fid_names))
		rater_coor_error['fid']= list(np.unique(rater_1_data['fid'].values.astype(int)))*int(len(rater_coor_Diff)/len(fid_names))
		
		rater_coor_error_plot = pd.DataFrame({})
		rater_coor_error_plot['error'] = rater_coor_error.groupby(['fid'])['error'].mean().values
		rater_coor_error_plot['name'] = fid_names
		rater_coor_error_plot['fid'] = list(np.unique(rater_1_data['fid'].values.astype(int)))
		
		title = ' '.join(["Error Between", rater_1, 'and', rater_2])
		rater_coor_error_plot[['error']].plot(kind='bar', title =title, ax=axes[irow,icol], legend=False, align='center', width=0.8)
		if irow == 3:
			axes[irow,icol].set_xlabel("Fiducial", fontsize=12, fontweight = 'bold')
		else:
			axes[irow,icol].xaxis.label.set_visible(False)
			
		axes[irow,icol].set_ylabel("Error", fontsize=12, fontweight = 'bold')
		
		axes[irow,icol].set_ylim([0,max_val])
		
		labels = [item.get_text() for item in axes[irow,icol].get_xticklabels()]
		new_labels = [ "%d" % int(float(l)) if '.0' in l else '' for l in labels]
		axes[irow,icol].set_xticklabels(new_labels,rotation = 45, fontweight='bold')
		
		plot_cnt += 1

fig.subplots_adjust(hspace=0.4, wspace=0.10, top=0.95, bottom=0.06, left=0.05, right=0.95) 

if not show_only:
	output_temp = os.path.dirname(data_dir)
	output_dir = os.path.join(os.path.dirname(output_temp),'output', 'plots')
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	
	file_name = 'error_between_all_raters.png'
	
	fig = plt.gcf()
	fig.set_size_inches(16, 10)
	fig.savefig(os.path.join(output_dir, file_name), dpi=100)
	plt.close()

#%%

output_dir = r'/home/greydon/Documents/GitHub/afids_parkinsons/output/avg_fcsv'
overall_mean = Data_comp.groupby(['subject','fid'])['x','y','z'].mean().reset_index()

for isub in np.unique(overall_mean['subject']):
	
	filename = "_".join(['sub-'+str(isub).zfill(3), 'FID32', 'T1w', 'standard.fcsv'])
	output_fname = os.path.join(output_dir, filename)
	
	with open(output_fname, 'w') as fid:
		fid.write("# Markups fiducial file version = 4.10\n")
		fid.write("# CoordinateSystem = 0\n")
		fid.write("# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n")
	
	fid_results = pd.DataFrame({})
	cnt = 1
	for ipoint in range(len(overall_mean[overall_mean['subject']==isub])):
		fid_out = {}
		fid_out['id']=str(cnt)
		fid_out['x']=str(overall_mean[overall_mean['subject']==isub]['x'].values[ipoint])
		fid_out['y']=str(overall_mean[overall_mean['subject']==isub]['y'].values[ipoint])
		fid_out['z']=str(overall_mean[overall_mean['subject']==isub]['z'].values[ipoint])
		fid_out['ow']=float(0)
		fid_out['ox']=float(0)
		fid_out['oy']=float(0)
		fid_out['oz']=float(1)
		fid_out['vis']=int(1)
		fid_out['sel']=int(1)
		fid_out['lock']=int(1)
		fid_out['label']=int(overall_mean[overall_mean['subject']==isub]['fid'].values[ipoint])
		fid_out['desc']=fid_desc[overall_mean[overall_mean['subject']==isub]['fid'].values[ipoint]]
		fid_out['associatedNodeID']=''
		
		fid_results = pd.concat([fid_results, pd.DataFrame([fid_out])], axis = 0)
		
		cnt+=1
	
	fid_results.to_csv(output_fname, sep=',', index=False, line_terminator="", mode='a', float_format='%.3f', header=False)
	
		
#%%

k=5
n=39

icc_data = Data_comp.groupby(['rater','subject','fid'])['x','y','z'].mean().reset_index()

Mean_Sub = Data_comp.sort_values(by=['rater','subject','fid'])[['x','y','z']].values.reshape(32, 3, 39)
Mean_Rat = icc_data.groupby(['fid','subject'])['x','y','z'].mean().reset_index()
Mean_Grand=Mean_Sub.groupby(['fid'])['x','y','z'].mean().reset_index()
test=Mean_Rat.sort_values(by=['subject','fid'])[['x','y','z']].values.reshape((32, 3, 39))

ICC_1=[]
for isub in range(len(Mean_Rat['subject'].unique())):
	ICC_1.append(((test[:,:,isub] - Mean_Grand[['x','y','z']].values)**2)*k)

ICC_1=np.vstack(ICC_1)
ICC_1_stat=np.sum(np.stack(ICC_1),0)/(n-1)



afle = pd.DataFrame({})
afle['subject'] = data_from_mcp['subject']
afle['rater'] = data_from_mcp['rater']
afle['fid'] = data_from_mcp['fid']
raters_data = data_from_mcp.loc[:,['x','y','z']].values
rater_data_avg = np.tile(data_from_mcp.groupby(['subject','fid'])['x','y','z'].mean().values[None,:], (len(raters), 1))[0]
rater_diff = raters_data - rater_data_avg
afle['euclid'] = pd.DataFrame(np.sqrt(rater_diff[:,0]**2 + rater_diff[:,1]**2 + rater_diff[:,2]**2)).values
afle['x'] = data_from_mcp['x']
afle['y'] = data_from_mcp['y']
afle['z'] = data_from_mcp['z']

exp_nov=np.zeros(afle.shape[0])
exp_nov[afle['rater'].isin(['MA','GG'])]=1
afle['exp_nov']=exp_nov

exp_nov=np.zeros(data_from_mcp.shape[0])
exp_nov[data_from_mcp['rater'].isin(['MA','GG'])]=1
data_from_mcp['exp_nov']=exp_nov

afle_mean = afle.groupby(['rater'])['euclid'].mean()

from scipy.stats import ranksums
import scipy.stats as stats

stats.mannwhitneyu(x=afle[afle['exp_nov']==0]['euclid'], y=afle[afle['exp_nov']==1]['euclid'], alternative = 'greater')
ranksums(afle[afle['exp_nov']==0]['euclid'], afle[afle['exp_nov']==1]['euclid'])
stats.ttest_ind(afle[afle['exp_nov']==0]['euclid'], afle[afle['exp_nov']==1]['euclid'])

afle_mean_coords = afle.groupby(['rater','fid'])['x','y','z'].mean().values

afle_mean_exp = afle.groupby(['rater','fid'])['euclid'].mean().values

import pingouin as pg


icc_overall=[]
for ifid in range(1,33):
	afle_data=afle[afle['fid']==ifid]
	icc_overall.append(icc(np.c_[afle_data[afle_data['rater']=='AT']['x'], afle_data[afle_data['rater']=='GG']['x'],
			  afle_data[afle_data['rater']=='MJ']['x'], afle_data[afle_data['rater']=='MA']['x'], afle_data[afle_data['rater']=='RC']['x']],'ICC(2,k)'))

afle[afle['exp_nov']==0]

icc_overall=[]
for ifid in range(1,33):
	iccx = pg.intraclass_corr(data=afle[(afle['fid']==ifid) ], targets='subject', raters='rater', ratings='x', nan_policy='omit').round(3)
	iccy = pg.intraclass_corr(data=afle[(afle['fid']==ifid) ], targets='subject', raters='rater', ratings='y', nan_policy='omit').round(3)
	iccz = pg.intraclass_corr(data=afle[(afle['fid']==ifid) ], targets='subject', raters='rater', ratings='z', nan_policy='omit').round(3)
	icc_overall.append([iccx.ICC[4],iccy.ICC[4],iccz.ICC[4]])

np.mean(icc_overall)

numpy.corrcoef(list1, list2)[0,1]

fig, axes = plt.subplots(5, 1)
max_val = 6.0
fid_cnt = 0
for irow in range(len(np.unique(afle['rater']))):
	afle_mean_rater = pd.DataFrame({})
	afle_mean_rater['error'] = afle_mean[fid_cnt:fid_cnt+32]
	afle_mean_rater['fid'] = np.unique(Data_comp['fid'])
	
	title = ' '.join(["Error Between", np.unique(afle['rater'])[irow], 'and group average'])
	afle_mean_rater.plot(kind='bar', x='fid', y='error', title =title, ax=axes[irow], legend=False, align='center', width=0.8)
	if irow == (len(raters)-1):
		axes[irow].set_xlabel("Fiducial", fontsize=12, fontweight = 'bold')
	else:
		axes[irow].xaxis.label.set_visible(False)
	axes[irow].set_ylabel("Error", fontsize=12, fontweight = 'bold')
	axes[irow].set_ylim([0,max_val])
	axes[irow].set_xticklabels(axes[irow].get_xticklabels(), rotation=45, fontweight = 'bold')
	
	fid_cnt += 32

fig.subplots_adjust(hspace=0.45, wspace=0.5, top=0.95, bottom=0.08, left=0.10, right=0.90)

if not show_only:
	output_temp = os.path.dirname(data_dir)
	output_dir = os.path.join(os.path.dirname(output_temp),'output', 'plots')
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	
	file_name = 'error_raters_group_average.png'
	
	fig = plt.gcf()
	fig.set_size_inches(16, 10)
	fig.savefig(os.path.join(output_dir, file_name), dpi=100)
	plt.close()

afle_mean_coords_x = afle_mean_coords[:,0]
afle_mean_coords_x = afle_mean_coords_x.reshape(5,32).T
afle_mean_coords_y = afle_mean_coords[:,1]
afle_mean_coords_y = afle_mean_coords_y.reshape(5,32).T
afle_mean_coords_z = afle_mean_coords[:,2]
afle_mean_coords_z = afle_mean_coords_z.reshape(5,32).T


rater_labels = np.unique(afle['rater'])

random.seed(1)
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(raters))]

min_val = -2.5
max_val = 2.5
major_ticks = np.linspace(min_val,max_val, 7)

fig = plt.figure(figsize=(18,8))
handles = {}
data_cnt = 0
for ifid in range(4):
	for jfid in range(8):
		ax = plt.subplot2grid((4, 8),(ifid,jfid), projection='3d')

		plot_title = 'Distance from the average of all raters'
		file_name = 'distance_from_all_raters_mean.png'
		tempData = [afle_mean_coords_x[data_cnt,:], afle_mean_coords_y[data_cnt,:], afle_mean_coords_z[data_cnt,:]]
		
		for i in range(len(rater_labels)): #plot each point + it's index as text above
			l1 = ax.scatter(tempData[0][i], tempData[1][i], tempData[2][i], marker='o', c=color[i],edgecolors='black', s=50, label=rater_labels[i])
			if rater_labels[i] not in handles:
				handles[rater_labels[i]] = l1
		 
		ax.plot((min_val, min_val), (min_val, min_val), (min_val-0.1, max_val+0.1), 'black', linewidth=1.0)
		
		ax.set_xlim([min_val, max_val])
		ax.set_ylim([min_val, max_val])
		ax.set_zlim([min_val, max_val])
		
		ax.set_xlabel('x', labelpad=-15, fontweight='bold')
		ax.set_ylabel('y', labelpad=-15, fontweight='bold')
		ax.set_zlabel('z', labelpad=-15, fontweight='bold')
		
		ax.get_xaxis().set_ticklabels([])
		ax.get_yaxis().set_ticklabels([])
		ax.zaxis.set_ticklabels([])
		ax.zaxis.set_major_locator(matplotlib.ticker.NullLocator())
		
		ax.set_xticks(major_ticks)
		ax.set_yticks(major_ticks)
		ax.set_zticks(major_ticks)
		
		ax.grid(which='major', alpha=0.5)
		
		ax.xaxis.pane.set_edgecolor('black')
		ax.yaxis.pane.set_edgecolor('black')
		ax.zaxis.pane.set_edgecolor('black')
		ax.xaxis.pane.set_alpha(1)
		ax.yaxis.pane.set_alpha(1)
		ax.zaxis.pane.set_alpha(1)
		ax.xaxis.pane.fill = False
		ax.yaxis.pane.fill = False
		ax.zaxis.pane.fill = False
				
		ax.view_init(elev=25, azim=44)
		
		ax.set_title(str(data_cnt+1) + ': ' + fid_dic[data_cnt+1], pad=5, fontweight='bold')

		data_cnt += 1
		
fig.subplots_adjust(hspace=0.04, wspace=0.02, top=0.90, bottom=0.06, left=0.02,right=0.92) 
plt.legend(handles=handles.values(), fontsize=12, bbox_to_anchor=[1.6, 2.5], handletextpad=0.05)
fig.suptitle(plot_title, y = 0.98, fontsize=14, fontweight='bold')

if not show_only:
	output_temp = os.path.dirname(data_dir)
	output_dir = os.path.join(os.path.dirname(output_temp), 'output', 'plots')
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
		
	plt.savefig(os.path.join(output_dir, file_name))
	plt.close()
	
#%%

plt.bar(np.arange(1,33,1),np.mean(afle_mean.reshape(5,32).T,1))
plt.xticks(np.arange(1,33,1), np.arange(1,33,1), rotation=45, fontweight = 'bold')
plt.xlabel("Fiducial", fontsize=12, fontweight = 'bold')
plt.ylabel("Error", fontsize=12, fontweight = 'bold')
plt.title('Average error across raters', fontsize=14, fontweight = 'bold')

if not show_only:
	output_temp = os.path.dirname(data_dir)
	output_dir = os.path.join(os.path.dirname(output_temp),'output', 'plots')
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	
	file_name = 'average_error_across_raters.png'
	
	fig = plt.gcf()
	fig.set_size_inches(14, 10)
	fig.savefig(os.path.join(output_dir, file_name), dpi=100)
	plt.close()

#%%


pal=sns.diverging_palette(h_neg=220, h_pos=10, s=50, l=50,sep=1,n=2,as_cmap=True)

fig = plt.figure(figsize=(12,10))
gs = gridspec.GridSpec(3, 10)

ax1 = fig.add_subplot(gs[0:1, :8])

plotData = {}
plotData['afid'] = np.repeat(list(range(1,33)),5).flatten()
plotData['AFLE'] = Rater_AFLE_mean.flatten()

sns.barplot(x='afid', y='AFLE', data=pd.DataFrame(plotData),ax=ax1, ci='sd',zorder=5, color='lightblue',errwidth=1.5,capsize = .3)
ax1.set_ylabel('ATLE (mm)', fontweight='bold',fontsize=18, labelpad=12)
ax1.set_ylim([0,5])
ax1.set_xlabel(None)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.tick_params(axis='both', which='major', labelsize=14)
ax1.text(-.07, 1,'a)', transform=ax1.transAxes, fontsize=18, fontweight='bold')

Rater_AFLE_norm = (Rater_AFLE-np.tile(min(Rater_AFLE.flatten()),Rater_AFLE.shape))/np.tile(max(Rater_AFLE.flatten())-min(Rater_AFLE.flatten()),Rater_AFLE.shape)
ax2 = fig.add_subplot(gs[1:, :])
sns.heatmap(Rater_AFLE, annot = False, linewidth=.5, linecolor='w', ax=ax2, cmap=pal, cbar_kws={"shrink": .7,"label":"ATLE"}, xticklabels=list(range(1,33)), vmin=0,vmax=5)
plt.gca().invert_yaxis()
font = FontProperties(weight='bold', size=18)
ax2.figure.axes[-1].yaxis.label.set_font_properties(font)

ax2.set_yticks([4.5,10,15,20,25,30,35])
ax2.yaxis.set_ticklabels([5,10,15,20,25,30,35])
ax2.set_ylabel('Subject', fontweight='bold',fontsize=18, labelpad=12)
ax2.set_xlabel('AFID', fontweight='bold',fontsize=18, labelpad=12)
ax2.tick_params(axis='both', which='major', labelsize=14)
ax2.text(-.07, 1,'b)', transform=ax2.transAxes, fontsize=18, fontweight='bold')

fig.suptitle("Mean anatomical target localization error", y = 0.98, fontsize=22, fontweight='bold')

plt.tight_layout()


#%%

data_dir_out = "/media/greydon/KINGSTON/phdCandidacy/thesis/imgs"

file_name="mean_ATLE_subject_space"
plt.savefig(os.path.join(data_dir_out, f"{file_name}.svg"),transparent=True)
plt.savefig(os.path.join(data_dir_out, f"{file_name}.png"),transparent=True,dpi=450)
plt.savefig(os.path.join(data_dir_out, f"{file_name}_white.png"),transparent=False,dpi=450)
plt.close()


#%%

pal=sns.diverging_palette(h_neg=220, h_pos=10, s=50, l=50,sep=1,n=2,as_cmap=True)

fig = plt.figure(figsize=(12,10))
gs = gridspec.GridSpec(3, 10)

ax1 = fig.add_subplot(gs[0:1, :8])

plotData = {}
plotData['afid'] = np.repeat(list(range(1,33)),5).flatten()
plotData['AFRE'] = MNI_AFLE_scan.flatten()

sns.barplot(x='afid', y='AFRE', data=pd.DataFrame(plotData),ax=ax1, ci='sd',zorder=5, color='lightblue',errwidth=1.5,capsize = .3)
ax1.set_ylabel('ATRE (mm)', fontweight='bold',fontsize=18, labelpad=12)
ax1.set_ylim([0,10])
ax1.set_xlabel(None)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.tick_params(axis='both', which='major', labelsize=14)
ax1.text(-.07, 1,'a)', transform=ax1.transAxes, fontsize=18, fontweight='bold')

MNI_AFLE_rater_norm = (MNI_AFLE_rater-np.tile(min(MNI_AFLE_rater.flatten()),MNI_AFLE_rater.shape))/np.tile(max(MNI_AFLE_rater.flatten())-min(MNI_AFLE_rater.flatten()),MNI_AFLE_rater.shape)

ax2 = fig.add_subplot(gs[1:, :])
sns.heatmap(MNI_AFLE_rater, annot = False, linewidth=.5, linecolor='w', ax=ax2, cmap=pal, cbar_kws={"shrink": .7,"label":"ATRE"}, xticklabels=list(range(1,33)), vmin=0,vmax=10)
plt.gca().invert_yaxis()
font = FontProperties(weight='bold', size=18)
ax2.figure.axes[-1].yaxis.label.set_font_properties(font)
ax2.set_yticks([4.5,10,15,20,25,30,35])
ax2.yaxis.set_ticklabels([5,10,15,20,25,30,35])
ax2.set_ylabel('Subject', fontweight='bold',fontsize=18, labelpad=12)
ax2.set_xlabel('AFID', fontweight='bold',fontsize=18, labelpad=12)
ax2.tick_params(axis='both', which='major', labelsize=14)
ax2.text(-.07, 1,'b)', transform=ax2.transAxes, fontsize=18, fontweight='bold')

fig.suptitle("Mean anatomical target registration error", y = 0.98, fontsize=22, fontweight='bold')

plt.tight_layout()


#%%

data_dir_out = "/media/greydon/KINGSTON/phdCandidacy/thesis/imgs"

file_name="mean_ATRE_mni_space"
plt.savefig(os.path.join(data_dir_out, f"{file_name}.svg"),transparent=True)
plt.savefig(os.path.join(data_dir_out, f"{file_name}.png"),transparent=True,dpi=450)
plt.savefig(os.path.join(data_dir_out, f"{file_name}_white.png"),transparent=False,dpi=450)
plt.close()


