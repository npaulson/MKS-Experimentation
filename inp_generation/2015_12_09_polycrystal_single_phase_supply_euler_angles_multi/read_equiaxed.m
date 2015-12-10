function [ pre_angleset ] = read_equiaxed(el,sn,euL)

file = sprintf('alpha_beta_volID12_%d.vtk', sn); 
fo = fopen( file , 'r');

% skip the header
for ii = 1:17
   fgetl(fo); 
end

readlen = ceil((el^3)/20); % number of lines to read

% grab the grain_ID data
temp = fscanf(fo,'%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n', [20, readlen]);

% keep only the info associated with el^3 voxels
temp = temp(1:el^3);

fclose(fo);

pre_angleset = zeros(el^3,1);

% assign the voxels with the same grain ID a random number in the range of
% 1 to euL (number of orientations to select from)
for ii = 1 : max(temp)
    pre_angleset(temp == ii) = round(1+rand()*(euL - 1));
end

end