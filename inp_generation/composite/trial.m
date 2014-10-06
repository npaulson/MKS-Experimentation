clear
clc
close all

% number of elements per side
el=25;
% this is the number of total samples
ns=5;

set_id = 'val25el';

% % load 21ws_cont50_ms.mat
% % M=[Mcal Mval];
% 
% % creating microstructures
% M=zeros(el^3,ns);
% % the first and last are delta microstructes
% M(:,end)=ones(el^3,1);
% M(4631,1)=1;
% M(4631,end)=0;
% % M(:,3:na)=round(rand(el^3,na-2));
% 
% % assign volume fractions from (min,max,...)
% vf=linspace(0.01,0.99,ns-2);
% 
% for ii=2:ns-1
%     % randperm scrambles a vector of numbers
%     Mp=randperm(el^3).';
%     Mr=zeros(el^3,1);
%     % assign 1s to indices with value greater than vf
%     Mr(Mp<vf(ii-1)*el^3)=1;
%     M(:,ii)=Mr;
%     
% end

% 50% volume fraction validation dataset
M = zeros(el^3,ns);
for sn = 1 : ns
    M(:,sn) = round(rand(el^3,1));
end

%%
filename = ['M_',int2str(ns),set_id,'.mat'];
save(filename,'M')

nodesets(el);
loadings(el);
fprintf('Data set loaded\n')

first50=fopen('50top.inp','r');
bcs_material_inp = fopen('bcs_material.inp','r');
loading_inp = fopen('loading.inp','r');
output_inp = fopen('output.inp','r');

A = fread(first50,inf);
B = fread(bcs_material_inp,inf);
C = fread(loading_inp,inf);
D = fread(output_inp,inf);

fclose(first50);
fclose(bcs_material_inp);
fclose(loading_inp);
fclose(output_inp);

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
    fwrite(combined,C);
    fwrite(combined,D);
    fclose(matsets);
    fclose(combined);
    materialsets=['matset' int2str(ii) '.inp'];
    delete(materialsets);
    fprintf('Done inp %i\n',ii)
end

fclose('all');