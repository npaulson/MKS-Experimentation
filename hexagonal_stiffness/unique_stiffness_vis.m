load orientation_large

orisz = [length(phi1vec),length(Phivec),length(phi2vec)]

ctot =  100;
color = hsv(ctot);

unique_list1 = (unique_list1 + 1)';
unique_list2 = (unique_list2 + 1)';


A = accumarray(unique_list2,unique_list1,[],@(x) {x});

figure(1)

for ii = 1:size(A,1)
% for ii = 1 : length(unique_list2)

%     [I,J,K] = ind2sub(orisz,unique_list1(ii)); 
    
    % [I,J,K] = ind2sub(orisz,A{ii});

    phi1 = eulervec(A{ii},1);
    Phi = eulervec(A{ii},2);
    phi2 = eulervec(A{ii},3);

%     if ii == 1   
%         cnum = round((ctot - 1)*rand()) + 1;
%     elseif unique_list2(ii) ~= unique_list2(ii - 1)
%         cnum = round((ctot - 1)*rand()) + 1;
%     end
% 
%     plot3(phi1,Phi,phi2,...
%         'LineStyle','none',...
%         'Marker','o',...
%         'MarkerEdgeColor','k',...
%         'MarkerFaceColor',color(cnum,:),...
%         'MarkerSize',5)
% 
%     if ii == 1   
%         colorvec = [rand(),rand(),rand()];
%     elseif unique_list2(ii) ~= unique_list2(ii - 1)
%         colorvec = [rand(),rand(),rand()];
%     end

    colorvec = [rand(),rand(),rand()];

    
    plot3(phi1,Phi,phi2,...
        'LineStyle','none',...
        'Marker','o',...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor',colorvec,...
        'MarkerSize',5)


    hold on
    
    if ii < 50; pause(0.1); else; pause(0.001); end
    
    axis equal
    axis([0 2*pi 0 pi 0 pi/3])
end

hold off

xlabel('\phi_1'); ylabel('\Phi'); zlabel('\phi_2');
title('Orientations with Same Elastic Stiffness Tensors in the Hexagonal-Triclinic Fundamental Zone')