% written by Noah Paulson 2/5/2015

file = 'texture.out';
 
fo = fopen( file , 'r');

nO =  fscanf(fo, '%f\n',1);
euler = fscanf(fo, '%f %f %f\n',[3 nO])';

fclose(fo);

save euler_out.mat nO euler