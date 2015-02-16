clear
close all

%The following code was developed for HW2, problem two for the course
%Texture, Microstructure and Anisotropy in 2014 by Noah Paulson. The code
%takes a specified crystal direction as well as the Bunge Euler angles and
%creates a pole figure. This specific instantiation applies orthorhombic
%sample symmetry as well.

run Symmetry_222.m
run Symmetry_432.m

%First we define the axes and a unit circle to make a pole figure template
%The circle function comes from Dr.Rosen in ME6103
axes1=[0,0,1.2;1.2,0,0];
circle1=circle(1,0,0,200);

%Here the axes and circle are plotted, and the correct scaling is applied.
plot3(axes1(1,:),axes1(2,:),[0,0,0],'k');
axis('equal');
axis([-1.3 1.3 -1.3 1.3 -1.3 1.3]);
hold on
plot3([0,0],[0,0],[0,1.2],'k');
plot3(circle1(1,:),circle1(2,:),circle1(3,:),'k');
xlabel('x-axis');
ylabel('y-axis');
title('Copper Component: \{111\} Pole Figure');

%normaldir is one normal to a crystal plane of interest in crystal space
normaldir=[1/sqrt(3);1/sqrt(3);1/sqrt(3)];
% normaldir=[1;0;0];

g=BungeMtrx(90,35,45);

%for i=1:4
    for j=1:24
        %in the following line, sym refers to cubic symmetry (applied 
        %to the crystal direction)while symorth is orthorhombic symmetry
        %(applied to sample)
        
        %symdir(:,j)= sym(:,:,j)*normaldir;
        %Hprime=symorth(:,:,i)'*g'*symdir(:,j);
        %galt=sym(:,:,j)*g*symorth(:,:,i);
        
        galt=sym(:,:,j)*g;
        Hprime=galt'*normaldir;
        
        
        % This 'if-statement' ensures that directions pointing below z=0
        % are not plotted
        if Hprime(3)>= -0.0001
            %the following four equations are from the lecture slides for
            %x-ray pole figures
            Theta=acos(Hprime(3));
            Phi=atan2(Hprime(2),Hprime(1));
            px=tan(Theta/2)*cos(Phi);
            py=tan(Theta/2)*sin(Phi);

            %plot3([0,Hprime(1)],[0,Hprime(2)],[0,Hprime(3)]);
            scatter3(px,py,0,'b');
        end
    end
%end

hold off