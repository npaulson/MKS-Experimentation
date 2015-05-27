% F is the deformation gradient
F = [.10,.21,.15;
     .23,.26,.05;
     .11,.15,.28]

% F = [exp(-.1/2) ,0 ,0; 0, exp(-.1/2), 0; 0 ,0 , exp(.1)]
% 
% F_d = F - eye(3)*trace(F)/3
% 
% [~, F_dp] = eig(F_d)
%  
% F_dp_trace = trace(F_dp)

% E is the Cauchy-Green Strain tensor 
E = 0.5*(F'*F-eye(3))

% E_h is the hydrostatic component of E
E_h = (1/3)*trace(E)*eye(3)

% E_d is the deviatoric component of E
E_d = E - E_h

E_d_sq = E_d.^2;

% nrm is the norm of E_d
nrm = sqrt(sum(E_d_sq(:)))

% E_d_nrm is the E_d normalized
E_d_nrm = E_d / nrm

% E_dp is the E_d in the principal frame
[~, E_dp] = eig(E_d_nrm)

% display the trace of E_dp
E_dp_trace = trace(E_dp)

theta = acos(sqrt(3/2)*E_dp(1))+pi/3
theta = acos(sqrt(3/2)*E_dp(2))-pi/3
theta = acos(-sqrt(3/2)*E_dp(3))
