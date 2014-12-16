function trial(tod,sn)

el=21;
na=25;

% nodesets(el);

first50=fopen('50top.inp','r');
bottom50=fopen('50bottom.inp','r');
periodic=fopen('periodicCE.inp','r');

A=fread(first50,inf);
B=fread(bottom50,inf);
P=fread(periodic,inf);

fclose(first50);
fclose(bottom50);
fclose(periodic);

nodesetspbc=fopen('nodesets.inp','r');
nodesetspbcx=fread(nodesetspbc,inf);
fclose(nodesetspbc);

for ii=1:na
    %     twopstatset(i,M);
    %     matsets=fopen(['matset' int2str(i) '.inp'],'r');
    %     materset=fread(matsets,inf);
    combined=fopen([int2str(el) '_aBTi_' int2str(ii) '_sn' int2str(sn) '.inp'],'w+');
    fwrite(combined,A);
    fprintf(combined,'\n');
    fwrite(combined,nodesetspbcx);
    fprintf(combined,'\n');
    fwrite(combined,P);
    fprintf(combined,'\n');
    includeorientationline(ii,tod,sn);
    include=['orienta' tod int2str(ii) int2str(sn) '.inp'];
    incl=fopen(include,'r');
    D=fread(incl,inf);
    %     fwrite(combined,materset);
    fwrite(combined,D);
    fprintf(combined,'\n');
    fwrite(combined,B);
    %     fclose(matsets);
    fclose(combined);
    fclose(incl);
    %     materialsets=['matset' int2str(i) '.inp'];
    %     delete(materialsets);
    delete(include);
%     fprintf('Done inp %i\n',ii)
end

fclose('all');