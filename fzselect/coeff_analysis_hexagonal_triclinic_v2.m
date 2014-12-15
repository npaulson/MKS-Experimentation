figure(1)

colnum = 20;
color = hsv(colnum);
for cc = 1:colnum
    plot(cc,5,...
        'LineStyle','none','Marker','o','MarkerEdgeColor','k',...
        'MarkerFaceColor',color(cc,:),'MarkerSize',7);
    hold on
end
hold off



v_phi1 = linspace(0,2*pi(),80);
v_Phi = acos(linspace(0,1,16));

[X,Y] = meshgrid(v_phi1,v_Phi);

left = [X(2:end-1,1),Y(2:end-1,1)];
top = [X(1,1:end-1)',Y(1,1:end-1)'];
bottom = [X(end,1:end-1)',Y(end,1:end-1)'];
Xcent = X(2:end-1,2:end-1);
Ycent = Y(2:end-1,2:end-1);
cent = [Xcent(:),Ycent(:)];

close('all')

figure(2)

scatter(left(:,1),left(:,2),'ro')
hold on
scatter(bottom(:,1),bottom(:,2),'bo')
scatter(top(:,1),top(:,2),'yo')
scatter(cent(:,1),cent(:,2),'go')

plot([0,2*pi,2*pi,0,0],[0,0,pi/2,pi/2,0],'k:')
axis equal
axis([ -.1 2*pi+.1 -.1 pi/2+.1])
xlabel('\phi1'); ylabel('\Phi')
legend('Potential FZ','\phi_2 = 0 edge of FZ','FZ Center')
hold off

%%

for ii = 1:length(left(:,1))
    tmp = gsh_hcp_tri_L_7(left(ii,1),left(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(kaled(ii,1),kaled(ii,2),0);
    leftgsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end

for ii = 1:length(bottom(:,1))
    tmp = gsh_hcp_tri_L_7(bottom(ii,1),bottom(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(exte(ii,1),exte(ii,2),0);
    bottomgsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end

for ii = 1:length(cent(:,1))
    tmp = gsh_hcp_tri_L_7(cent(ii,1),cent(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(cent(ii,1),cent(ii,2),0);
    centgsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end

for ii = 1:length(top(:,1))
    tmp = gsh_hcp_tri_L_7(top(ii,1),top(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(cent(ii,1),cent(ii,2),0);
    topgsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end

%% 3D images of GSH coefficients

compA = 1;
compB = 4;
compC = 5;

figure(3)
plot3(leftgsh(:,compA),leftgsh(:,compB),leftgsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','o',...
    'MarkerFaceColor',color(1,:))
hold on
plot3(bottomgsh(:,compA),bottomgsh(:,compB),bottomgsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
    'MarkerFaceColor',color(13,:))
plot3(centgsh(:,compA),centgsh(:,compB),centgsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
    'MarkerFaceColor',color(8,:))
plot3(topgsh(:,compA),topgsh(:,compB),topgsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
    'MarkerFaceColor',color(4,:))
hold off

legend('Potential FZ','\Phi = 0 edge of FZ','FZ Center')
xlabel(['gsh',int2str(compA)]);
ylabel(['gsh',int2str(compB)]);
zlabel(['gsh',int2str(compC)]);
axis tight equal; grid on;




% %% Save 2D images of GSH coefficients
% 
% ims = {}
% 
% for comp = 1:14
% 
%     compA = 1;
%     compB = comp;
%     
%     figure(3)
%     plot(kaledgsh(:,compA),kaledgsh(:,compB),...
%         'LineStyle','none','MarkerEdgeColor','k','Marker','o',...
%         'MarkerFaceColor',color(1,:))
%     hold on
%     plot(extegsh(:,compA),extegsh(:,compB),...
%         'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
%         'MarkerFaceColor',color(13,:))
%     plot(centgsh(:,compA),centgsh(:,compB),...
%         'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
%         'MarkerFaceColor',color(8,:))
%     hold off
% 
%     legend('Potential FZ','\Phi = 0 edge of FZ','FZ Center')
%     xlabel(['gsh',int2str(compA)]);
%     ylabel(['gsh',int2str(compB)]);
%     axis tight equal; grid on;
%     
%     ims{comp} = fullfile( 'gshplt', sprintf('gshplt_%i_%i.png',compA,compB) );
%     saveas( gcf, ims{comp} )
% 
% end