close all

phi1 = 0:pi/6:2*pi;
phi = 0:pi/6:pi;
phi2 = 0:pi/6:pi/3;

[PHI1, PHI, PHI2] = meshgrid(phi1,phi,phi2);

figure(1)

plot3(PHI1(:),PHI(:),PHI2(:),...
    'LineStyle','none',...
    'Marker','o',...
    'MarkerEdgeColor','r',...
    'MarkerFaceColor','b',...
    'MarkerSize',5);

axis equal





CsM = zeros(6,6,length(PHI1(:)));

for cc = 1 : length(PHI1(:))
      
    [Cs,CsM(:,:,cc)] = stiffness_calc_hex([PHI1(cc),PHI(cc),PHI2(cc)]);

end


orilist_old = 1:length(PHI1(:));
orilist_new = 1:length(PHI1(:));

unique_list1 = [];
unique_list2 = [];

for cc = 1:length(PHI1(:))
    
    if sum(orilist_old == cc) == 0 
        continue
    end
        
    for dd = orilist_old
        
        if all(abs(CsM(:,:,cc)-CsM(:,:,dd)) < 1E-10) == 1        
            orilist_new(orilist_new == dd) = [];
            unique_list1 = [unique_list1 ,dd];
            unique_list2 = [unique_list2, cc];
        end
    end
    orilist_old = orilist_new;
end





figure(2)


A = accumarray(unique_list2',unique_list1',[],@(x) {x});

pause(.5)

for ii = 1:size(A,1)


    phi1 = PHI1(A{ii});
    Phi = PHI(A{ii});
    phi2 = PHI2(A{ii});

    
    colorvec = [rand(),rand(),rand()];

    
    plot3(phi1,Phi,phi2,...
        'LineStyle','none',...
        'Marker','s',...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor',colorvec,...
        'MarkerSize',9)

    hold on
    
    if ii < 50; pause(0.1); else; pause(0.001); end
    
    axis equal
    axis([0 2*pi 0 pi 0 pi/3])
end

hold off

xlabel('\phi_1'); ylabel('\Phi');
title('Orientations with same Stiffness Matrix')