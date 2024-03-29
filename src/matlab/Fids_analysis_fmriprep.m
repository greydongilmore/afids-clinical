clear
clc
fclose('all');

Dir = 'D:\School\Residency\Research\FIDs Study\Github\afids_parkinsons';
% Dir = 'C:\Users\moham\Documents\GitHub\afids_parkinsons\input';

% transf2use '_nlin' to analyze non-linear transformation, '_lin' to
% analyze linear transformation
data_dir = ([Dir, '\data\input_fid_MNI_linear_combined']);
transf2use = '_lin';

sub_ignore = [146];

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
        fileN = fileN(contains({fileN.name},transf2use));
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

%% Load MNI mean data from Jon's paper (i.e. gold standard MNI (gs MNI))

% Generate array with fid number, x, y and z coordinates for MNI mean
load([Dir, '\data\fid_standards\MNI152NLin2009cAsym_standard_afids\MNI152NLin2009cAsym_standard.mat']);
MNI_mean = mni_jon_standard(:,1:4);

% Difference between each fiducial placed and gs MNI + euclidian distance

MNI_Diff = Tot_Data(:,1:4,:,:) - repmat(MNI_mean,1,1,length(Sub_Comp),length(raters));
MNI_AFLE = squeeze(sqrt(MNI_Diff(:,2,:,:).^2 + MNI_Diff(:,3,:,:).^2 + MNI_Diff(:,4,:,:).^2));

% AFLE from gs MNI across raters, individual scans and raters + fids
MNI_AFLE_rater = squeeze(mean(MNI_AFLE,3));
MNI_AFLE_scan = squeeze(mean(MNI_AFLE,2));
MNI_AFLE_total = squeeze(mean(MNI_AFLE_rater,1));



%% Generate mean coordinates for gold standard + non-gold standard raters

%## Load Raters MNI standard
patient_files = dir(fullfile([Dir, '\data\fid_standards\MNI152NLin2009bAsym_rater_standard']));
patient_files = patient_files(endsWith({patient_files.name},'.mat'));

load([patient_files.folder , '\' , patient_files.name]);
mni_rater_standard_rep = repmat(mni_rater_standard,1,1,length(Sub_Comp),length(raters));
mni_rater_standard_diff = Tot_Data - mni_rater_standard_rep;
mni_rater_standard_eudiff = sqrt(mni_rater_standard_diff(:,2,:,:).^2 + mni_rater_standard_diff(:,3,:,:).^2 + mni_rater_standard_diff(:,4,:,:).^2);
mni_rater_standard_AFLE_mean = squeeze(mean(mni_rater_standard_eudiff,3));
mni_rater_standard_AFLE_SD = squeeze(std(mni_rater_standard_eudiff,0,[3 4]));

% Preliminary figure
for fid = 1:32
    plot3(mni_rater_standard_diff(fid,2),mni_rater_standard_diff(fid,3),mni_rater_standard_diff(fid,4),'o','Color','b','MarkerSize',8,'MarkerFaceColor',[217/255,1,1])
%     text(mni_rater_standard_diff(fid,2),mni_rater_standard_diff(fid,3),mni_rater_standard_diff(fid,4),num2str(fid),'FontSize',11,'FontWeight','bold')
    hold on
    
    plot3(MNI_Diff(fid,2),MNI_Diff(fid,3),MNI_Diff(fid,4),'o','Color','y','MarkerSize',8,'MarkerFaceColor',[217/255,1,1])
%     text(mni_jon_standard_diff(fid,2),mni_jon_standard_diff(fid,3),mni_jon_standard_diff(fid,4),num2str(fid),'FontSize',11,'FontWeight','bold')
    
    xyz = vertcat([mni_rater_standard_diff(fid,2),mni_rater_standard_diff(fid,3),mni_rater_standard_diff(fid,4)],...
    [MNI_Diff(fid,2),MNI_Diff(fid,3),MNI_Diff(fid,4)]);
    plot3(xyz(:,1),xyz(:,2), xyz(:,3),'k-')
    eudiff = sqrt((xyz(2,1)-xyz(1,1)).^2 + (xyz(2,2)-xyz(1,2)).^2 + (xyz(2,3)-xyz(1,3)).^2);
    text(sum(xyz(:,1))/2, sum(xyz(:,2))/2, sum(xyz(:,3))/2, [num2str(fid), ': ', num2str(eudiff)],'FontSize',11,'FontWeight','bold')
end
grid on
axis equal
xl = max(abs(xlim()));xl = linspace(xl,-xl,2);
yl = max(abs(ylim()));yl = linspace(yl,-yl,2);
zl = max(abs(zlim()));zl = linspace(zl,-zl,2);
line(2*xl, [0,0], [0,0], 'LineWidth', 1, 'Color', 'k');
line([0,0], 2*yl, [0,0], 'LineWidth', 1, 'Color', 'k');
line([0,0], [0,0], 2*zl, 'LineWidth', 1, 'Color', 'k');

xlabel('X coord')
ylabel('Y coord')
zlabel('Z coord')



GS_raters = ["GG", "MA"];

GS_mean = squeeze(mean(Tot_Data(:,:,:,ismember(raters,GS_raters)),4));
NGS_mean =  squeeze(mean(Tot_Data(:,:,:,~ismember(raters,GS_raters)),4));
Tot_mean = squeeze(mean(Tot_Data(:,:,:,:),4));

% Outliers

Tot_diff = Tot_Data - repmat(Tot_mean,1,1,1,length(raters));
Tot_eudiff = sqrt(Tot_diff(:,2,:,:).^2 + Tot_diff(:,3,:,:).^2 + Tot_diff(:,4,:,:).^2);
Outlier = Tot_eudiff > 10;

% Diff between GS vs NGS

GS_Diff = GS_mean - NGS_mean;
GS_error_rate = sqrt(GS_Diff(:,2,:).^2 + GS_Diff(:,3,:).^2 + GS_Diff(:,4,:).^2);

% Mean error between GS and NGS across subjects

Mean_GS_Diff = mean(GS_Diff,3);

% Anatomical Fiducial Localization Error (AFLE) calculations 

% Mean AFLE across raters

Rater_AFLE_mean = squeeze(mean(Tot_eudiff,3));
Rater_AFLE_SD = squeeze(std(Tot_eudiff,0,3));

%Total mean AFLE

Total_AFLE_mean = squeeze(mean(Rater_AFLE_mean,2));
Total_AFLE_SD = squeeze(std(Tot_eudiff,0,[3 4]));

% Preliminary figure
for fid = 1:32
    plot3(Mean_GS_Diff(fid,2),Mean_GS_Diff(fid,3),Mean_GS_Diff(fid,4),'o','Color','b','MarkerSize',10,'MarkerFaceColor',[217/255,1,1])
    text(Mean_GS_Diff(fid,2),Mean_GS_Diff(fid,3),Mean_GS_Diff(fid,4),num2str(fid),'FontSize',14,'FontWeight','bold')
    hold on
end
grid on
axis equal
xl = max(abs(xlim()));xl = linspace(xl,-xl,2);
yl = max(abs(ylim()));yl = linspace(yl,-yl,2);
zl = max(abs(zlim()));zl = linspace(zl,-zl,2);
line(2*xl, [0,0], [0,0], 'LineWidth', 1, 'Color', 'k');
line([0,0], 2*yl, [0,0], 'LineWidth', 1, 'Color', 'k');
line([0,0], [0,0], 2*zl, 'LineWidth', 1, 'Color', 'k');

xlabel('X coord')
ylabel('Y coord')
zlabel('Z coord')


%% Plot matrix of AFRE, mean AFRE across raters for all subjects and AFIDs

%Mean AFRE across raters (using rater standard)

Rater_AFRE = (squeeze(mean(mni_rater_standard_eudiff,4)))';
Rater_AFRE(:,33) = 0;
Rater_AFRE(length(Sub_Comp)+1,:) = 0;
pcolor(Rater_AFRE);
colormap(parula);
colorbar;
caxis([0 10]);
xticks(0.5:1:32.5);
xticklabels(0:1:32);
yticks(0.5:5:40.5);
yticklabels(0:5:40);

% Bar plot + SD

AFRE_mean = mean(mni_rater_standard_AFLE_mean,2);

bar(1:32, AFRE_mean);
hold on
er = errorbar(1:32, AFRE_mean, [], mni_rater_standard_AFLE_SD);
er.Color = [0 0 0];                            
er.LineStyle = 'none';
xticks([])
yticks(0:2:12);
yticklabels(0:2:12);
