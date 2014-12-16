close('all')

%%

figure(1)

colnum = 80;
color = hsv(colnum);
for cc = 1:colnum
    plot(cc,5,...
        'LineStyle','none','Marker','o','MarkerEdgeColor','k',...
        'MarkerFaceColor',color(cc,:),'MarkerSize',7);
    hold on
end
hold off

%%

v_phi1 = linspace(0,4*pi(),80);
v_Phi = acos(linspace(0,1,16));

[X,Y] = meshgrid(v_phi1,v_Phi);


figure(2)

plot(X(end,1:end-1)',Y(end,1:end-1)',...
    'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
    'MarkerFaceColor',[0.4,0.4,0.4])
hold on

plot(X(1,1:end-1)',Y(1,1:end-1)',...
    'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
    'MarkerFaceColor',[0.9,0.9,0.9])

for ii = 1:size(X,2)-1
    plot(X(2:end-1,ii),Y(2:end-1,ii),...
        'LineStyle','none','MarkerEdgeColor','k','Marker','s',...
        'MarkerFaceColor',color(ii,:))
end
    
plot([0,2*pi,2*pi,0,0],[0,0,pi/2,pi/2,0],'k:')
axis equal
% axis([ -.1 2*pi+.1 -.1 pi/2+.1])
xlabel('\phi1'); ylabel('\Phi')
hold off

%%

for ii = 1:size(X,1)
    for jj = 1:size(X,2)
        
        tmp = gsh_hcp_tri_L_7(X(ii,jj),Y(ii,jj),0);
        gshall(:,ii,jj) = [real(tmp(2:3)'),tmp(4),imag(tmp(5:6)'),real(tmp(7:10)'),tmp(11),imag(tmp(12:15)')];
        
    end
end

%% 3D images of GSH coefficients

compA = 1;
compB = 5;
compC = 8;

figure(3)

for jj = 1:size(X,2)
    
    plot3(gshall(compA,:,jj),gshall(compB,:,jj),gshall(compC,:,jj),...
        'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
        'MarkerFaceColor',color(jj,:));
    hold on
    
end

hold off

xlabel(['gsh',int2str(compA)]);
ylabel(['gsh',int2str(compB)]);
zlabel(['gsh',int2str(compC)]);
axis tight equal; grid on;


%% Save 2D images of GSH coefficients

% ims = {}

for comp = 2:14

    compA = 1;
    compB = comp;
    
    figure(3+comp)
    
    for jj = 1:size(X,1)

        plot(squeeze(gshall(compA,jj,:)),squeeze(gshall(compB,jj,:)),...
            'LineStyle','none','MarkerEdgeColor','k','Marker','v',...
            'MarkerFaceColor',color(jj,:));
        hold on

    end
    
    xlabel(['gsh',int2str(compA)]);
    ylabel(['gsh',int2str(compB)]);
    axis tight equal; grid on;
    
%     ims{comp} = fullfile( 'gshplt', sprintf('gshplt_%i_%i.png',compA,compB) );
%     saveas( gcf, ims{comp} )

end