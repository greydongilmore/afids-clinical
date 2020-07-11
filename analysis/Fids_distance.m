clear
clc
fclose('all');

% data_dir = 'C:\Users\greydon\Documents\github\afids_parkinsons\input\input_fid';
% data_dir = 'D:\School\Residency\Research\FIDs Study\Github\afids_parkinsons\input\input_fid';
data_dir = 'C:\Users\moham\Documents\GitHub\afids_parkinsons\input\input_fid';

sub_ignore = [];

raters = dir(data_dir);
raters = raters([raters.isdir] & ~strcmp({raters.name},'.') & ~strcmp({raters.name},'..'));
df_raters = cell(1,1);
iter_cnt = 1;
for irater = 1:length(raters)
    patient_files = dir(fullfile(data_dir,raters(irater).name));
    patient_files = patient_files([patient_files.isdir] & ~strcmp({patient_files.name},'.') & ~strcmp({patient_files.name},'..'));
    for isub = 1:length(patient_files)
        fileN = dir(fullfile(data_dir,raters(irater).name, patient_files(isub).name));
        fileN = fileN(~strcmp({fileN.name},'.') & ~strcmp({fileN.name},'..'));
        [data_table] = read_fcsv(fileN, raters(irater).name, patient_files(isub).name);
        df_raters{iter_cnt} = data_table;
        iter_cnt = iter_cnt + 1;
    end
end

Data = vertcat(df_raters{:});

% List of raters
raters = string(unique(Data.rater,'rows'));

% Generates arrays for subjects completed by each rater
Sub = {};
Size_sub = [];
for r = 1:length(raters)
    idx = ismember(Data.rater, raters(r));
    sub_temp = unique(Data.subject(idx,:), 'rows');
    if ~isempty(sub_ignore)
        sub_temp = sub_temp(~ismember(sub_temp, sub_ignore));
    end
    Sub{1,r} = sub_temp(~ismember(sub_temp, sub_ignore));
    Size_sub(r) = length(Sub{1,r});
end

% Subjects completed by all raters
[B,I] = sort(Size_sub, 'descend');
Sub = Sub(I);
Sub_Comp = intersect(Sub{1,1},Sub{1,2});
for irate = 2:length(raters)
    Sub_Comp = intersect(Sub_Comp,Sub{1,irate});
end

% Table only containing subjects completed by all raters
Data_comp = Data(ismember(Data.subject, Sub_Comp),:);

% Generate an array for each rater with x,y,z coordinates. 4D array: fids x
% coordinates x subjects x raters. 
Tot_Data = zeros(32,5,length(Sub_Comp), length(raters));
for r = 1:length(raters)
     temp_data = table2array(Data_comp(ismember(Data_comp.rater, raters(r)),[1:4,6]));
     for s = 1:length(Sub_Comp)
         tempData = temp_data(ismember(temp_data(:,5),(Sub_Comp(s))),:);
         [~,idx] = sort(tempData(:,1)); % sort just the first column
         Tot_Data(:,:,s,r) = tempData(idx,:);
     end
end


%% Calculate distance between all fids for PD patients. Generates a 32x32 table with pairwise distance between each fid.

Mean_Coor_PD = squeeze(mean(Tot_Data,4));

for s = 1:length(Sub_Comp)
    for fid = 1:32
        for fid2 = 1:32
            Dist_PD(fid,fid2,s) = sqrt(sum((Mean_Coor_PD(fid,2:4,s)- Mean_Coor_PD(fid2,2:4,s)).^2));
        end
    end
end
        
Mean_Dist_PD = squeeze(mean(Dist_PD,3));
SD_Dist_PD = squeeze(std(Dist_PD,0,3));

%% Load OASIS data

data_dir = 'C:\Users\moham\Documents\GitHub\afids_parkinsons\input\OASIS-1';

patient_files = dir(fullfile(data_dir));
patient_files = patient_files(~[patient_files.isdir]);

for data = 1:length(patient_files)
    [data_table] = read_fcsv_oas(patient_files(data));
    df_raters_oas{data} = data_table;
end

Data = vertcat(df_raters_oas{:});

Oas_Data_temp = zeros(32,5,length(patient_files));
Oas_Data_temp = table2array(Data(:,1:5));

Oas_sub = unique(Oas_Data_temp(:,5));

% Geerate array of OASIS coordianates placed, 3D array: fids x coordinates
% x subject

Oas_Data = zeros (32, 5, length(Oas_sub));

for s = 1:length(Oas_sub)
         Oas_Data(:,:,s) = Oas_Data_temp(ismember(Oas_Data_temp(:,5),(Oas_sub(s))),:);
end

%% Calculate distance between all fids for OASIS subjects. Generates a 32x32 table with pairwise distance between each fid.

for s = 1:length(Oas_sub)
    for fid = 1:32
        for fid2 = 1:32
            Dist_Oas(fid,fid2,s) = sqrt(sum((Oas_Data(fid,2:4,s)- Oas_Data(fid2,2:4,s)).^2));
        end
    end
end
        
Mean_Dist_Oas = squeeze(mean(Dist_Oas,3));
SD_Dist_Oas = squeeze(std(Dist_Oas,0,3));


%% Plot matrix of pairwise distance

%PD
Mean_Dist_PD(33,33) = 0;
pcolor(Mean_Dist_PD);
colorbar;
colormap(jet);
caxis([0 100]);
xticks(0.5:1:32.5);
xticklabels(0:1:32);
yticks(0.5:1:32.5);
yticklabels(0:1:32);

%Oas
Mean_Dist_Oas(33,33) = 0;
pcolor(Mean_Dist_Oas);
colorbar;
colormap(jet);
caxis([0 100]);
xticks(0.5:1:32.5);
xticklabels(0:1:32);
yticks(0.5:1:32.5);
yticklabels(0:1:32);

% Difference between Oasis subjects and PD patients
Mean_Diff_Dist = Mean_Dist_Oas - Mean_Dist_PD;
pcolor(Mean_Diff_Dist);
colorbar;
colormap(jet);
caxis([-5 5]);
xticks(0.5:1:32.5);
xticklabels(0:1:32);
yticks(0.5:1:32.5);
yticklabels(0:1:32);

% T test between PD and OAS distances

Ttest_p = zeros(32,32);
Ttest_h = zeros(32,32);

% Number of comparisons + Bonferroni correction
Comp = 32*31/2;
Bon_p = 0.05/Comp;

for fid = 1:32
    for fid2 = 1:32
        [Ttest_h(fid,fid2),Ttest_p(fid,fid2)] = ttest2(Dist_Oas(fid,fid2,:),Dist_PD(fid,fid2,:),'Vartype','unequal','Alpha',Bon_p);
    end
end

Ttest_p(33,33) = 0;
Ttest_h(33,33) = 0;
pcolor(Ttest_h);
colorbar;
caxis([0 1]);
xticks(0.5:1:32.5);
xticklabels(0:1:32);
yticks(0.5:1:32.5);
yticklabels(0:1:32);


%% Generate table of sig distances

% Goal to generate table of sig distances, with following columns - Fid 1,
% Fid 2, PD distance, PD SD, Oas distance, Oas SD, p-val


%coordinates of sig values

[sig_coor(:,2),sig_coor(:,1)] = find(Ttest_h==1);

for c = 1:length(sig_coor)
    sig_coor(c, 3) = Mean_Dist_PD(sig_coor(c,1),sig_coor(c,2));
    sig_coor(c, 4) = SD_Dist_PD(sig_coor(c,1),sig_coor(c,2));
    sig_coor(c, 5) = Mean_Dist_Oas(sig_coor(c,1),sig_coor(c,2));
    sig_coor(c, 6) = SD_Dist_Oas(sig_coor(c,1),sig_coor(c,2));
    sig_coor(c, 7) = Ttest_p(sig_coor(c,1),sig_coor(c,2));
end






