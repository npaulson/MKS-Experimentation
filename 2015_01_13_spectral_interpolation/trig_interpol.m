function [ P ] = trig_interpol( xi,Yk, L )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

N = length(Yk);

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

