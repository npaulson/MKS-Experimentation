clear
clc
close all

% number of elements per side
el=21;
% this is the number of total samples
ns=50;

set_id = 'cal';

M=zeros(el^3,ns);
% M(4631,1)=1;
% M(:,2)=1;
% M(4631,2)=0;

for sn = 1:ns
    M(:,sn) = rand(el^3,1) > .5;
end

%%
filename = ['M_',int2str(ns),set_id,'.mat'];
save(filename,'M')

% nodesets(el);
% loadings(el);
% fprintf('Data set loaded\n')

first50=fopen('50top.inp','r');
bcs_material_inp = fopen('bcs_material.inp','r');

A = fread(first50,inf);
B = fread(bcs_material_inp,inf);

fclose(first50);
fclose(bcs_material_inp);

nodesetspbc=fopen('nodesets.inp','r');
nodesetspbcx=fread(nodesetspbc,inf);
fclose(nodesetspbc);

for ii=1:ns
    twopstatset(ii,M);
    matsets=fopen(['matset' int2str(ii) '.inp'],'r');
    materset=fread(matsets,inf);
    combined=fopen(['sq' int2str(el) '_' int2str(ns) set_id '_' int2str(ii) '.inp'],'w+');
    fwrite(combined,A);
    fprintf(combined,'\n');
    fwrite(combined,nodesetspbcx);
    fprintf(combined,'\n');
    fwrite(combined,materset);
    fprintf(combined,'\n');
    fwrite(combined,B);
    fclose(matsets);
    fclose(combined);
    materialsets=['matset' int2str(ii) '.inp'];
    delete(materialsets);
    fprintf('Done inp %i\n',ii)
end

fclose('all');