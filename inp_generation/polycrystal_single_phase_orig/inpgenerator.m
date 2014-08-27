function inpgenerator()

el=21;
na=50;

nodesets(el);
fprintf('Data set loaded\n')

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
fclose('all');

for ii=1:na
    combined=fopen(['hcp_' int2str(el) 'el_200s_val_' int2str(ii) '.inp'],'w+');
    fwrite(combined,A);
    fprintf(combined,'\n');
    fwrite(combined,nodesetspbcx);
    fprintf(combined,'\n');
    fwrite(combined,P);
    fprintf(combined,'\n');
    includeorientationline(ii);
    include=['orienta' int2str(ii) '.inp'];
    incl=fopen(include,'r');
    D=fread(incl,inf);
    fwrite(combined,D);
    fprintf(combined,'\n');
    fwrite(combined,B);
    fclose(combined);
    fclose(incl);
    delete(include);
    fprintf('Done inp %i\n',ii)
end

fclose('all');