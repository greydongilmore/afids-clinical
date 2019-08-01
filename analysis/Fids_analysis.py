# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import random
plt.rcdefaults()
plt.rc('xtick.major', size = 0, width=0)
plt.rc('ytick.major', size = 0, width=0)

data_dir = r'/home/ggilmore/Documents/GitHub/afids_parkinsons/input/input_fid'
data_dir = r'C:\Users\Greydon\Documents\github\afids_parkinsons\input\input_fid'

sub_ignore = [149,150]

def plot_fiducials(data, expert_mean, data_dir,analysis=2):
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
            tempData = data[data['fid'].isin([data_cnt])]
            rater_labels = tempData['rater'].values
            if analysis == 1:
                plot_title = 'Distance from the average of expert raters'
                file_name = 'distance_from_expert_mean.png'
                tempData = tempData.loc[:,'x':'z'].values - expert_mean.loc[expert_mean['fid'].isin([data_cnt]),'x':'z'].values
            elif analysis == 2:
                plot_title = 'Distance from the average of all raters'
                file_name = 'distance_from_all_raters_mean.png'
                tempData = tempData.loc[:,'x':'z'].values - tempData.loc[:,'x':'z'].mean().values
            
            for i in range(len(rater_labels)): #plot each point + it's index as text above
                l1 = ax.scatter(tempData[i,0], tempData[i,1], tempData[i,2], marker='o', c=color[i],edgecolors='black', s=50, label=rater_labels[i])
                if rater_labels[i] not in handles:
                    handles[rater_labels[i]] = l1
             
            ax.plot((min_val,min_val), (min_val,min_val), (min_val-0.1,max_val+0.1), 'black', linewidth=1.0)
            
            ax.set_xlim([min_val,max_val])
            ax.set_ylim([min_val,max_val])
            ax.set_zlim([min_val,max_val])
            
            ax.set_xlabel('x',labelpad=-15, fontweight='bold')
            ax.set_ylabel('y',labelpad=-15, fontweight='bold')
            ax.set_zlabel('z',labelpad=-15, fontweight='bold')
            
            ax.get_xaxis().set_ticklabels([])
            ax.get_yaxis().set_ticklabels([])
            ax.get_zaxis().set_ticklabels([])
            ax.get_zaxis().set_major_locator(matplotlib.ticker.NullLocator())
            
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
            
            ax.set_title(str(data_cnt), pad=5, fontweight='bold')
    
            data_cnt += 1
            
    fig.subplots_adjust(hspace=0.04, wspace=0.02, top=0.90, bottom=0.06, left=0.02,right=0.92) 
    plt.legend(handles=handles.values(), fontsize=12, bbox_to_anchor=[1.6, 2.5], handletextpad=0.05)
    fig.suptitle(plot_title, y = 0.98, fontsize=14, fontweight='bold')
    
    output_temp = os.path.dirname(data_dir)
    output_dir = os.path.join(os.path.dirname(output_temp),'output', 'plots')
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    plt.savefig(os.path.join(output_dir, file_name))
    plt.close()

#%%
raters = os.listdir(data_dir)
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
	sub_temp = [x for x in sub_temp if x not in sub_ignore]
	data_table = pd.DataFrame({'rater': np.repeat(r,len(sub_temp)), 'subject':sub_temp})
	Sub = pd.concat([Sub, data_table], axis = 0, ignore_index=True)
	size.append((r,len(sub_temp)))

size = sorted(size, key=lambda tup: tup[1], reverse=True)
Sub_Comp = list(set(Sub[Sub['rater']==size[0][0]]['subject'].values) & 
				set(Sub[Sub['rater']==size[1][0]]['subject'].values))
for irate in range(2,len(raters)):
    Sub_Comp = list(set(Sub_Comp) & set(Sub[Sub['rater']==size[irate][0]]['subject'].values))


Data_comp = rater_final[rater_final['subject'].isin(Sub_Comp)]
Data_comp = Data_comp.sort_values(['rater','subject', 'fid'], ascending=[True, True,True])


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

plot_fiducials(rater_mean, GS_total_mean, data_dir, 1)
plot_fiducials(rater_mean, GS_total_mean, data_dir, 2)

