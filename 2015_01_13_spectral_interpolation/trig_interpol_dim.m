function [ P ] = trig_interpol_dim( xi, arr_fft, L )
%UNTITLED5 Summary of this function goes here
%   xi: interpolation point in the dimension of interest

%   arr_fft: array to use for interpolation. This array must be shaped
%   so that it is 'm' by 'n' where interpolation will be performed along
%   the 'n' dimension for all vectors indexed by 'm' 

%   L: range of coordinates in the dimension of interest

N = size(arr_fft, 2);

% calculate the trigonometric interpolation at the locations in lvec
P = arr_fft(:, 1);
for k = 1:floor(N/2)

    P = P + ...
        arr_fft(:,k+1).*exp((2*pi*1i*k*xi)/L) +...
        arr_fft(:,N-k+1).*exp((-2*pi*1i*k*xi)/L);
    
end

if mod(N,2)==0
    disp('even')
    P = P + arr_fft(:,N/2)*cos((pi*N*xi)/L);
end

P = P/N;

end

