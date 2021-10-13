
function brainsuite_process_all()
    configfile = 'config_brainsuite.ini';
    t1file = 't1list.txt';

    filetext = fileread(t1file);
    t1subs = splitlines(filetext);

    for j = 1:length(t1subs)

        [orig_pth,subbasename,ext] = fileparts(t1subs{j});
        if strfind(t1subs{j},'C:')
            tempdir = orig_pth;
            newt1file = fullfile(tempdir,[subbasename,ext]);      
        else
            tempdir = tempname;
            mkdir(tempdir);
            newt1file = fullfile(tempdir,[subbasename,ext]);  
            copyfile(t1subs{j}, newt1file);
        end


        [pth,subbasename,ext] = fileparts(newt1file);


        if strcmp(subbasename(end-2:end),'nii')
            subbasename = fullfile(pth,subbasename(1:end-4));
        else
            subbasename = fullfile(pth,subbasename);
        end


        if SVReg_done_check(subbasename)
            fprintf('BrainSuite processing is already done for %s',subbasename);
            continue;
        end

        brainsuite_process_subject(configfile,subbasename);

        if ~strfind(t1subs{j},'C:')
            copyfile(tempdir,orig_pth);
            rmdir(tempdir, 's');
        end
    end
