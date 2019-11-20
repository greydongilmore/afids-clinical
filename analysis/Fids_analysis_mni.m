clear
clc
fclose('all');

data_dir = 'D:\School\Residency\Research\FIDs Study\Github\afids_parkinsons\input\input_mniTransform';
patient_files = dir(fullfile(data_dir));
patient_files = patient_files(~[patient_files.isdir]);

for data = 1:length(patient_files)
    [data_table] = read_fcsv_mni(patient_files(data));
    df_raters{data} = data_table;
end


Data = vertcat(df_raters{:});

% List of raters
raters = ["AT";"GG";"MA";"MJ";"RC"];

% Generates arrays for subjects completed by each rater
Sub = {};
Size_sub = [];
sub_ignore = [];
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

%% Generate mean coordinates for gold standard + non-gold standard raters

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
