% D is the stretching tensor
% D = [.10,.21,.15;
%      .23,.26,.05;
%      .11,.15,.28];
D = rand(3);
D = D'*D;
 
% D = [exp(-.1/2) ,0 ,0; 0, exp(-.1/2), 0; 0 ,0 , exp(.1)]

D = D - eye(3)*trace(D)/3

D_sq = D.^2;

% nrm is the norm of E_d
nrm = sqrt(sum(D_sq(:)));

% E_d_nrm is the E_d normalized
D_nrm = D / nrm

% E_dp is the E_d in the principal frame
[~, D_p] = eig(D_nrm)

% display the trace of E_dp
D_p_trace = trace(D_p)

theta1 = acos(sqrt(3/2)*D_p(1,1))+pi/3
theta2 = acos(sqrt(3/2)*D_p(2,2))-pi/3
theta3 = acos(-sqrt(3/2)*D_p(3,3))
