% phi1 = .1:pi/6:2*pi-.1;
% phi = .1:pi/6:pi/2-.1;
% phi2 = .1:pi/6:pi/3-.1;
% 
% [PHI1, PHI, PHI2] = meshgrid(phi1,phi,phi2);
% 
% figure(1)
% 
% plot3(PHI1(:),PHI(:),PHI2(:),...
%     'LineStyle','none',...
%     'Marker','o',...
%     'MarkerEdgeColor','k',...
%     'MarkerFaceColor','b',...
%     'MarkerSize',5);
% 
% axis equal

load symhex.mat
load plotbox.mat


boxa = bsxfun(@plus,box,[0.5,0.5,0.5]);
boxb1 = bsxfun(@times,boxa,[2*pi,0.5*pi,(1/3)*pi]);

plot3(boxb1(:,1),boxb1(:,2),boxb1(:,3),...
    'LineStyle',':');      

hold on

boxb2 = bsxfun(@times,boxa,[2*pi,pi,2*pi]);

plot3(boxb2(:,1),boxb2(:,2),boxb2(:,3),...
    'r-');   


for ii = 1:12
    
    randloc = [2*pi*rand();0.5*pi*rand();(1/3)*pi*rand()]; 
    
    g = BungeMtrxAlt(randloc(1),randloc(2),randloc(3));
    
    symloc = symhex(:,:,ii) * g;
    
    plot3(symloc(1),symloc(2),symloc(3),...
        'LineStyle','none',...
        'Marker','o',...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor','b',...
        'MarkerSize',5);        

end

hold off
axis equal
