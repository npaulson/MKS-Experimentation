clear; clc; close all;

el = 21;

M = single(rand(1,el^2) > .95);
% M = rand(1,el^3);


figure(1)
plot_micr(M,el)

h = fspecial('disk', 3);
M_alt = imfilter(M,h,'replicate');

% M_alt = imgaussfilt3(M,10,'FilterSize',[5,5,5]);
% M_alt = imgaussfilt3(M,10);

figure(2)
plot_micr(M_alt,el)

figure(3)
plot_micr(M_alt>.15,el)