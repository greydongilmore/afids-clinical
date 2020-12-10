
%
%   Loading Jon's MNI standard
%
data_dir = 'C:\Users\greydon\Documents\GitHub\afids_parkinsons\input\mni';
patient_files = dir(fullfile(data_dir));
patient_files = patient_files(~[patient_files.isdir] & ~endsWith({patient_files.name},'.mat'));

filename = patient_files(1);

%--- Import the data
fileID = fopen(fullfile(filename.folder, filename.name));
data = textscan(fileID,'%s %f %f %f %f %f %f %f %f %f %f %f %s %s', 'Delimiter', ',','headerLines', 3, 'CollectOutput', 1);

%--- Create table
data_table = table;

%--- Allocate imported array to column variable names
data_table.fid = data{1,2}(:,11);
data_table.X = data{1,2}(:,1);
data_table.Y = data{1,2}(:,2);
data_table.Z = data{1,2}(:,3);
data_table.rater = repmat(100, length(data{1,2}), 1);

mni_jon_standard = table2array(data_table);


%
%   Loading Raters MNI standard
%
data_dir = 'C:\Users\greydon\Documents\GitHub\afids_parkinsons\input\raters_mni';
patient_files = dir(fullfile(data_dir));
patient_files = patient_files(~[patient_files.isdir] & ~endsWith({patient_files.name},'.mat'));

X = zeros(32,length(patient_files));
Y = zeros(32,length(patient_files));
Z = zeros(32,length(patient_files));
for idata = 1:length(patient_files)
    %--- Import the data
    fileID = fopen(fullfile(patient_files(idata).folder, patient_files(idata).name));
    data = textscan(fileID,'%s %f %f %f %f %f %f %f %f %f %f %f %s %s', 'Delimiter', ',','headerLines', 3, 'CollectOutput', 1);

    X(:,idata) = data{1,2}(:,1);
    Y(:,idata) = data{1,2}(:,2);
    Z(:,idata) = data{1,2}(:,3);
end

mni_rater_standard = [[1:32].',mean(X,2), mean(Y,2), mean(Z,2), repmat(100, 32,1)];

