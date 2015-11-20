clear; clc; close all

load symhex.mat

plot3([0,0],[0,0],[0,360],'k-')
hold on

plot3([0,0],[90, 90],[0,360],'k-')
plot3([0,0],[180,180],[0,360],'k-')
plot3([360,360],[0,0],[0,360],'k-')
plot3([90,90],[90,90],[0,360],'k-')
plot3([360,360],[180,180],[0,360],'k-')

xlabel('\phi_1')
ylabel('\Phi')
zlabel('\phi_2')
sc = 1.2;
axis([-0.2*360 sc*360 -0.2*180 sc*180, -0.2*360 sc*360]);

for ii = 0:6
    zpos = ii*60;
    plot3([0,360],[0,0],[zpos,zpos],'k-')
    plot3([0,360],[90,90],[zpos,zpos],'k-')
    plot3([0,360],[180,180],[zpos,zpos],'k-')    
    plot3([0,0],[0,180],[zpos,zpos],'k-') 
    plot3([360,360],[0,180],[zpos,zpos],'k-')
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
    
    eulerdeg = euler *(180/pi);
    
    plot3(eulerdeg(:,1),eulerdeg(:,2),eulerdeg(:,3),...
        'LineStyle','none',...
        'Marker','o',...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor',[jj/3,jj/3,jj/3],...
        'MarkerSize',5);   

end

hold off



