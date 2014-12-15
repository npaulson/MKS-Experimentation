% This code generates orientation values in ABAQUS format from random Euler
% angles for cubic-triclinic symmetry and puts it inside a distribution 
% table in ABAQUS inp file format.
% Yuksel C. Yabansu

function []=randomorientation(tod,sn)

% Shuffling the data set
rng('shuffle');

% Number of data sets
na=25;

% Number of elements on an edge
el=21;

orientation=zeros(3,3,el^3,na);

load extremeorientc_cub.mat
load extremeorientc_hexa.mat

load procdata.mat

for ms=1:na   
    
    c=ct(:,ms,sn);
    
    euler=zeros(el^3,3);
    euler(cta(:,ms,sn)==0,:)=extremeorientc(c(cta(:,ms,sn)==0),:);
    euler(cta(:,ms,sn)==1,:)=extremeorienth(c(cta(:,ms,sn)==1),:);
    
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
	
    orient=['orientation' tod int2str(ms) 'sn' int2str(sn) '.inp'];
    
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

for nn=1:na
    
    els1=['elset1_' tod '_' int2str(nn) 'sn' int2str(sn) '.txt'];
    els2=['elset2_' tod '_' int2str(nn) 'sn' int2str(sn) '.txt'];
    
    fid1=fopen(els1,'wt');
    fid2=fopen(els2,'wt');
    
    for ii=1:el^3
        
        if cta(ii,nn,sn)==0;
            fprintf(fid1,'%i,\n',ii);
        elseif cta(ii,nn,sn)==1;
            fprintf(fid2,'%i,\n',ii);
        end
        
    end
    
    fprintf('Ms %i done !\n',nn);
    
    fclose('all');
    fclose all;
    
end

ct=ct(:,:,sn);
cta=cta(:,:,sn);

orifile=['orientation' tod int2str(sn) '.mat'];
save(orifile,'orientation','ct','cta');

trial(tod,sn);