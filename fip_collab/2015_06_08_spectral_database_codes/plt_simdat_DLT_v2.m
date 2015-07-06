clear; clc; close all;

%% Read from txt file

filename =  'sim_Ti64_0000006.dat';
fid = fopen(filename);
fgetl(fid)
A = fscanf(fid, '%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f',[23,inf]);
fclose(fid);

A = A';

time = A(:,1);
E_eff = A(:,2);
Sig11 = A(:,3);
Sig22 = A(:,4);
Sig33 = A(:,5);
Eps11 = A(:,9);
Eps22 = A(:,10);
Eps33 = A(:,11);
Epl11 = A(:,15);
Epl22 = A(:,19);
Epl33 = A(:,23);

%% plot stress strain curve

figure(1)
plot(E_eff,abs(Sig11))

%% fit legendre polynomial to function values with regression

% order of the legendre polynomial to use
N = 1;

% % find the roots and weights of the legendre polynomial for the given truncation level
% [roots, weights] = lgwt(N,-1,1);

xvar_orig = E_eff(10:end);
yvar = Epl33(10:end);

lb = xvar_orig(1); 
ub = xvar_orig(end);

xvar = (2*xvar_orig-(ub+lb))/(ub-lb);

xtst = xvar(1:1:end);
ytst = yvar(1:1:end);

X = zeros(length(xtst),N+1);

for n = 0:N

%     X(:,n+1) = legendreP(n,xtst);
    X(:,n+1) = xtst.^n;

end

coeffs = X'*X\X'*ytst;

%% plot the interpolation

rcvec = linspace(-1,1,100)';
recon = zeros(length(rcvec),1);

for n = 0:N  

%     recon = recon + coeffs(n+1)*legendreP(n,rcvec);
    recon = recon + coeffs(n+1)*rcvec.^n;
    
end

figure(2)
plot(xvar,yvar,'k')
hold on
% scatter(roots,recon,'b+')
plot(roots,recon,'b')

