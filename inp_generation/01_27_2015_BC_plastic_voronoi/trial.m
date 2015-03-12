clear
clc
close all

% number of elements per side
el=21;
% this is the number of total samples
% ns=190;

set_id = 'calRpc';

% M=zeros(el^3,ns);

% Deltas microstructures
% M(4631,1)=1;
% M(:,2)=1;
% M(4631,2)=0;

% 50percent VF microstructures
% for sn = 1:ns
%     M(:,sn) = rand(el^3,1) > .5;
% end

% Range of VF microstructures
% percentile = linspace(.01,.99,ns);
% for sn = 1:ns
%     M(:,sn) = rand(el^3,1) > percentile(sn);
% end

% Voronoi microstructures
N = round(linspace(250,10000,16));
vf = linspace(0.05,.95,25);

ns = length(N)*length(vf);
c = 0;

for ii = 1:length(N)
    for jj = 1:length(vf)
        c = c + 1;
        tmp = GenVoronoi(el, N(ii), vf(jj), 0);
        M(:,c) = tmp(:);
        
        vf(jj)
        N(ii)
        mean(tmp(:))
        
    end
end

%%
filename = ['M_',int2str(ns),set_id,'.mat'];
save(filename,'M')

% % Import M
% M = load(filename);
% M = M.M;

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