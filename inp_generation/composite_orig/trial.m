clear
clc
close all

% number of elements per side
el=21;
% this is the number of total samples
na=100;

% load 21ws_cont50_ms.mat
% M=[Mcal Mval];

% creating microstructures
M=zeros(el^3,na);
% the first and last are delta microstructes
M(:,end)=ones(el^3,1);
M(4631,1)=1;
M(4631,end)=0;
% M(:,3:na)=round(rand(el^3,na-2));

% assign volume fractions from (min,max,...)
vf=linspace(0.01,0.99,na-2);

for ii=2:na-1
    % randperm scrambles a vector of numbers
    Mp=randperm(el^3).';
    Mr=zeros(el^3,1);
    % assign 1s to indices with value greater than vf
    Mr(Mp<vf(ii-1)*el^3)=1;
    M(:,ii)=Mr;
    
end

% 50% volume fraction validation dataset
M=[M round(rand(el^3,1))];

%%

save M_seventhorder.mat M

nodesets(el);
fprintf('Data set loaded\n')

first50=fopen('50top.inp','r');
bottom50=fopen('50bottom.inp','r');

A=fread(first50,inf);
B=fread(bottom50,inf);

fclose(first50);
fclose(bottom50);

nodesetspbc=fopen('nodesets.inp','r');
nodesetspbcx=fread(nodesetspbc,inf);
fclose(nodesetspbc);

for ii=1: (na+1)
    twopstatset(ii,M);
    matsets=fopen(['matset' int2str(ii) '.inp'],'r');
    materset=fread(matsets,inf);
    combined=fopen(['sq' int2str(el) '_5cont_' int2str(ii) '.inp'],'w+');
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