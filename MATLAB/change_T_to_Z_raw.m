function change_T_to_Z_raw

%% Change t to Z planes for raw non-deconvolved data

% User defined parameters
Data_Folder = '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/';
Result_Folder_Name =  '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/'; %Result Folder name
Stim = {'0.3ugHAL'};
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
        disp(['Creating Z for t= ', int2str(t)])
        
        for z = 1:num_z
            Image1 = im2uint8(imread([Stim_Folder,Stim{s},'_t',sprintf('%01.0f', t),'.tif'], z));
            
            if t == 1
                imwrite(Image1,[Result_Folder, 'Z=',int2str(z), '.tif'],'tif');
            else
                imwrite(Image1,[Result_Folder, 'Z=',int2str(z), '.tif'],'tif','WriteMode','append');
            end
        end
    end
    
end
