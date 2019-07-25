
data_dir = 'F:/projects/templateProjects/32FiducialBIDS_PDPatients/analysisScripts/input/input_fid';

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
for r = 1:length(raters)
    idx = ismember(Data.rater, raters(r));
    sub_temp = Data.subject(idx,:);
    Sub{1,r} = unique(Data.subject(idx,:), 'rows');
end

% Subjects completed by all raters
Sub_Comp = intersect(intersect(intersect(Sub{1,1},Sub{1,2}),Sub{1,3}), Sub{1,4});

% Table only containing subjects completed by all raters
Data_comp = Data(ismember(Data.subject, Sub_Comp),:);

% Generate an array for each rater with x,y,z coordinates. 4D array: fids x
% coordinates x subjects x raters. 

Tot_Data = zeros(32,5,length(Sub_Comp), length(raters));

for r = 1:length(raters)
     temp_data = table2array(Data_comp(ismember(Data_comp.rater, raters(r)),[1:4,6]));
     for s = 1:length(Sub_Comp)
         Tot_Data(:,:,s,r) = temp_data(ismember(temp_data(:,5),(Sub_Comp(s))),:);
     end
end


%% Difference between raters

% Define the 2 raters
r1 = 1;
r2 = 2;

Coor_Diff = squeeze(Tot_Data(:,:,:,r1) - Tot_Data(:,:,:,r2));


%% Future plans

% Built into Coor_Diff are columns 1 and 5, if they are 0 then the same
% fidicual (column 1) and subject (column 5) are compared.

% Add an if statement for red flags if differences in x y or z coordinates
% are greater than a certain value (3 mm?)

% Calcuate statistics (mean differences, SD, SE, IRR, etc).



