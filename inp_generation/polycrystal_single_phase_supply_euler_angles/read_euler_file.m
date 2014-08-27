fileID = fopen('euler_only.txt','r');
formatSpec = '%d %f';
sizeA = [5 9261];

A = fscanf(fileID,formatSpec,sizeA);
fclose(fileID);
