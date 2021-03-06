% This function is used in trial inp generator to create the lines that add
% the orientation in an inp file
% Yuksel C. Yabansu

function []=includeorientationline(ms)

orienta=['orienta' int2str(ms) '.inp'];
fid1=fopen(orienta,'wt');

fprintf(fid1,'**** ------------------------------------------------\n');
fprintf(fid1,'** MATERIALS\n');
fprintf(fid1,'**\n');
fprintf(fid1,'** Orientation file is included separately as a distribution table\n');
fprintf(fid1,'**\n');
fprintf(fid1,'*Include, input=orientation%i.inp\n',ms);
fprintf(fid1,'**\n');
fprintf(fid1,'*Solid Section, elset=elsetl, material=material-1, orientation=ori%i\n',ms);
fprintf(fid1,'1.\n');
fprintf(fid1,'** Name: material-1, alpha phase titanium\n');
fprintf(fid1,'*Material, name=material-1\n');
fprintf(fid1,'*Elastic,type=anisotropic\n');
fprintf(fid1,'154, 86, 154, 67, 67, 183, 0, 0\n');
fprintf(fid1,'0, 34, 0, 0, 0, 0, 46, 0\n');
fprintf(fid1,'0, 0, 0, 0, 46\n');
fprintf(fid1,'**\n');
fprintf(fid1,'*Solid Section, elset=elset2, material=material-2, orientation=ori%i\n',ms);
fprintf(fid1,'1.\n');
fprintf(fid1,'** Name: material-2, beta phase titanium\n');
fprintf(fid1,'*Material, name=material-2\n');
fprintf(fid1,'*Elastic,type=anisotropic\n');
fprintf(fid1,'98, 83, 98, 83, 83, 98, 0, 0\n');
fprintf(fid1,'0, 38, 0, 0, 0, 0, 38, 0\n');
fprintf(fid1,'0, 0, 0, 0, 38\n');
fprintf(fid1,'**\n');

fclose(fid1);