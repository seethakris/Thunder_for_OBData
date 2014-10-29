function convert_to_multitiff

%% Convert to multitiff
% User Input
Data_Folder = '~/Desktop/Michelle_OB_Thunder/Data/141011_Fish3/';
Stim = {'30ugHAM', '3ugHAS'};
num_z = 27;
num_t = 121;
delete_flag = 0; %0 - if you dont want to delete the single tiffs, 1 if you do. The files will get permenantely deleted after all multitiffs are saved

%Pick up data from the respective folders that has been registered
%Convert to multitiffs for each Z with number of time points

for s = 1:length(Stim) %Loop through each stimulus
    Stim_Folder = [Data_Folder, Stim{s}, filesep, 'Registered', filesep];
    for z = 1:num_z
        for t = 1:num_t
            %Read image
            disp(['Stim...', Stim{s}, ' Stack...', int2str(z), ' Time...', int2str(t)]);
            
            image1 = imread([Stim_Folder, Stim{s}, '_Z', int2str(z), '_T', int2str(t), '.tif']);
            
            %If t = 1 create new file, else append to multitiff
            if t==1
                imwrite(image1,[Stim_Folder, filesep,'Registered_Z=',int2str(z)],'tif');
            else
                imwrite(image1,[Stim_Folder, filesep,'Registered_Z=',int2str(z)],'tif', 'WriteMode','append');
            end
            
        end
    end
end

%Delete single tiffs

if delete_flag == 1
    for s = 1:length(Stim) %Loop through each stimulus
        Stim_Folder = [Data_Folder, Stim{s}, filesep, 'Registered', filesep];
        for z = 1:num_z
            for t = 1:num_t
                %Read image
                disp('Deleting...'); 
                delete([Stim_Folder, Stim{s}, '_Z', int2str(z), '_T', int2str(t), '.tif']);
            end
        end
    end
end


