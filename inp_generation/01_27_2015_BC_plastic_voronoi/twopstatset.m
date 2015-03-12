function []=twopstatset(na,M)

M=M';

firstphase=find(M(na,:)>0);
secondphase=find(M(na,:)<1);

matset1=zeros(1,length(firstphase));
matset2=zeros(1,length(secondphase));

for i=1:length(firstphase)
    matset1(i)=firstphase(i);
end

for i=1:length(secondphase)
    matset2(i)=secondphase(i);
end

materialset=['matset' int2str(na) '.inp'];

fid=fopen(materialset,'wt');

fprintf(fid,'**\n');
fprintf(fid,'*Elset, elset=elset1\n');
for i=1:11:11*floor(length(matset1)/11)
    fprintf(fid,'%8i,',matset1(i));
    fprintf(fid,'%8i,',matset1(i+1));
    fprintf(fid,'%8i,',matset1(i+2));
    fprintf(fid,'%8i,',matset1(i+3));
    fprintf(fid,'%8i,',matset1(i+4));
    fprintf(fid,'%8i,',matset1(i+5));
    fprintf(fid,'%8i,',matset1(i+6));
    fprintf(fid,'%8i,',matset1(i+7));
    fprintf(fid,'%8i,',matset1(i+8));
    fprintf(fid,'%8i,',matset1(i+9));
    fprintf(fid,'%8i,\n',matset1(i+10));
end

for i=1:length(matset1)-11*floor(length(matset1)/11)
    fprintf(fid,'%8i,',matset1(11*floor(length(matset1)/11)+i));
end

fprintf(fid,'\n**\n');

fprintf(fid,'*Elset, elset=elset2\n');
for i=1:11:11*floor(length(matset2)/11)
    fprintf(fid,'%8i,',matset2(i));
    fprintf(fid,'%8i,',matset2(i+1));
    fprintf(fid,'%8i,',matset2(i+2));
    fprintf(fid,'%8i,',matset2(i+3));
    fprintf(fid,'%8i,',matset2(i+4));
    fprintf(fid,'%8i,',matset2(i+5));
    fprintf(fid,'%8i,',matset2(i+6));
    fprintf(fid,'%8i,',matset2(i+7));
    fprintf(fid,'%8i,',matset2(i+8));
    fprintf(fid,'%8i,',matset2(i+9));
    fprintf(fid,'%8i,\n',matset2(i+10));
end

for i=1:length(matset2)-11*floor(length(matset2)/11)
    fprintf(fid,'%8i,',matset2(11*floor(length(matset2)/11)+i));
end

fclose(fid);