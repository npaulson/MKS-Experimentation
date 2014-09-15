load euler_GSH_200cal.mat
load euler_200cal.mat

% find the linear indicies of the NaN elements in the GSH orientation array
ind = find(isnan(euler_GSH));

% convert the linear indices to 3 columns of subscripts
[sub1,sub2,sub3] = ind2sub(size(euler_GSH),ind);

% append these column vectors to have an array of all the subscripts
% describing the locations of NaN elements in the GSH orientation array
sub = [sub1 sub2 sub3];

% find the euler angles in the original orientation array corresponding
% with the indices of the NaN elements in the GSH orientation array
bad_euler_angles = euler_200cal(sub(:,1),sub(:,2),:);