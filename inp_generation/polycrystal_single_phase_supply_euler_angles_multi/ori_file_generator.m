% This code generates orientation values in ABAQUS format from random Euler
% angles for cubic-triclinic symmetry and puts it inside a distribution 
% table in ABAQUS inp file format.
% Yuksel C. Yabansu

% Edited by Noah Paulson to take in an orientation file

% Number of elements on an edge
el=21;

% ns = number of datasets
ns = 50;

set_id = 'val';

orientation=zeros(3,3,el^3,ns);

load euler_50val_s1.mat

    
for sn = 1 : ns
    
    g=zeros(3,3,el^3);
    
    % Rotation matrix
    for ii=1:el^3
        Z1=[cos(euler(ii,sn,1)) sin(euler(ii,sn,1)) 0;...
            -sin(euler(ii,sn,1)) cos(euler(ii,sn,1)) 0; 0 0 1];
        X=[1 0 0; 0 cos(euler(ii,sn,2)) sin(euler(ii,sn,2));...
            0 -sin(euler(ii,sn,2)) cos(euler(ii,sn,2))];
        Z2=[cos(euler(ii,sn,3)) sin(euler(ii,sn,3)) 0;...
            -sin(euler(ii,sn,3)) cos(euler(ii,sn,3)) 0; 0 0 1];
        g(:,:,ii)=Z2*X*Z1;
    end

    orientation(:,:,:,sn)=squeeze(g);

    a=[1; 0; 0]/norm([1; 0; 0]);
    b=[0.1; 1; 0]/norm([0.1; 1; 0]);

    an=zeros(3,1,el^3);
    bn=zeros(3,1,el^3);

    for ii=1:el^3
        an(:,:,ii)=squeeze(g(:,:,ii)).'*a;
        bn(:,:,ii)=squeeze(g(:,:,ii)).'*b;
    end

    orient=['orientation' int2str(sn) '.inp'];

    fid=fopen(orient,'wt');

    fprintf(fid,'*Distribution Table, name=tab%i\n',sn);
    fprintf(fid,'COORD3D, COORD3D\n');
    fprintf(fid,'*Distribution, name=dist%i, location=element, table=tab%i\n',sn,sn);
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
    fprintf(fid,'*Orientation, name=ori%i, definition=coordinates\n',sn);
    fprintf(fid,' dist%i\n',sn);
    fprintf(fid,'3, 0\n');
    fprintf(fid,'**');

    fclose(fid);
    
end

orifile=['orientation_' int2str(ns) set_id '.mat'];
save(orifile,'orientation');
    