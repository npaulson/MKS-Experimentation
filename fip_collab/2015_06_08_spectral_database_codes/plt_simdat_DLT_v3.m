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

xvar = E_eff(60:end)';
yvar = Epl33(60:end)';

xtmp = ones(size(xvar))*(max(xvar)-min(xvar));
xtst = [xvar,xvar + xtmp];

ytmp = yvar - min(yvar);

ytmp1 = ones(size(yvar))*yvar(end)-fliplr(ytmp);
ytmp2 = ones(size(yvar))*yvar(end)-ytmp;
ytmp3 = fliplr(yvar);

ytst = [yvar, ytmp1];

ytmp_ = ytst - max(ytst);

ytst = [ytst, ones(size(ytst))*max(ytst)-ytmp_];

rcvec = linspace(min(xtst),max(xtst),500)';
recon = trig_interpol(rcvec,xtst(1:end-1),ytst(1:end-1),min(xtst),max(xtst));

figure(2)
plot(xtst,ytst,'k')
hold on
plot(rcvec,real(recon),'b')

