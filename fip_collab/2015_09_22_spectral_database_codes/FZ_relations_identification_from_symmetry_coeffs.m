clear; clc; close all

load symhex.mat

plot3([0,0],[0,0],[0,2*pi],'k-')
hold on

plot3([0,0],[pi/2,pi/2],[0,2*pi],'k-')
plot3([0,0],[pi,pi],[0,2*pi],'k-')
plot3([2*pi,2*pi],[0,0],[0,2*pi],'k-')
plot3([2*pi,2*pi],[pi/2,pi/2],[0,2*pi],'k-')
plot3([2*pi,2*pi],[pi,pi],[0,2*pi],'k-')

xlabel('\phi_1')
ylabel('\Phi')
zlabel('\phi_2')
sc = 1.2;
axis([-0.2*2*pi sc*2*pi -0.2*pi sc*pi, -0.2*2*pi sc*2*pi]);

for ii = 0:6
    zpos = ii*pi/3;
    plot3([0,2*pi],[0,0],[zpos,zpos],'k-')
    plot3([0,2*pi],[pi/2,pi/2],[zpos,zpos],'k-')
    plot3([0,2*pi],[pi,pi],[zpos,zpos],'k-')    
    plot3([0,0],[0,pi],[zpos,zpos],'k-') 
    plot3([2*pi,2*pi],[0,pi],[zpos,zpos],'k-')
end

for jj = 0:3
   
    randloc = [2*pi*rand(),0.5*pi*rand(),(1/3)*pi*rand()];
    g = BungeMtrxMult(randloc);

    tmp = zeros(12,3);

    for ii = 1:12   
        g_sym = symhex(:,:,ii) * g;   
        tmp(ii,:) = rotmat2euler(g_sym);
    end

    euler = zeros(12,3);

    euler(:,1) = tmp(:,1);
    ltz = euler(:,1) < 0;
    euler(:,1) = euler(:,1) + 2*pi*ltz;

    euler(:,2) = tmp(:,2);
    ltz = euler(:,2) < 0;
    euler(:,2) = euler(:,2) + 2*pi*ltz;

    euler(:,3) = tmp(:,3);
    ltz = euler(:,3) < 0;
    euler(:,3) = euler(:,3) + 2*pi*ltz;   
    
    plot3(euler(:,1),euler(:,2),euler(:,3),...
        'LineStyle','none',...
        'Marker','o',...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor',[jj/3,jj/3,jj/3],...
        'MarkerSize',5);   

end

hold off



