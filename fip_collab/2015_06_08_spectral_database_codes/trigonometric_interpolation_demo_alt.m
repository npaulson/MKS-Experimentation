clear; clc; close all;

% f is the function of interest
% f = @(x) cos(x+pi/4)+0.5*cos(2*x);
f = @(x) abs(x-pi);
% f = @(x) x;

% N is # samples (must be even)
N = 11;

% xvar is the first N values of rcvec are the sampling points
xvar = linspace(0,2*pi,N+1)';
% yvar is the first N values of the function at the sampling points 
yvar = f(xvar);

% lvec is the vector of x values used for plotting a "smooth" function
lvec = linspace(0,2*pi,1000)';


figure(1)
% plot the sampled points of the function
scatter(xvar,yvar)
hold on
% plot the original function
plot(lvec,f(lvec))

f_int = trig_interpol(lvec,xvar(1:end-1),yvar(1:end-1),0,2*pi);

figure(1)
% plot the function reconstructed using trigonometric interpolation
plot(lvec,real(f_int))