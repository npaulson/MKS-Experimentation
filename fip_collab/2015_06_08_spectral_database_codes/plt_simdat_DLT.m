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
N = 15;

% find the roots and weights of the legendre polynomial for the given truncation level
[roots, weights] = lgwt(N,-1,1);

xvar_orig = E_eff(60:end);
yvar = Epl22(60:end);

lb = xvar_orig(1); 
ub = xvar_orig(end);

xvar = (2*xvar_orig-(ub+lb))/(ub-lb);

Fk = zeros(N,1); 

for k = 0:N - 1

    tmp = 0;

    for n = 0:N-1
        
        fval = interp1(xvar,yvar,roots(n+1),'spline');
        Pn = legendreP(n,roots(k+1));

        tmp = tmp + fval*Pn;
    end

    Fk(k+1) = tmp;

end

%% plot the interpolation

rcvec = linspace(-1,1,100);
recon = zeros(length(roots),1);

for n = 0:N-1    

    tmp = 0;

    for k = 0:N-1
        
%         tmp = tmp + weights(k+1)*Fk(k+1)*legendreP(n,roots(k+1));
        tmp = tmp + weights(k+1)*Fk(k+1)*legendreP(n,roots(k+1));


    end

    recon(n+1) = (n+0.5)*tmp;    
    
end

figure(2)
plot(xvar,yvar,'k')
hold on
% scatter(roots,recon,'b+')
scatter(roots,recon,'b+')

