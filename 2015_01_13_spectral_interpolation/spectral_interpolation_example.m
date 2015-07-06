close all

x = -0*pi: 0.01: 2*pi;

% sample times for the function
Nd = 14;
x_d = linspace(0,2*pi,Nd);

% f = @(x) cos(x) + 0.5*sin(2*x) + 0.25*cos(3*x).^2;
f = @(x) -0.75*sin(x) + 0.25*cos(3*x);


% plot the function and the locations which are sampled
figure(1)

f_eval = f(x);

plot(x,f_eval,'LineSmoothing','on')
hold on
scatter(x_d,f(x_d))

xlabel('time')
ylabel('amplitude')
minB = @(v) min(v)-0.2*abs(min(v));
maxB = @(v) max(v)+0.2*abs(max(v));

axis([0 2*pi minB(f_eval) maxB(f_eval)])

% take the fft
f_d_fft = fft(f(x_d(1:end-1)));

% plot the real and imaginary parts of the fft
figure(2)

subplot(2,1,1)

scatter(0:Nd-2,real(f_d_fft));
title('Real frequencies in the original FFT')
xlabel('frequency')
ylabel('amplitude')
axis([0 Nd-2 minB(real(f_d_fft)) maxB(real(f_d_fft))])

subplot(2,1,2)

scatter(0:Nd-2,imag(f_d_fft));
title('Imaginary frequencies in the original FFT')
xlabel('frequency')
ylabel('amplitude')
axis([0 Nd-2 minB(imag(f_d_fft)) maxB(imag(f_d_fft))])

% zero pad in frequency space

scale = 2;

f_Nd_fft = zeros(1,scale*(Nd-1));
% f_Nd_fft(1:0.5*Nd-1) = f_d_fft(1:0.5*Nd-1);
% f_Nd_fft(0.5*Nd) = 0.5*f_d_fft(0.5*Nd);
% f_Nd_fft(end - 0.5*Nd + 1) = 0.5*f_d_fft(0.5*Nd+1);
% f_Nd_fft(end - 0.5*Nd + 2: end) = f_d_fft(0.5*Nd+2:end);

f_Nd_fft(1:0.5*Nd) = f_d_fft(1:0.5*Nd);
length(f_Nd_fft(end - 0.5*Nd + 2: end))
length(f_d_fft(0.5*Nd+1:end))
f_Nd_fft(end - 0.5*Nd+2: end) = f_d_fft(0.5*Nd+1:end);


% plot the real and imaginary parts of the fft
figure(3)

subplot(2,1,1)

scatter(0:length(f_Nd_fft)-1,real(f_Nd_fft));
title('Real frequencies in the padded FFT')
xlabel('frequency')
ylabel('amplitude')
axis([0 scale*Nd-1 minB(real(f_Nd_fft)) maxB(real(f_Nd_fft))])

subplot(2,1,2)

scatter(0:length(f_Nd_fft)-1,imag(f_Nd_fft));
title('Imaginary frequencies in the padded FFT')
xlabel('frequency')
ylabel('amplitude')
axis([0 2*Nd-1 minB(imag(f_Nd_fft)) maxB(imag(f_Nd_fft))])

% perform the ifft

f_Nd_ifft = ifft(f_Nd_fft);

% scale the amplitudes accordingly

f_eval_interpolate = f_Nd_ifft * scale;

% plot the interpolated values

figure(1)

x_d_new = linspace(0,2*pi,Nd*scale-1);

scatter(x_d_new(1:end-1),real(f_eval_interpolate),'rx')
title('Original Function (blue), Sampled Values (green), Interpolated Values(red)')

