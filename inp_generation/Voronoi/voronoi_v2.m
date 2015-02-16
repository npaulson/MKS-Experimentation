clear; clc; close all;

el = 21;

n = 400;

el_ = 3*el;
x1vec = round((el_-1)*rand(1,n)-(el-1));
x2vec = round((el_-1)*rand(1,n)-(el-1));

micr = zeros(el,el);

linvec = 1:el;
[X,Y] = meshgrid(linvec,linvec);

tmp = sqrt(bsxfun(@minus,X(:),x1vec).^2 +...
           bsxfun(@minus,Y(:),x2vec).^2);

tmp = reshape(tmp,[el,el,n]);

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
% axis([0.5 el+0.5 0.5 el+0.5])
axis([-el 2*el -el 2*el])


figure(2)

micr = zeros(el,el);

for ii = unique(I)'    
    micr(I(:) == ii) = rand() > 0.9;
end

micr = reshape(micr,[el,el]);

image(micr,'CDataMapping','scaled')
set(gca,'YDir','normal')

axis equal
grid on
axis([0.5 el+0.5 0.5 el+0.5])
