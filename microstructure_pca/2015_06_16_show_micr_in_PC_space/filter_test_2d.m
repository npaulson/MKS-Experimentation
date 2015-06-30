clear; clc; close all;

el = 51;

M = single(rand(1,el^2) > .995);

M = reshape(M,[el,el]);

figure(1)
image(M,'CDataMapping','scaled')
set(gca,'YDir','normal')
colorbar
axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])

h = fspecial('motion',15,-30);
M_alt = imfilter(M,h,'replicate');

% M_alt = imgaussfilt3(M,10,'FilterSize',[5,5,5]);
% M_alt = imgaussfilt3(M,10);

figure(2)
image(M_alt,'CDataMapping','scaled')
set(gca,'YDir','normal')
colorbar
axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])

M_thresh = M_alt > mean(M_alt(:));

figure(3)
image(M_thresh,'CDataMapping','scaled')
set(gca,'YDir','normal')
colorbar
axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])

pdS = 25;
mask = padarray(ones(size(M_thresh)),[pdS,pdS]);

tmp = padarray(M_thresh,[pdS,pdS]);
numer = FullConv('a','n','m',tmp,mask);
tmp = padarray(ones(size(M_thresh)),[pdS,pdS]);
denom = FullConv('a','n','m',tmp,mask);

figure(4)
image(denom,'CDataMapping','scaled')
set(gca,'YDir','normal')
colorbar
axis equal
grid on
% axis([0.5 el+0.5 0.5 el+0.5])

sts = numer./denom;

figure(5)
image(sts(3*pdS+1:end-3*pdS,3*pdS+1:end-3*pdS),'CDataMapping','scaled')
set(gca,'YDir','normal')
colorbar
axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])