f = @(x1,x2) .75*cos(x1)+.25*sin(4*x1)+.5*sin(2*x2)+.5*cos(3*x2);

figure(1)

ns = 10;

x1v = linspace(0,2*pi,ns);
x2v = linspace(0,2*pi,ns);
yv = f(x1v,x2v);

scatter3(x1v,x2v,yv)