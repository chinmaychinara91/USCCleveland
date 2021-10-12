
function done = SVReg_done_check(subbasename)
% figure out if SVReg has already been run for the subject, return true if
% it has, return false if not

% output here is used to skip over subject if they've been run already

    done = exist([subbasename, '.svreg.label.nii.gz'],'file');

end

