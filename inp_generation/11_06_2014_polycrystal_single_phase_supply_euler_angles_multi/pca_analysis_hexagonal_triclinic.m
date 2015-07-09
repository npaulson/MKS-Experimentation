v_phi1 = linspace(0,2*pi(),12);
v_Phi = linspace(0,pi()/2,8);
% v_phi1 = linspace(0,2*pi(),24);
% v_Phi = linspace(0,pi()/2,16);

[X,Y] = meshgrid(v_phi1,v_Phi);

kaled = [X(:,1),Y(:,1);X(end,2:end)',Y(end,2:end)';X(2:end-1,end),Y(2:end-1,end)];
exte = [X(1,2:end)',Y(1,2:end)'];
Xcent = X(2:end-1,2:end-1);
Ycent = Y(2:end-1,2:end-1);
cent = [Xcent(:),Ycent(:)];

close('all')

figure(1)
scatter(kaled(:,1),kaled(:,2),'ro')
hold on
scatter(exte(:,1),exte(:,2),'bo')
scatter(cent(:,1),cent(:,2),'go')
xlabel('\phi1'); ylabel('\Phi')
legend('Potential FZ','\phi_2 = 0 edge of FZ','FZ Center')
hold off
axis tight equal


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

totgsh = [kaledgsh;extegsh;centgsh];
coeff = pca(totgsh);

kaledpca = kaledgsh * coeff;   
extepca = extegsh * coeff;
centpca = centgsh * coeff; 

pcaA = 1; pcaB = 2; pcaC = 3;


figure(2)

colnum = 20;
color = hsv(colnum);
for cc = 1:colnum
    plot(cc,5,...
        'LineStyle','none','Marker','o','MarkerEdgeColor','k',...
        'MarkerFaceColor',color(cc,:),'MarkerSize',7);
    hold on
end
hold off

figure(3)
plot3(kaledpca(:,pcaA),kaledpca(:,pcaB),kaledpca(:,pcaC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','o',...
    'MarkerFaceColor',color(1,:))
hold on
plot3(extepca(:,pcaA),extepca(:,pcaB),extepca(:,pcaC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
    'MarkerFaceColor',color(13,:))
plot3(centpca(:,pcaA),centpca(:,pcaB),centpca(:,pcaC),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
    'MarkerFaceColor',color(8,:))
hold off

legend('Potential FZ','\phi_2 = 0 edge of FZ','FZ Center')
xlabel(['pca',int2str(pcaA)]);
ylabel(['pca',int2str(pcaB)]);
zlabel(['pca',int2str(pcaC)]);
axis tight equal; grid on;


figure(4)
plot(kaledpca(:,pcaA),kaledpca(:,pcaB),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','o',...
    'MarkerFaceColor',color(1,:))
hold on
plot(extepca(:,pcaA),extepca(:,pcaB),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
    'MarkerFaceColor',color(13,:))
plot(centpca(:,pcaA),centpca(:,pcaB),...
    'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
    'MarkerFaceColor',color(8,:))
hold off

legend('Potential FZ','\phi_2 = 0 edge of FZ','FZ Center')
xlabel(['pca',int2str(pcaA)]);
ylabel(['pca',int2str(pcaB)]);
axis tight equal; grid on;


