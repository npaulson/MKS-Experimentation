%% Orientation Selection

% v_phi1,V_phi,v_phi2: vectors which discretize the hexagonal fundamental
% zone into a number of orienations
% v_phi1 = linspace(0,2*pi(),41);
% v_Phi = linspace(0,pi()/2,12);
% v_phi2 = linspace(0,pi()/3,10);

v_phi1 = linspace(0,2*pi(),20);
v_Phi = linspace(0,pi()/2,7);
v_phi2 = linspace(0,pi()/3,5);

[X,Y,Z] = meshgrid(v_phi1,v_Phi,v_phi2);
% ori: array containing bunge-euler angles for all trial orientations
ori = [X(:), Y(:), Z(:)];
% ori = [ori (1:length(ori))']
close('all')

figure(1)
scatter(ori(:,1),ori(:,2),'.')
axis equal

figure(2)
scatter(ori(:,2),ori(:,3),'.')
axis equal

% ori_len: number of trial orientations
N = length(ori(:,1));

%% Read OIM coefficient file

fileID = fopen('OIM_coeff_L04.txt','r');
formatSpec = '%d %d %d %f %f';
sizeA = [5, inf];
A = fscanf(fileID,formatSpec,sizeA)';

%% Regression

% ocf: number of coefficients from the original ODF harmonic description
ocf = 56;

% lvec: vector containing the sequence of l-numbers from 0 to L
lvec = A(:,1);

% w: "half width of the gaussian peak located at the orientation g_i" OIM
% software (is this the same as the Gaussian Smoothing angle?)
w = 2.5 * (pi()/180);

% Y_coeff: vector of the coefficients used
Y_coeff = A(:,4) + A(:,5)*1i;

X_coeff = zeros(ocf, N);

for ii = 1:N
    
    gsh_res = gsh_hcp_tri_L_7(ori(ii,1),ori(ii,2),ori(ii,3))';
    
    for jj = 1:length(gsh_res)
        %
        l = lvec(jj);
        %
        K = (exp(-0.25*(l^2)*(w^2))-exp(-0.25*((l+1)^2)*(w^2)))/(1-exp(-0.25*w^2));
        %
        X_coeff(jj,ii) = (2*l+1)*K*gsh_res(jj);
        %       X_coeff(jj,ii) = gsh_res(jj);
        
        
    end
end

save X_coeff.mat X_coeff % Corresponding GSH basis function evaluated at descrete orientation
save Y_coeff.mat Y_coeff % Target ODF

%%
% vol_frac: the vector of volume fractions from the regression
% vol_frac = regress(Y_coeff,X_coeff);
%
% disp(vol_frac)

%% Debug

% for ii = 1
%
% %     gsh_res = GSH_Hexagonal_Triclinic(ori(ii,1),ori(ii,2),ori(ii,3))';
%
%     for jj = 1:length(gsh_res)
%
%         l = lvec(jj);
%
%         K = (exp(-0.25*(l^2)*(w^2))-exp(-0.25*((l+1)^2)*(w^2)))/(1-exp(-0.25*w^2));
%
%         temp = ((2*l+1)/N)*K
%
%     end
% end