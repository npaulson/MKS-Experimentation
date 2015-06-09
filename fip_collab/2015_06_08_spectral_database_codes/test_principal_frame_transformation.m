clear; clc;

% generate a random 3x3 matrix with values ranging from -1 to 1. This
% represents some deformation gradient F
F = 2*(rand(3,3)-.5)

% F = [1,0,1;
%      0,0,0;
%      1,0,0];

% calculate the associated total strain tensor from F as the Cauchy-Green
% strain. This tensor is in the sample frame
et = 0.5*(F'*F-eye(3));

% find the deviatoric total strain tensor
et_ = et - (1/3)*trace(et)*eye(3);

% calculate the magnitude of the deviatoric total strain tensor
en = sqrt(sum(et_(:).^2));

% normalize the deviatoric total strain tensor
et_n = et_ / en

% find the principal strains 
[V,D] = eig(et_n);

% sort the principal strains in descending order
[et_i,indx] = sort([D(1,1),D(2,2),D(3,3)],'descend')

V = [V(:,indx(1)),V(:,indx(2)),V(:,indx(3))];

% determine the angle theta associated with the diagonal matrix of interest
theta1 = acos(sqrt(3/2)*et_i(1))+(pi/3);
theta2 = acos(sqrt(3/2)*et_i(2))-(pi/3);
theta3 = acos(-sqrt(3/2)*et_i(3));

et_ii = @(x) [sqrt(2/3)*cos(x-(pi/3)), ...
              sqrt(2/3)*cos(x+(pi/3)), ...
              -sqrt(2/3)*cos(x)];

et_ii(theta2)

% demonstrate the transformation from et_n to the principal frame using 
% eigenvectors
disp(V'*et_n*V)

% find the set of euler angle associated with the transformation from the
% principal to crystal reference frames <-- ?
euler = rotmat2euler(V);
