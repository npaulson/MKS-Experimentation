clear; clc; close all;

N = 21;

x_plt = linspace(0,2*pi,100);

% the sample function
t_func = @(x) cos(x) + 0.25*sin(5*x);

figure(1)

% plot the original function
plot(x_plt, t_func(x_plt))

hold on

% define a sampling of the function
x_samp = linspace(0, 2*pi, N);
f_samp = t_func(x_samp);

% plot the sampling of the function
scatter(x_samp, f_samp, 'ro')

hold off

F_samp = zeros(N,1);

% calculate the DFT for the sampled values
for k = 0:N-1
    
    F_temp = 0; 
    
    for n = 0:N-1
    
        F_temp = F_temp + f_samp(n+1)*exp(-2*pi*1j*n*k/N);

    end
    
    F_samp(k+1) = (1/N)*F_temp;
    
end

figure(2)

% plot the DFT for all frequencies
scatter(0:N-1,real(F_samp))




f_recon = zeros(N,1);

% calculate the DFT for the sampled values
for n = 0:N-1
    
    f_temp = 0; 
    
    for k = 0:N-1
    
        f_temp = f_temp + F_samp(k+1)*exp(2*pi*1j*n*k/N);

    end
    
    f_recon(n+1) = f_temp;
    
end

figure(1)

hold on

scatter(x_samp, real(f_recon), 'bx')

f_recon = 0;

for k = 1:floor(N/2)

    disp([k+1,N-k+1])
    disp([F_samp(k+1),F_samp(N-k+1)])

    f_recon = f_recon + F_samp(k+1)*exp(1j*k*x_plt) + F_samp(N-k+1)*exp(-1j*k*x_plt);
    
end

% f_recon = F_samp(1) + f_recon + F_samp(ceil(N/2)+1)*cos(0.5*N*x_plt);
f_recon = F_samp(1) + f_recon;

plot(linspace(0,2*pi,95), f_recon(1:95))

hold off