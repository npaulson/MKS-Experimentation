clear
clc
close all

% number of elements per side
el=21;
% this is the number of total samples
na=1;
% 50% volume fraction dataset
M=round(rand(el^3,1));

%%

save M_50percent.mat M

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

twopstatset(1,M);
matsets=fopen(['matset' int2str(1) '.inp'],'r');
materset=fread(matsets,inf);
combined=fopen(['Yuksel_BCs' '.inp'],'w+');
fwrite(combined,A);
fprintf(combined,'\n');
fwrite(combined,nodesetspbcx);
fprintf(combined,'\n');
fwrite(combined,materset);
fprintf(combined,'\n');
fwrite(combined,B);
fclose(matsets);
fclose(combined);
materialsets=['matset' int2str(1) '.inp'];
delete(materialsets);
fprintf('Done inp')


fclose('all');