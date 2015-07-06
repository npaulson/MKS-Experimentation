function [ P ] = trig_interpol( xi,x,y,lb,ub )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

N = length(x);
L = ub-lb;

% calculate the DFT
% Yk = zeros(1,N);
% kvec = 0:N-1;
% for n = 0:N-1
%     Yk = Yk + (1/N)*y(n+1).*exp((-2*pi*1i*n*kvec)/N);
% end

Yk = fft(y);

% calculate the trigonometric interpolation at the locations in lvec
P = Yk(1);
for k = 1:floor(N/2)

    P = P + ...
        Yk(k+1).*exp((2*pi*1i*k*xi)/L) +...
        Yk(N-k+1).*exp((-2*pi*1i*k*xi)/L);
    
end

if mod(N,2)==0
    disp('even')
    P = P + Yk((N/2))*cos((pi*N*xi)/L);
end

P = P/N;

end

