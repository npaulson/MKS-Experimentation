phi1 = .1;
Phi = .2;
phi2 = .3;

t1 = cos(phi1);
t2 = sqrt(0.3e1);
t3 = sin(phi1);
t4 = t1 * t2;
t5 = t3 + t4;
t2 = t2 * t3;
t6 = -t1 + t2;
t7 = t5 / 0.2e1;
t8 = t6 / 0.2e1;
t3 = -t3 + t4;
t1 = t1 + t2;
t2 = t3 / 0.2e1;
t4 = t1 / 0.2e1;
t9 = -0.2e1 * phi1;
TempExpr = [-phi1 + atan2(-t7, -t8) -pi 0;...
            0 0 0;...
            -phi1 + atan2(t7, -t8) 0 0;...
            -phi1 + atan2(t2, -t4) 0 0;...
            -pi 0 0;...
            -phi1 + atan2(-t7, t8) 0 0;...
            -phi1 + atan2(-t2, t4) 0 0;...
            t9 -pi 0;...
            -phi1 + atan2(t5, t6) -pi 0;...
            -phi1 + atan2(-t2, -t4) -pi 0;...
            pi + t9 -pi 0;...
            -phi1 + atan2(t3, t1) -pi 0];

disp(TempExpr)

phi1col = TempExpr(:,3);
ltz = phi1col < 0;
phi1col = phi1col + 2*pi*ltz;

Phicol = TempExpr(:,2);
ltz = Phicol < 0;
Phicol = Phicol + 2*pi*ltz;

phi2col = TempExpr(:,1);
ltz = phi2col < 0;
phi2col = phi2col + 2*pi*ltz;

phi1_pts = phi1 + phi1col;
Phi_pts = Phi + Phicol;
phi2_pts = phi2 + phi2col;

scatter3(phi1_pts, Phi_pts, phi2_pts)
hold on

xlabel('\phi_1')
ylabel('\Phi')
zlabel('\phi_2')
sc = 1.2;
axis([-0.2*2*pi sc*2*pi -0.2*pi sc*pi, -0.2*2*pi sc*2*pi]);

% for ii = 0:1
%     xpos = ii*2*pi;
%     plot3([xpos,xpos],[0,pi],[0,0],'b-')
%     plot3([xpos,xpos],[0,pi],[2*pi,2*pi],'b-')
% %     plot3([xpos,xpos],[pi,pi],[0,0],'b-')
% %     plot3([xpos,xpos],[0,0],[0,2*pi],'b-')
% 
% end

for ii = 0:6
    zpos = ii*pi/3;
    plot3([0,2*pi],[0,0],[zpos,zpos],'k-')
    plot3([0,2*pi],[pi/2,pi/2],[zpos,zpos],'k-')
    plot3([0,2*pi],[pi,pi],[zpos,zpos],'k-')    
    plot3([0,0],[0,pi],[zpos,zpos],'k-') 
    plot3([2*pi,2*pi],[0,pi],[zpos,zpos],'k-')
end
    
plot3([0,0],[0,0],[0,2*pi],'k-')
plot3([0,0],[pi/2,pi/2],[0,2*pi],'k-')
plot3([0,0],[pi,pi],[0,2*pi],'k-')
plot3([2*pi,2*pi],[0,0],[0,2*pi],'k-')
plot3([2*pi,2*pi],[pi/2,pi/2],[0,2*pi],'k-')
plot3([2*pi,2*pi],[pi,pi],[0,2*pi],'k-')


% for ii = 0:2
%     ypos = ii*pi/2;
%     plot3([0,2*pi],[ypos,ypos],[0,0],'b-')
%     plot3([0,0],[ypos,ypos],[0,2*pi],'b-')
% end

% for ii = 0:6
%     xpos = ii*pi/3;
%     plot([xpos,xpos],[0,pi],'b-')
% end

hold off