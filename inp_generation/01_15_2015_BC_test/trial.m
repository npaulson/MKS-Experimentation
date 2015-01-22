clear
clc
close all

% number of elements per side
el=21;
% this is the number of total samples
ns=2;

set_id = 'test';

M=zeros(el^3,ns);
M(4631,1)=1;
M(:,2)=1;
M(4631,2)=0;

% for sn = 1:ns
%     M(:,sn) = rand(el^3,1) > .3;
% end

%%
filename = ['M_',int2str(ns),set_id,'.mat'];
save(filename,'M')

top = fopen('top.inp','r');
A = fread(top,inf);
fclose(top);

nodesets = fopen('nodesets.inp','r');
B = fread(nodesets,inf);
fclose(nodesets);

boundary_conditions = fopen('boundary_conditions.inp','r');
C = fread(boundary_conditions,inf);
fclose(boundary_conditions);

materials = fopen('materials.inp','r');
D = fread(materials,inf);
fclose(materials);

velocity = fopen('velocity.inp','r');
E = fread(velocity,inf);
fclose(velocity);

output = fopen('output.inp','r');
F = fread(output,inf);
fclose(output);


for ii=1:ns
    twopstatset(ii,M);
    matsets=fopen(['matset' int2str(ii) '.inp'],'r');
    materset=fread(matsets,inf);
    combined=fopen(['sq' int2str(el) '_' int2str(ns) set_id '_' int2str(ii) '.inp'],'w+');
    fwrite(combined,A);
    fprintf(combined,'\n');
    fwrite(combined,B);
    fprintf(combined,'\n');
    fwrite(combined,materset);
    fprintf(combined,'\n');
    fwrite(combined,C);
    fprintf(combined,'\n');
    fwrite(combined,D);    
    fprintf(combined,'\n');
    fwrite(combined,E); 
    fprintf(combined,'\n');
    fwrite(combined,F);     
    fclose(matsets);
    fclose(combined);
    materialsets=['matset' int2str(ii) '.inp'];
    delete(materialsets);
    fprintf('Done inp %i\n',ii)
end

fclose('all');