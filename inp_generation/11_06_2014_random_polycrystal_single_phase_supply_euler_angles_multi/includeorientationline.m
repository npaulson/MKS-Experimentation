% This function is used in trial inp generator to create the lines that add
% the orientation in an inp file
% Yuksel C. Yabansu

function []=includeorientationline(ms)

orienta=['orienta' int2str(ms) '.inp'];
fid1=fopen(orienta,'wt');

fprintf(fid1,'**** ------------------------------------------------\n');
fprintf(fid1,'** MATERIALS\n');
fprintf(fid1,'**\n');
fprintf(fid1,'** Orientation file is included seperately as a distribution table\n');
fprintf(fid1,'**\n');
fprintf(fid1,'*Include, input=orientation%i.inp\n',ms);
fprintf(fid1,'**\n');
fprintf(fid1,'*Solid Section, elset=allel, material=material-1, orientation=ori%i\n',ms);
fprintf(fid1,'1.\n');
fprintf(fid1,'**');

fclose(fid1);