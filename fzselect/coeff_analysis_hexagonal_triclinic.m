v_phi1 = linspace(0,2*pi()-.03,80);
v_Phi = acos(linspace(0,1,16));

[X,Y] = meshgrid(v_phi1,v_Phi);

% kaled = [X(:,1),Y(:,1);X(1,2:end)',Y(1,2:end)';X(2:end-1,end),Y(2:end-1,end)];
kaled = [X(1:end-1,end),Y(1:end-1,end);X(1:end-1,1),Y(1:end-1,1); X(1,2:end-1)',Y(1,2:end-1)'];
exte = [X(end,1:end)',Y(end,1:end)'];
Xcent = X(2:end-1,2:end-1);
Ycent = Y(2:end-1,2:end-1);
cent = [Xcent(:),Ycent(:)];

close('all')

figure(1)
scatter(kaled(:,1),kaled(:,2),'ro')
hold on
scatter(exte(:,1),exte(:,2),'bo')
scatter(cent(:,1),cent(:,2),'go')
plot([0,2*pi,2*pi,0,0],[0,0,pi/2,pi/2,0],'k:')
axis equal
axis([ -.1 2*pi+.1 -.1 pi/2+.1])
xlabel('\phi1'); ylabel('\Phi')
legend('Potential FZ','\phi_2 = 0 edge of FZ','FZ Center')
hold off

%%

for ii = 1:length(kaled(:,1))
    tmp = gsh_hcp_tri_L_7(kaled(ii,1),kaled(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(kaled(ii,1),kaled(ii,2),0);
    kaledgsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end

for ii = 1:length(exte(:,1))
    tmp = gsh_hcp_tri_L_7(exte(ii,1),exte(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(exte(ii,1),exte(ii,2),0);
    extegsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end

for ii = 1:length(cent(:,1))
    tmp = gsh_hcp_tri_L_7(cent(ii,1),cent(ii,2),0);
%     tmp = GSH_Hexagonal_Triclinic(cent(ii,1),cent(ii,2),0);
    centgsh(ii,:) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
end


%% 3D images of GSH coefficients

color = hsv(20);

compA = 3;
compB = 4;
compC = 9;

figure(2)
plot3(kaledgsh(:,compA),kaledgsh(:,compB),kaledgsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','o',...
    'MarkerFaceColor',color(1,:))
hold on
plot3(extegsh(:,compA),extegsh(:,compB),extegsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
    'MarkerFaceColor',color(13,:))
plot3(centgsh(:,compA),centgsh(:,compB),centgsh(:,compC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
    'MarkerFaceColor',color(8,:))
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