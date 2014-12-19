phi1 = 0:pi/12:2*pi;
phi = 0:pi/12:pi;
% phi2 = 0:pi/12:pi/3;

[PHI1, PHI] = meshgrid(phi1,phi);

figure(1)

plot(PHI1(:),PHI(:),...
    'LineStyle','none',...
    'Marker','o',...
    'MarkerEdgeColor','r',...
    'MarkerFaceColor','b',...
    'MarkerSize',5);

axis equal

gsh = gsh_hcp_tri_L_4_vec(PHI1(:),PHI(:));


orilist_old = 1:length(PHI1(:));
orilist_new = 1:length(PHI1(:));

unique_list1 = [];
unique_list2 = [];

for cc = 1:length(PHI1(:))
    
    if sum(orilist_old == cc) == 0 
        continue
    end
        
    for dd = orilist_old
        
        if all(abs(gsh(:,cc)-gsh(:,dd)) < 1E-5) == 1        
            orilist_new(orilist_new == dd) = [];
            unique_list1 = [unique_list1 ,dd];
            unique_list2 = [unique_list2, cc];
        end
    end
    orilist_old = orilist_new;
end


figure(2)

A = accumarray(unique_list2',unique_list1',[],@(x) {x});

for ii = 1:size(A,1)


    phi1 = PHI1(A{ii});
    Phi = PHI(A{ii});
    
    colorvec = [rand(),rand(),rand()];

    
    plot(phi1,Phi,...
        'LineStyle','none',...
        'Marker','o',...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor',colorvec,...
        'MarkerSize',5)

    hold on
    
    if ii < 50; pause(0.1); else; pause(0.001); end
    
    axis equal
    axis([0 2*pi 0 pi])
end

hold off

xlabel('\phi_1'); ylabel('\Phi');
title('Orientations with Same GSH coefficients in the Hexagonal-Triclinic Fundamental Zone')