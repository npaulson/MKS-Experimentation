clear; clc; close all

% sample times for the function
Nd = 100;
N = Nd-1;
x_d = linspace(0,2*pi,Nd);
L = max(x_d)-min(x_d);

f = @(x1,x2,x3) -.85*sin(x1+.5423234342) + .15*cos(2*x1) + .5*sin(x2)+ .23*cos(x3-.442);

[X1d, X2d, X3d] = ndgrid(x_d,x_d,x_d);

Zd = f(X1d, X2d, X3d);

% take the fft
f_d_fft = fftn(Zd(1:end-1,1:end-1,1:end-1));

% point to interpolate:
pt = [0.8,6.1,2.2];

f_eval = f(pt(1),pt(2),pt(3))

tic

tmp = permute(f_d_fft,[2,3,1]);
tmp = reshape(tmp,[N*N,N]);
tmp = trig_interpol_dim(pt(1),tmp,L);
tmp = reshape(tmp,[N,N]);

tmp = permute(tmp,[2,1]);
tmp = reshape(tmp,[N,N]);
tmp = trig_interpol_dim(pt(2),tmp,L);
tmp = reshape(tmp,[1,N]);

tmp = trig_interpol_dim(pt(3),tmp,L);
f_intp = real(tmp)

toc

P = 0;

kmax = floor(N/2.)

for l = -kmax:kmax
for m = -kmax:kmax
for n = -kmax:kmax

    P = P + f_d_fft(mod(l,N)+1,mod(m,N)+1,mod(n,N)+1)*...
        exp((2*pi*1i*l*pt(1))/L)*...
        exp((2*pi*1i*m*pt(2))/L)*...
        exp((2*pi*1i*n*pt(3))/L);        
    
end
end
end

P = P/(N^3);

disp(P)