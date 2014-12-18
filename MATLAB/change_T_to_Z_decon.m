function change_T_to_Z_decon

%% Change t to Z planes for deconvolved data

% User defined parameters
Data_Folder = '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/';
Result_Folder_Name =  '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/'; %Result Folder name
Stim = {'3ugHAS'};
num_z = 27;
num_t = 121;

%Loop through and create Z planes from t
for s = 1:length(Stim) %Loop through each stimulus
    
    Stim_Folder = [Data_Folder, Stim{s}, filesep];
    Result_Folder = [Result_Folder_Name, Stim{s}, filesep, 'Z', filesep]; %Result folder variable
    
    if ~isdir(Result_Folder)
        mkdir(Result_Folder)
    end
    
    for t = 1:num_t
        for z = 1:num_z
            Image1 = mat2gray(imread([Stim_Folder,'10_',Stim{s},'_T',sprintf('%03.0f', t),'.tif'], z));
            Image2 = im2uint8(Image1);
            if t == 1
                imwrite(Image2,[Result_Folder, 'Z=',int2str(z), '.tif'],'tif');
            else
                imwrite(Image2,[Result_Folder, 'Z=',int2str(z), '.tif'],'tif','WriteMode','append');
            end
        end
    end
    
end
