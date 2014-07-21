% This code generates orientation values in ABAQUS format from random Euler
% angles for cubic-triclinic symmetry and puts it inside a distribution 
% table in ABAQUS inp file format.
% Yuksel C. Yabansu

% Modified by Noah Paulson for mixed cubic-triclinic symmetry and
% hexagonal-triclinic symmetry datasets

function []=orientationgenerator(na, set_id, M)
% Shuffling the matlab seed, so everytime this code runs matlab selects a
% unique seed according to the machine time.
rng('shuffle');

% Number of elements on an edge
el=21;

orientation = zeros(3,3,el^3,na);
ct = zeros(el^3,na);

load extremeorientc_hexa.mat
oriset_hexa = extremeorienth;
load extremeorientc_cube.mat
oriset_cube = extremeorienth;

for ms=1:na
    
    % In this section we generate a set indices from which to generate a
    % set of Bunge Euler angles for the hexagonal phase material.
    M1 = M(:,ms);
    c_hexa_pre = ceil(0.000001+(size(oriset_hexa,1)-0.000001).*rand(el^3,1));
    euler_hexa= [M1 M1 M1] .* oriset_hexa(c_hexa_pre,:);    
    c_hexa = M1 .* c_hexa_pre;

    % In this section we generate a set indices from which to generate a
    % set of Bunge Euler angles for the cubic phase material.    
    M2 = ones(el^3,1) - M1;
    c_cube_pre = ceil(0.000001+(size(oriset_cube,1)-0.000001).*rand(el^3,1));
    euler_cube = [M2 M2 M2] .* oriset_cube(c_cube_pre,:);    
    c_cube = M2 .* c_cube_pre;
    
    euler = euler_hexa + euler_cube;
    ct(:,ms) = c_hexa + c_cube;

    % Rotation matrix

    g=zeros(3,3,el^3);

    for ii=1:el^3
        Z1=[cos(euler(ii,1)) sin(euler(ii,1)) 0;...
            -sin(euler(ii,1)) cos(euler(ii,1)) 0; 0 0 1];
        X=[1 0 0; 0 cos(euler(ii,2)) sin(euler(ii,2));...
            0 -sin(euler(ii,2)) cos(euler(ii,2))];
        Z2=[cos(euler(ii,3)) sin(euler(ii,3)) 0;...
            -sin(euler(ii,3)) cos(euler(ii,3)) 0; 0 0 1];
        g(:,:,ii)=Z2*X*Z1;
    end

    orientation(:,:,:,ms)=squeeze(g);

    a=[1; 0; 0]/norm([1; 0; 0]);
    b=[0.1; 1; 0]/norm([0.1; 1; 0]);

    an=zeros(3,1,el^3);
    bn=zeros(3,1,el^3);

    for ii=1:el^3
        an(:,:,ii)=squeeze(g(:,:,ii)).'*a;
        bn(:,:,ii)=squeeze(g(:,:,ii)).'*b;
    end

    orient=['orientation' int2str(ms) '.inp'];

    fid=fopen(orient,'wt');

    fprintf(fid,'*Distribution Table, name=tab%i\n',ms);
    fprintf(fid,'COORD3D, COORD3D\n');
    fprintf(fid,'*Distribution, name=dist%i, location=element, table=tab%i\n',ms,ms);
    fprintf(fid,' ,1, 0, 0, 0, 1, 0\n');

    for jj=1:el^3-1
        fprintf(fid,'%i, %11i, %11i, %11i, %11i, %11i, %11i\n', jj,...
            an(1,:,jj), an(2,:,jj), an(3,:,jj),...
            bn(1,:,jj), bn(2,:,jj), bn(3,:,jj));
    end

    fprintf(fid,'%i, %11i, %11i, %11i, %11i, %11i, %11i\n', el^3,...
        an(1,:,el^3), an(2,:,el^3), an(3,:,el^3),...
        bn(1,:,el^3), bn(2,:,el^3), bn(3,:,el^3));

    fprintf(fid,'**\n');
    fprintf(fid,'*Orientation, name=ori%i, definition=coordinates\n',ms);
    fprintf(fid,' dist%i\n',ms);
    fprintf(fid,'3, 0\n');
    fprintf(fid,'**');

    fclose(fid);
    
end

orifile =['orientation' set_id '.mat'];
save(orifile,'orientationA','orientationB','ctA','ctB');


