clear; clc; close all;

% f is the function of interest
% f = @(x) cos(x+pi/4)+0.5*cos(2*x);
% f = @(x) abs(x-pi);
f = @(x) x;

% N is # samples (must be even)
N = 50;

% xvar is the first N values of rcvec are the sampling points
xvar = linspace(0,2*pi,N+1)';
% yvar is the first N values of the function at the sampling points 
yvar = f(rcvec);

% lvec is the vector of x values used for plotting a "smooth" function
lvec = linspace(0,2*pi,1000)';


figure(1)
% plot the sampled points of the function
scatter(xvar,yvar)
hold on
% plot the original function
plot(lvec,f(lvec))

% calculate the DFT
Yk = zeros(1,N);
kvec = 0:N-1;
for n = 0:N-1
    Yk = Yk + (1/N)*yvar(n+1).*exp((-2*pi*1i*n*kvec)/N);
end

figure(2)
% plot the frequency spectrum of the DFT
scatter(kvec,real(Yk))

% calculate the trigonometric interpolation at the locations in lvec
f_int = Yk(1);
for k = 1:floor(N/2)

    f_int = f_int + ...
            Yk(k+1).*exp((2*pi*1i*k*lvec)/(2*pi)) +...
            Yk(N-k+1).*exp((-2*pi*1i*k*lvec)/(2*pi));
    
end

figure(1)
% plot the function reconstructed using trigonometric interpolation
plot(lvec,real(f_int))