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

tic

xvar = E_eff(60:1:end);
yvar = Epl33(60:1:end);

tmp = xvar - xvar(1);

xtmp = linspace(tmp(1),tmp(end),2*length(tmp)+1);
ytmp = interp1(tmp,yvar,xtmp,'spline');

xtst = xtmp;
midval = ytmp(end)*(1+0.25*(abs(ytmp(end)-ytmp(end-1))/abs(ytmp(end)-ytmp(1))));
ytst = [yvar;midval;flipud(yvar)];

rcvec = linspace(min(xtst),max(xtst),500)';
recon = trig_interpol(xtst(1:end-1),xtst(1:end-1),ytst(1:end-1),0,xtst(end));

toc

figure(2)
plot(xtst,ytst,'k')
hold on
plot(xtst(1:end-1),real(recon),'b')

error = 100*mean(abs((ytst(1:end-1)-real(recon'))./ytst(1:end-1)));