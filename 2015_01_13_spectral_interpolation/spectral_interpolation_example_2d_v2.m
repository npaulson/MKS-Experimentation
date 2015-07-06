close all

% sample times for the function
Nd = 10;

scale = 2;

x_d = linspace(0,2*pi,Nd);

x_d_L = linspace(0,2*pi,Nd*scale-1);

f = @(x1,x2) -.85*sin(x1) + .15*cos(2*x1) + .5*sin(x2);


[X1, X2] = meshgrid(x_d_L,x_d_L);
[X1d, X2d] = meshgrid(x_d,x_d);

Z = f(X1,X2);
Zd = f(X1d, X2d);

% plot the function and the locations which are sampled
figure(1)

C = 0.5*ones(size(Z));

% surf(X1,X2,Z,C)

% plot3(X1(:),X2(:),Z(:),...
%     'LineStyle','none',...
%     'Marker','.',...
%     'MarkerEdgeColor','b',...
%     'MarkerSize',5); 

color = hsv(20);

hold on

plot3(X1d(:),X2d(:),Zd(:),...
    'LineStyle','none',...
    'Marker','o',...
    'MarkerEdgeColor','b',...
    'MarkerSize',8); 

xlabel('x1 dimension')
ylabel('x2 dimension')
zlabel('z dimension')
minB = @(v) min(v)-0.2*abs(min(v));
maxB = @(v) max(v)+0.2*abs(max(v));

axis([0 2*pi 0 2*pi minB(Z(:)) maxB(Z(:))])
axis equal

% take the fft
f_d_fft = fft2(Zd(1:end-1,1:end-1));

figure(2)
[Xggg, Yggg]=meshgrid(1:Nd-1);
scatter3(Xggg(:),Yggg(:),imag(f_d_fft(:)))


% zero pad in frequency space

f_Nd_fft = zeros(scale*(Nd-1));
f_Nd_fft(1:0.5*Nd,1:0.5*Nd) = f_d_fft(1:0.5*Nd,1:0.5*Nd);
disp(f_Nd_fft(1:0.5*Nd,end-0.5*Nd+2:end))
disp(f_d_fft(1:0.5*Nd,0.5*Nd+1:end))
f_Nd_fft(1:0.5*Nd,end-0.5*Nd+2:end) = f_d_fft(1:0.5*Nd,0.5*Nd+1:end);
f_Nd_fft(end-0.5*Nd+2:end,1:0.5*Nd) = f_d_fft(0.5*Nd+1:end,1:0.5*Nd);
f_Nd_fft(end-0.5*Nd+2:end,end-0.5*Nd+2:end) = f_d_fft(0.5*Nd+1:end,0.5*Nd+1:end);

% perform the ifft

f_Nd_ifft = ifft2(f_Nd_fft);

% scale the amplitudes accordingly

Z_Nd = f_Nd_ifft * scale^2;

% plot the interpolated values

figure(1)

[X1d_r, X2d_r] = meshgrid(x_d_L(1:end-1),x_d_L(1:end-1));

Z_Nd_r = Z_Nd;

plot3(X1d_r(:),X2d_r(:),real(Z_Nd_r(:)),...
    'LineStyle','none',...
    'Marker','o',...
    'MarkerEdgeColor','k',...
    'MarkerFaceColor',[0.8,0.8,0.8],...
    'MarkerSize',5); 

title('Original Function(green), Sampled Points(blue), Interpolated Points(grey)')

avgerr = 100*mean(abs((f(X1d_r(:), X2d_r(:))-Z_Nd_r(:))./Z_Nd_r(:)));
disp(avgerr)
