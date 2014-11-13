function image_register_save_as_multitiff

%% Register images in X-Y
% User Input
Data_Folder = '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/141010 Fish2 Deconvolved/';
Result_Folder_Name = '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/141010 Fish2 Deconvolved/'; %Result FOlder name
Stim = {'30ugHAM', '3ugHAS', '30ugHAL'};
num_z = 27;
num_t = 121;


%% Code
for s = 1:length(Stim) %Loop through each stimulus
    
    Stim_Folder = [Data_Folder, Stim{s}, filesep];
    Result_Folder = [Result_Folder_Name, Stim{s}, filesep, 'Registered', filesep]; %Result folder variable
    
    if ~isdir(Result_Folder)
        mkdir(Result_Folder)
    end
    
    for z = 1:num_z %Loop through each z stack
        Stim_Folder_Base = [Data_Folder, Stim{1}, filesep]; % Use these two lines if one stimulus is to be used as template.
        base = mat2gray(imread([Stim_Folder_Base, '10_', Stim{1},'_T001.tif'], z));

        % base = mat2gray(imread([Stim_Folder, '10_', Stim{1},'_T001.tif'], z)); % Uncomment this line if first time point from eahc stimulus is to be used as template.
        
        for t = 1:num_t
            %Loop through each time point
            
            unregistered = mat2gray(imread([Stim_Folder, '10_', Stim{s},'_T', sprintf('%03.0f', t), '.tif'], z));
            
            c = normxcorr2(base,unregistered); %Calculate correlation between base and unregistered image
            
            %% Register image by calculating shift
            [y,x] = find(c == max(c(:)),1);
            
            [yc,xc] = size(unregistered);
            
            %Find offset
            yoff = y - yc;
            xoff = x - xc;
            
            disp(['Stim...', Stim{s}, ' Stack...', int2str(z), ' Time...', int2str(t), ' X offset...', num2str(xoff), ' Y offset...', num2str(yoff)]);
            
            if xoff < 0
                xoffa = abs(xoff)+1;
            else
                xoffa = xoff;
            end
            if yoff < 0
                yoffa = abs(yoff)+1;
            else
                yoffa = yoff;
            end
            
            % Adjust according to peak correlation
            registered = zeros(yc+abs(yoffa), xc+abs(xoffa));
            
            if xoff~=0 && yoff==0
                if xoff < 0
                    registered(:, xoffa:(xc+xoffa-1)) = unregistered;
                    registered(:,end-xoffa+1:end) = [];
                else
                    registered(:, 1:xc) = unregistered;
                    registered(:,1:xoffa) = [];
                end
            elseif xoff==0 && yoff~=0
                if yoff < x
                    registered(yoffa:(yc+yoffa-1), :) = unregistered;
                    registered(end-yoffa+1:end,:) = [];
                else
                    registered(1:yc, :) = unregistered;
                    registered(1:yoffa,:) = [];
                end
            elseif xoff~=0 && yoff~=0
                if xoff < 0 && yoff < 0
                    registered(yoffa:(yc+yoffa-1), xoffa:(xc+xoffa-1)) = unregistered;
                    registered(end-yoffa+1:end,:) = [];
                    registered(:,end-xoffa+1:end) = [];
                elseif xoff > 0 && yoff > 0
                    registered(1:yc, 1:xc) = unregistered;
                    registered(1:yoffa,:) = [];
                    registered(:,1:xoffa) = [];
                elseif xoff < 0 && yoff > 0
                    registered(1:yc, xoffa:(xc+xoffa-1)) = unregistered;
                    registered(1:yoffa,:) = [];
                    registered(:,end-xoffa+1:end) = [];
                elseif xoff > 0 && yoff < 0
                    registered(yoffa:(yc+yoffa-1), 1:xc) = unregistered;
                    registered(end-yoffa+1:end,:) = [];
                    registered(:,1:xoffa) = [];
                end
            elseif xoff==0 && yoff==0
                registered = im2uint8(unregistered);
            end
            
            
            %% Save image
            if t == 1
                imwrite(registered,[Result_Folder, 'Registered_Z=',int2str(z), '.tif'],'tif');
            else
                imwrite(registered,[Result_Folder, 'Registered_Z=',int2str(z), '.tif'],'tif','WriteMode','append');
            end
            
        end
        
    end
end

