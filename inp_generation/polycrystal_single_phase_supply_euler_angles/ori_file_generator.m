% This code generates orientation values in ABAQUS format from random Euler
% angles for cubic-triclinic symmetry and puts it inside a distribution 
% table in ABAQUS inp file format.
% Yuksel C. Yabansu

% Edited by Noah Paulson to take in a single orientation file

% Number of elements on an edge
el=21;

% Arbirary file designations and print-outs (this file has been modified
% to only create on orientation file at a time)
ms=1;
sn=1;

orientation=zeros(3,3,el^3);

load euler_priddy_test.mat

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

orientation(:,:,:)=squeeze(g);

a=[1; 0; 0]/norm([1; 0; 0]);
b=[0.1; 1; 0]/norm([0.1; 1; 0]);

an=zeros(3,1,el^3);
bn=zeros(3,1,el^3);

for ii=1:el^3
    an(:,:,ii)=squeeze(g(:,:,ii)).'*a;
    bn(:,:,ii)=squeeze(g(:,:,ii)).'*b;
end

orient= 'orientation1.inp';

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
    