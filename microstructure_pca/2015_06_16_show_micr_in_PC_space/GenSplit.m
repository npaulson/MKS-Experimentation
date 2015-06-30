function [ I ] = GenSplit( el, plotif)

el_ = 3*el;
x1vec = round((el_-1)*rand(1,2)-(el-1));
x2vec = round((el_-1)*rand(1,2)-(el-1));
x3vec = round((el_-1)*rand(1,2)-(el-1));

linvec = 1:el;
[X,Y,Z] = meshgrid(linvec,linvec,linvec);

tmp = sqrt(bsxfun(@minus,X(:),x1vec).^2 +...
           bsxfun(@minus,Y(:),x2vec).^2 +...
           bsxfun(@minus,Z(:),x3vec).^2);

tmp = reshape(tmp,[el,el,el,2]);

% find the indices of the seed which each x1,x2,x3 location in the
% microstructure is closest to
[~, I] = min(tmp,[],4);

I = I - 1;

if plotif == 1

    close all
    
    figure(1)

    image(I(:,:,1),'CDataMapping','scaled')
    set(gca,'YDir','normal')

    colorbar
    
    axis equal
    grid on
    axis([0.5 el+0.5 0.5 el+0.5])
    
    disp(mean(I(:)))
    
end

end
