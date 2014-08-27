function []=nodesets(el)

Z=zeros(el+1,el+1);
for i=1:(el+1)*(el+1)
    Z(i)=i;
end

N=zeros(el+1,el+1,el+1);

for i=1:el+1
    N(:,:,i)=Z+(el+1)*(el+1)*(i-1);
end

n1plus=N(2:el,2:el,1);
n1minus=N(2:el,2:el,end);
n2plus=N(1,2:el,2:el);
n2minus=N(end,2:el,2:el);
n3plus=N(2:el,1,2:el);
n3minus=N(2:el,end,2:el);

n1plus_n2plus=N(1,2:el,1);
n1minus_n2plus=N(1,2:el,end);
n1plus_n2minus=N(end,2:el,1);
n1minus_n2minus=N(end,2:el,end);

n2plus_n3plus=N(1,1,2:el);
n2plus_n3minus=N(1,end,2:el);
n2minus_n3plus=N(end,1,2:el);
n2minus_n3minus=N(end,end,2:el);

n3plus_n1plus=N(2:el,1,1);
n3plus_n1minus=N(2:el,1,end);
n3minus_n1plus=N(2:el,end,1);
n3minus_n1minus=N(2:el,end,end);

n1plus=nonzeros(n1plus);
n1minus=nonzeros(n1minus);
n2plus=nonzeros(n2plus);
n2minus=nonzeros(n2minus);
n3plus=nonzeros(n3plus);
n3minus=nonzeros(n3minus);

n1plus_n2plus=nonzeros(n1plus_n2plus);
n1minus_n2plus=nonzeros(n1minus_n2plus);
n1plus_n2minus=nonzeros(n1plus_n2minus);
n1minus_n2minus=nonzeros(n1minus_n2minus);

n2plus_n3plus=nonzeros(n2plus_n3plus);
n2plus_n3minus=nonzeros(n2plus_n3minus);
n2minus_n3plus=nonzeros(n2minus_n3plus);
n2minus_n3minus=nonzeros(n2minus_n3minus);

n3plus_n1plus=nonzeros(n3plus_n1plus);
n3plus_n1minus=nonzeros(n3plus_n1minus);
n3minus_n1plus=nonzeros(n3minus_n1plus);
n3minus_n1minus=nonzeros(n3minus_n1minus);

% Writing the data to txt file in abaqus format

inpf=['nodesets.inp'];
inputfile=fopen(inpf,'w+');

fprintf(inputfile,'*Nset, nset=n1plus\n');

for i=1:12:12*floor(length(n1plus)/12)
    fprintf(inputfile,'%8i,',n1plus(i));
    fprintf(inputfile,'%8i,',n1plus(i+1));
    fprintf(inputfile,'%8i,',n1plus(i+2));
    fprintf(inputfile,'%8i,',n1plus(i+3));
    fprintf(inputfile,'%8i,',n1plus(i+4));
    fprintf(inputfile,'%8i,',n1plus(i+5));
    fprintf(inputfile,'%8i,',n1plus(i+6));
    fprintf(inputfile,'%8i,',n1plus(i+7));
    fprintf(inputfile,'%8i,',n1plus(i+8));
    fprintf(inputfile,'%8i,',n1plus(i+9));
    fprintf(inputfile,'%8i,',n1plus(i+10));
    fprintf(inputfile,'%8i,\n',n1plus(i+11));
end

for i=1:length(n1plus)-12*floor(length(n1plus)/12)
    fprintf(inputfile,'%8i,',n1plus(12*floor(length(n1plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n1minus\n');
for i=1:12:12*floor(length(n1minus)/12)
    fprintf(inputfile,'%8i,',n1minus(i));
    fprintf(inputfile,'%8i,',n1minus(i+1));
    fprintf(inputfile,'%8i,',n1minus(i+2));
    fprintf(inputfile,'%8i,',n1minus(i+3));
    fprintf(inputfile,'%8i,',n1minus(i+4));
    fprintf(inputfile,'%8i,',n1minus(i+5));
    fprintf(inputfile,'%8i,',n1minus(i+6));
    fprintf(inputfile,'%8i,',n1minus(i+7));
    fprintf(inputfile,'%8i,',n1minus(i+8));
    fprintf(inputfile,'%8i,',n1minus(i+9));
    fprintf(inputfile,'%8i,',n1minus(i+10));
    fprintf(inputfile,'%8i,\n',n1minus(i+11));
end

for i=1:length(n1minus)-12*floor(length(n1minus)/12)
    fprintf(inputfile,'%8i,',n1minus(12*floor(length(n1minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n2plus\n');
for i=1:12:12*floor(length(n2plus)/12)
    fprintf(inputfile,'%8i,',n2plus(i));
    fprintf(inputfile,'%8i,',n2plus(i+1));
    fprintf(inputfile,'%8i,',n2plus(i+2));
    fprintf(inputfile,'%8i,',n2plus(i+3));
    fprintf(inputfile,'%8i,',n2plus(i+4));
    fprintf(inputfile,'%8i,',n2plus(i+5));
    fprintf(inputfile,'%8i,',n2plus(i+6));
    fprintf(inputfile,'%8i,',n2plus(i+7));
    fprintf(inputfile,'%8i,',n2plus(i+8));
    fprintf(inputfile,'%8i,',n2plus(i+9));
    fprintf(inputfile,'%8i,',n2plus(i+10));
    fprintf(inputfile,'%8i,\n',n2plus(i+11));
end

for i=1:length(n2plus)-12*floor(length(n2plus)/12)
    fprintf(inputfile,'%8i,',n2plus(12*floor(length(n2plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n2minus\n');
for i=1:12:12*floor(length(n2minus)/12)
    fprintf(inputfile,'%8i,',n2minus(i));
    fprintf(inputfile,'%8i,',n2minus(i+1));
    fprintf(inputfile,'%8i,',n2minus(i+2));
    fprintf(inputfile,'%8i,',n2minus(i+3));
    fprintf(inputfile,'%8i,',n2minus(i+4));
    fprintf(inputfile,'%8i,',n2minus(i+5));
    fprintf(inputfile,'%8i,',n2minus(i+6));
    fprintf(inputfile,'%8i,',n2minus(i+7));
    fprintf(inputfile,'%8i,',n2minus(i+8));
    fprintf(inputfile,'%8i,',n2minus(i+9));
    fprintf(inputfile,'%8i,',n2minus(i+10));
    fprintf(inputfile,'%8i,\n',n2minus(i+11));
end

for i=1:length(n2minus)-12*floor(length(n2minus)/12)
    fprintf(inputfile,'%8i,',n2minus(12*floor(length(n2minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n3plus\n');
for i=1:12:12*floor(length(n3plus)/12)
    fprintf(inputfile,'%8i,',n3plus(i));
    fprintf(inputfile,'%8i,',n3plus(i+1));
    fprintf(inputfile,'%8i,',n3plus(i+2));
    fprintf(inputfile,'%8i,',n3plus(i+3));
    fprintf(inputfile,'%8i,',n3plus(i+4));
    fprintf(inputfile,'%8i,',n3plus(i+5));
    fprintf(inputfile,'%8i,',n3plus(i+6));
    fprintf(inputfile,'%8i,',n3plus(i+7));
    fprintf(inputfile,'%8i,',n3plus(i+8));
    fprintf(inputfile,'%8i,',n3plus(i+9));
    fprintf(inputfile,'%8i,',n3plus(i+10));
    fprintf(inputfile,'%8i,\n',n3plus(i+11));
end

for i=1:length(n3plus)-12*floor(length(n3plus)/12)
    fprintf(inputfile,'%8i,',n3plus(12*floor(length(n3plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n3minus\n');
for i=1:12:12*floor(length(n3minus)/12)
    fprintf(inputfile,'%8i,',n3minus(i));
    fprintf(inputfile,'%8i,',n3minus(i+1));
    fprintf(inputfile,'%8i,',n3minus(i+2));
    fprintf(inputfile,'%8i,',n3minus(i+3));
    fprintf(inputfile,'%8i,',n3minus(i+4));
    fprintf(inputfile,'%8i,',n3minus(i+5));
    fprintf(inputfile,'%8i,',n3minus(i+6));
    fprintf(inputfile,'%8i,',n3minus(i+7));
    fprintf(inputfile,'%8i,',n3minus(i+8));
    fprintf(inputfile,'%8i,',n3minus(i+9));
    fprintf(inputfile,'%8i,',n3minus(i+10));
    fprintf(inputfile,'%8i,\n',n3minus(i+11));
end

for i=1:length(n3minus)-12*floor(length(n3minus)/12)
    fprintf(inputfile,'%8i,',n3minus(12*floor(length(n3minus)/12)+i));
end
%%
fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n1plus_n2plus\n');
for i=1:12:12*floor(length(n1plus_n2plus)/12)
    fprintf(inputfile,'%8i,',n1plus_n2plus(i));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+1));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+2));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+3));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+4));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+5));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+6));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+7));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+8));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+9));
    fprintf(inputfile,'%8i,',n1plus_n2plus(i+10));
    fprintf(inputfile,'%8i,\n',n1plus_n2plus(i+11));
end

for i=1:length(n1plus_n2plus)-12*floor(length(n1plus_n2plus)/12)
    fprintf(inputfile,'%8i,',n1plus_n2plus(12*floor(length(n1plus_n2plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n1minus_n2plus\n');
for i=1:12:12*floor(length(n1minus_n2plus)/12)
    fprintf(inputfile,'%8i,',n1minus_n2plus(i));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+1));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+2));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+3));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+4));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+5));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+6));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+7));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+8));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+9));
    fprintf(inputfile,'%8i,',n1minus_n2plus(i+10));
    fprintf(inputfile,'%8i,\n',n1minus_n2plus(i+11));
end

for i=1:length(n1minus_n2plus)-12*floor(length(n1minus_n2plus)/12)
    fprintf(inputfile,'%8i,',n1minus_n2plus(12*floor(length(n1minus_n2plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n1plus_n2minus\n');
for i=1:12:12*floor(length(n1plus_n2minus)/12)
    fprintf(inputfile,'%8i,',n1plus_n2minus(i));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+1));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+2));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+3));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+4));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+5));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+6));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+7));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+8));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+9));
    fprintf(inputfile,'%8i,',n1plus_n2minus(i+10));
    fprintf(inputfile,'%8i,\n',n1plus_n2minus(i+11));
end

for i=1:length(n1plus_n2minus)-12*floor(length(n1plus_n2minus)/12)
    fprintf(inputfile,'%8i,',n1plus_n2minus(12*floor(length(n1plus_n2minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n1minus_n2minus\n');
for i=1:12:12*floor(length(n1minus_n2minus)/12)
    fprintf(inputfile,'%8i,',n1minus_n2minus(i));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+1));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+2));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+3));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+4));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+5));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+6));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+7));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+8));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+9));
    fprintf(inputfile,'%8i,',n1minus_n2minus(i+10));
    fprintf(inputfile,'%8i,\n',n1minus_n2minus(i+11));
end

for i=1:length(n1minus_n2minus)-12*floor(length(n1minus_n2minus)/12)
    fprintf(inputfile,'%8i,',n1minus_n2minus(12*floor(length(n1minus_n2minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n2plus_n3plus\n');
for i=1:12:12*floor(length(n2plus_n3plus)/12)
    fprintf(inputfile,'%8i,',n2plus_n3plus(i));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+1));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+2));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+3));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+4));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+5));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+6));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+7));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+8));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+9));
    fprintf(inputfile,'%8i,',n2plus_n3plus(i+10));
    fprintf(inputfile,'%8i,\n',n2plus_n3plus(i+11));
end

for i=1:length(n2plus_n3plus)-12*floor(length(n2plus_n3plus)/12)
    fprintf(inputfile,'%8i,',n2plus_n3plus(12*floor(length(n2plus_n3plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n2plus_n3minus\n');
for i=1:12:12*floor(length(n2plus_n3minus)/12)
    fprintf(inputfile,'%8i,',n2plus_n3minus(i));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+1));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+2));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+3));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+4));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+5));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+6));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+7));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+8));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+9));
    fprintf(inputfile,'%8i,',n2plus_n3minus(i+10));
    fprintf(inputfile,'%8i,\n',n2plus_n3minus(i+11));
end

for i=1:length(n2plus_n3minus)-12*floor(length(n2plus_n3minus)/12)
    fprintf(inputfile,'%8i,',n2plus_n3minus(12*floor(length(n2plus_n3minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n2minus_n3plus\n');
for i=1:12:12*floor(length(n2minus_n3plus)/12)
    fprintf(inputfile,'%8i,',n2minus_n3plus(i));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+1));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+2));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+3));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+4));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+5));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+6));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+7));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+8));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+9));
    fprintf(inputfile,'%8i,',n2minus_n3plus(i+10));
    fprintf(inputfile,'%8i,\n',n2minus_n3plus(i+11));
end

for i=1:length(n2minus_n3plus)-12*floor(length(n2minus_n3plus)/12)
    fprintf(inputfile,'%8i,',n2minus_n3plus(12*floor(length(n2minus_n3plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n2minus_n3minus\n');
for i=1:12:12*floor(length(n2minus_n3minus)/12)
    fprintf(inputfile,'%8i,',n2minus_n3minus(i));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+1));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+2));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+3));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+4));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+5));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+6));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+7));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+8));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+9));
    fprintf(inputfile,'%8i,',n2minus_n3minus(i+10));
    fprintf(inputfile,'%8i,\n',n2minus_n3minus(i+11));
end

for i=1:length(n2minus_n3minus)-12*floor(length(n2minus_n3minus)/12)
    fprintf(inputfile,'%8i,',n2minus_n3minus(12*floor(length(n2minus_n3minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n3plus_n1plus\n');
for i=1:12:12*floor(length(n3plus_n1plus)/12)
    fprintf(inputfile,'%8i,',n3plus_n1plus(i));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+1));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+2));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+3));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+4));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+5));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+6));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+7));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+8));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+9));
    fprintf(inputfile,'%8i,',n3plus_n1plus(i+10));
    fprintf(inputfile,'%8i,\n',n3plus_n1plus(i+11));
end

for i=1:length(n3plus_n1plus)-12*floor(length(n3plus_n1plus)/12)
    fprintf(inputfile,'%8i,',n3plus_n1plus(12*floor(length(n3plus_n1plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n3plus_n1minus\n');
for i=1:12:12*floor(length(n3plus_n1minus)/12)
    fprintf(inputfile,'%8i,',n3plus_n1minus(i));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+1));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+2));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+3));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+4));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+5));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+6));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+7));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+8));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+9));
    fprintf(inputfile,'%8i,',n3plus_n1minus(i+10));
    fprintf(inputfile,'%8i,\n',n3plus_n1minus(i+11));
end

for i=1:length(n3plus_n1minus)-12*floor(length(n3plus_n1minus)/12)
    fprintf(inputfile,'%8i,',n3plus_n1minus(12*floor(length(n3plus_n1minus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n3minus_n1plus\n');
for i=1:12:12*floor(length(n3minus_n1plus)/12)
    fprintf(inputfile,'%8i,',n3minus_n1plus(i));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+1));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+2));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+3));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+4));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+5));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+6));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+7));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+8));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+9));
    fprintf(inputfile,'%8i,',n3minus_n1plus(i+10));
    fprintf(inputfile,'%8i,\n',n3minus_n1plus(i+11));
end

for i=1:length(n3minus_n1plus)-12*floor(length(n3minus_n1plus)/12)
    fprintf(inputfile,'%8i,',n3minus_n1plus(12*floor(length(n3minus_n1plus)/12)+i));
end

fprintf(inputfile,'\n**');
fprintf(inputfile,'\n*Nset, nset=n3minus_n1minus\n');
for i=1:12:12*floor(length(n3minus_n1minus)/12)
    fprintf(inputfile,'%8i,',n3minus_n1minus(i));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+1));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+2));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+3));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+4));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+5));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+6));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+7));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+8));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+9));
    fprintf(inputfile,'%8i,',n3minus_n1minus(i+10));
    fprintf(inputfile,'%8i,\n',n3minus_n1minus(i+11));
end

for i=1:length(n3minus_n1minus)-12*floor(length(n3minus_n1minus)/12)
    fprintf(inputfile,'%8i,',n3minus_n1minus(12*floor(length(n3minus_n1minus)/12)+i));
end
fclose(inputfile);