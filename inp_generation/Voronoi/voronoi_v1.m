clear; clc; close all;

el = 21;
bord = round(.5*el);

el_ = el + 2*bord;
n = 25;

x1vec = round((el_-1)*rand(1,n)+1);
x2vec = round((el_-1)*rand(1,n)+1);

micr = zeros(el_,el_);

linvec = 1:el_;
[X,Y] = meshgrid(linvec,linvec);

tmp = sqrt(bsxfun(@minus,X(:),x1vec).^2 +...
           bsxfun(@minus,Y(:),x2vec).^2);

tmp = reshape(tmp,[el_,el_,n]);

% find the indices of the seed which each x1,x2 location in the
% microstructure is closest to
[~, I] = min(tmp,[],3);

figure(1)

image(I,'CDataMapping','scaled')
set(gca,'YDir','normal')

hold on

scatter(x1vec,x2vec)
axis equal
grid on
axis([0.5 el_+0.5 0.5 el_+0.5])

figure(2)
micr = I(bord+1:bord+el,bord+1:bord+el);
image(micr,'CDataMapping','scaled')
set(gca,'YDir','normal')

axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])