inc = 10;
alpha = 0.5;
lwid = 1;

for p1 = 0:inc:360
    for P = 0:inc:90
        x = [p1, p1];
        y = [P, P];
        z = [0, 60];
        p = plot3(x, y, z, 'b', 'LineWidth', lwid);
        p.Color(4) = alpha;
        hold on
    end 
end

for p1 = 0:inc:360
    for p2 = 0:inc:60
        x = [p1, p1];
        y = [0, 90];
        z = [p2, p2];
        p = plot3(x, y, z, 'b', 'LineWidth', lwid);
        p.Color(4) = alpha;
    end 
end

for P = 0:inc:90
    for p2 = 0:inc:60
        x = [0, 360];
        y = [P, P];
        z = [p2, p2];
        p = plot3(x, y, z, 'b', 'LineWidth', lwid);
        p.Color(4) = alpha;
    end 
end

hold off

axis equal tight

xlabel('\phi_1')
ylabel('\Phi')
zlabel('\phi_2')