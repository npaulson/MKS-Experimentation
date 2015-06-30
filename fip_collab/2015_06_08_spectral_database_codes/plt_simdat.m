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

%% fit legendre polynomial to function values

% order of the legendre polynomial to use
N = 5;

% find the roots of the legendre polynomial for the given truncation level
syms x
roots = double(vpasolve(legendreP(N,x) == 0));

xvar_orig = E_eff(60:end);
yvar = Epl22(60:end);

lb = xvar_orig(1); 
ub = xvar_orig(end);

xvar = (2*xvar_orig-(ub+lb))/(ub-lb);

Fk = zeros(N,1); 

for kk = 0:N - 1

    tmp = 0;

    for nn = 1:N
        pk = legendreP(kk,roots(kk+1));
        pNm1 = legendreP(N-1,roots(kk+1));
        tmpval = 1-roots(kk+1)^2;
        fval = interp1(xvar,yvar,tmpval,'spline');
        
        tmp = tmp + (fval*pk)/pNm1;
    end

    Fk(kk+1) = ((2*kk+1)/(N^2))*tmp;

end

%% plot the interpolation

rcvec = linspace(-1,1,100);
recon = zeros(length(roots),1);
    
for kk = 0:N-1
    recon = recon + Fk(kk+1)*legendreP(kk,roots);
end

figure(2)
scatter(xvar,yvar)
hold on
scatter(roots,recon)

