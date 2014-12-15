% Mesh generator with element and node information
% Yuksel C. Yabansu

clear
clc
close all
format short
opengl neverselect

% Window size
el=51;

% Number of nodes on an edge
no=el+1;

% Dimension of the RVE (in pixels)
di=20;

% 3-D configuration of node numbering
node3=permute(reshape(no^3:-1:1,no,no,no),[3 1 2]);

% 3-D configuration of element numbering
elem3=permute(reshape(el^3:-1:1,el,el,el),[3 1 2]);

% Coordinates of nodes in 3-D configuration
[Y X Z]=meshgrid(linspace(0,di,no),linspace(0,di,no),linspace(0,di,no));

% Initialization of mesh arrays
elemlist=zeros(el^3,9);
nodelist=zeros(no^3,4);

it=0;

for xx=1:el
    for yy=1:el
        for zz=1:el
            
            it=it+1;
            
            % Generating the element list
            nodesp=node3(xx:xx+1,yy:yy+1,zz:zz+1);
            elems=elem3(xx,yy,zz);
            elemlist(it,:)=[elems nodesp(7) nodesp(5) nodesp(1) nodesp(3) ...
                nodesp(8) nodesp(6) nodesp(2) nodesp(4)];
            
        end
    end
end

it=0;

for xx=1:no
    for yy=1:no
        for zz=1:no
            
            it=it+1;
            
            % Generating the node list
            nodes1=node3(xx,yy,zz);
            x=X(xx,yy,zz); y=Y(xx,yy,zz); z=Z(xx,yy,zz);
            nodelist(it,:)=[nodes1 x y z];
            
        end
    end
end

% Sort the node and element list
[~,nx]=sort(nodelist(:,1),1);
[~,ne]=sort(elemlist(:,1),1);

elemlist=elemlist(ne,:);
nodelist=nodelist(nx,:);

% Writing the element and node lists to txt file

nodefile=['mesh3D_' int2str(el) 'node.txt'];
elemfile=['mesh3D_' int2str(el) 'element.txt'];

fidnode=fopen(nodefile,'wt');
fprintf(fidnode,'%5i, %11.9g, %11.9g, %11.9g\n',nodelist.');
fclose(fidnode);

fidelem=fopen(elemfile,'wt');
fprintf(fidnode,'%5i, %8i, %8i, %8i, %8i, %8i, %8i, %8i, %8i\n',elemlist.');
fclose(fidelem);

fprintf('Done creating node and element definitions !\n');