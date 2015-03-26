clear; clc; close all;

el = 21;

n = 1000;

el_ = 3*el;
x1vec = round((el_-1)*rand(1,n)-(el-1));
x2vec = round((el_-1)*rand(1,n)-(el-1));
x3vec = round((el_-1)*rand(1,n)-(el-1));


micr = zeros(el,el,el);

linvec = 1:el;
[X,Y,Z] = meshgrid(linvec,linvec,linvec);

tmp = sqrt(bsxfun(@minus,X(:),x1vec).^2 +...
           bsxfun(@minus,Y(:),x2vec).^2 +...
           bsxfun(@minus,Y(:),x2vec).^2);

tmp = reshape(tmp,[el,el,el,n]);

% find the indices of the seed which each x1,x2,x3 location in the
% microstructure is closest to
[~, I] = min(tmp,[],4);

figure(1)

image(I(:,:,1),'CDataMapping','scaled')
set(gca,'YDir','normal')

axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])


figure(2)

micr = zeros(el,el,el);

for ii = unique(I)'    
    micr(I(:) == ii) = rand() > .5;
end

micr = reshape(micr,[el,el,el]);

image(micr(:,:,1),'CDataMapping','scaled')
set(gca,'YDir','normal')

axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])
