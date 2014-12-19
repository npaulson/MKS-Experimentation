function [ euler ] = g2euler( g )

normal = squeeze(abs(g(3,3,:) - 1) > .0001)
altcase = ones(size(normal)) - normal

phi = zeros(size(normal));
euler = zeros(length(normal),3);

acos(g(3,3,:))

phi(normal) = acos(g(3,3,normal));

euler(normal,2) = phi(normal);
euler(normal,1) = atan2(g(3,1,normal)./sin(phi(normal)),...
    -g(3,2,normal)./sin(phi(normal)));
euler(normal,3) = atan2(g(1,3,normal)./sin(phi(normal)),...
    g(2,3,normal)./sin(phi(normal)));

if sum(altcase) > 0

    % in the altcase Phi = 0
    0.5*atan2(g(1,2,altcase),g(1,1,altcase))
    euler(altcase,1) = 0.5*atan2(g(1,2,altcase),g(1,1,altcase));
    euler(altcase,3) = euler(altcase,1);
    
end