fileID = fopen('e11_coeff_add_L8_summary.txt','r');
formatSpec = '%d %f %f %f';
sizeA = [4 Inf];
orig = fscanf(fileID,formatSpec,sizeA);
orig = orig';
redu = orig(2:end,:);

% B1,I1 are for mean error
% B2,I2 are for average max error
% B3,I3 are for absolute max error

[B1,I1] = sort(redu(:,2));
[B2,I2] = sort(redu(:,3));
[B3,I3] = sort(redu(:,4));

cull = 17;

commonID = intersect(I1(1:cull),I2(1:cull));
% commonID = intersect(commonID,I3(1:cull));

disp(redu(commonID,:))

