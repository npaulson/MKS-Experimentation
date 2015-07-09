clear
clc
close all

N = 1000;
phiz = linspace(0,pi/2,N);
% scatter(phiz,zeros(length(phiz),1),'bo')
% hold on

phibin = phiz(1:end-1) + 0.5*((pi/2)/(N-1));

% scatter(phibin,zeros(length(phibin),1),'go')
% 
% hold off

phiinv = 1./((N-1)*sin(phibin));
sum(phiinv)

