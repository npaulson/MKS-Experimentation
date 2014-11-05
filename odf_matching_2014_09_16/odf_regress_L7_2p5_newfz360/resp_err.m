%% Results and Error Measurment Script
% Noah Paulson 2014-10-17
%
% Measure the error in the GSH representation of the ODF calculated by
% fmincon to the representation from the OIM software.

%% Load Data

load X_coeff
load Y_coeff
load results

% order the GSH coefficients from our code and the OIM software the same
% way. The user should only leave the desired set of coefficients
% uncovered. The first set is for L == 4, the second set is for L == 6, and
% the third set is for L == 7.

% indXl = [4:6 11:15];
% indYl = [2 4:2:6 7 9:2:15];
% indXl = [4:6 11:15 28:2:40 29:2:41];
% indYl = [2 4:2:6 7 9:2:15 16 18:2:28 29 31:2:41];
indXl = [4:6 11:15 28:2:40 29:2:41 49:56];
indYl = [2 4:2:6 7 9:2:15 16 18:2:28 29 31:2:41 42 44:2:56];

X_coeff = X_coeff(indXl,:);
Y_coeff = Y_coeff(indYl,:);

%% Error Calculation

% vector of error for each GSH coefficient
errvec = 100*(abs(X_coeff*x - Y_coeff)./abs(Y_coeff));
% measure of the average error over all coefficients
errmeas = mean(errvec);

%% Convert Volume Fractions to MRD (Multiples of a Random Distribution)

load orientations

phi1max = max(ori(:,1)); 
Phimax = max(ori(:,2));
phi2max = max(ori(:,3));

orivol = phi1max * 1 * phi2max;

phi1unique = length(unique(ori(:,1)));
Phiunique = length(unique(ori(:,2))); 
phi2unique = length(unique(ori(:,3)));

phi1del = phi1max/(phi1unique);
Phidel = Phimax/(Phiunique);
phi2del = phi2max/(phi2unique);

mrd = (orivol * x)./(phi1del*phi2del*(cos(ori(:,2) - 0.5*Phidel)-cos(ori(:,2) + 0.5*Phidel)));

