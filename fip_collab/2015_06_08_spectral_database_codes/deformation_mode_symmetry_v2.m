D1 = @(x) sqrt(2/3)*cos(x*(pi/180)-(pi/3));
D2 = @(x) sqrt(2/3)*cos(x*(pi/180)+(pi/3));
D3 = @(x) -sqrt(2/3)*cos(x*(pi/180));

x = 0:1:360;

figure(1)

plot(x,D1(x),'r-')

hold on

plot(x,D2(x),'g-')
plot(x,D3(x),'b-')

hold off

figure(2)

plot3(D1(x),D2(x),D3(x))
hold on

axis equal
xlabel('D1'); ylabel('D2'); zlabel('D3')

N = 6*16;

for ii = 1:N
    c = mod(ii,16)/16;
    x = (ii-1)*(pi/(N/2));

    tmp = [D1(x),D2(x),D3(x)];
    
    scatter3(tmp(1),tmp(2),tmp(3),[],[.5 c .5],'filled')

end

hold off