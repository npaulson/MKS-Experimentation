function []=loadings(el)

nd = el + 1;

inpf= 'loading.inp';
inputfile=fopen(inpf,'w+');

set{1} = ['\n',int2str(nd^3),',1,3,0\n'];
set{2} = [int2str(nd^3 - nd^2 + nd),',1,3,0\n'];
set{3} = [int2str(nd^3 - el),',1,3,0\n'];
set{4} = [int2str(nd^3 - nd^2 + 1),',1,3,0\n'];

set{5} = [int2str(nd^2),',1,1,0.02\n'];
set{6} = [int2str(nd),',1,1,0.02\n'];
set{7} = [int2str(nd^2-el),',1,1,0.02\n'];
set{8} = [int2str(1),',1,1,0.02\n'];

set{9} = [int2str(nd^2),',2,3,0\n'];
set{10} = [int2str(nd),',2,3,0\n'];
set{11} = [int2str(nd^2-el),',2,3,0\n'];
set{12} = [int2str(1),',2,3,0\n'];

for ii = 1:12
    fprintf(inputfile,set{ii});
end