clear
clc
format long
close all

na=3;

% Effective strain epsilon11

el=21;

strain=zeros(el^3*8,na);
strain11=zeros(el^3,na);

for ii=1:na
    
    datfile=[int2str(el) '_' int2str(ii) '_noah.dat'];
    datafile=fopen(datfile,'r');
    
    for j=1:247
        fgetl(datafile);
    end
    
    location=ftell(datafile);
    fseek(datafile,location,'bof');
    data=fscanf(datafile,'%g %g %g %g %g %g %g %g',[8 el^3*8]);
    data=data.';
    strain(:,ii)=data(:,3);
    fclose(datafile);
    fprintf('Done strain %i!\n',ii)
    
end

for ii=1:el^3
    strain11(ii,:)=sum(strain((ii-1)*8+1:ii*8,:),1)/8;
end

save strain11.mat strain11

fprintf('Done with mean values of integration values !\n')