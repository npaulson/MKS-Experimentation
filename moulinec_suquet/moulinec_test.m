close all

%% Define Particle Shapes

ra = 4;

linvec = linspace(1,2*ra+1,2*ra+1);
[X,Y] = meshgrid(linvec,linvec);

% distances: array in the shape of X,Y where each entry is the
% euclidean distance of that cell from the central cell of the array
distances = sqrt((X-(ra + 1)).^2 +...
                 (Y-(ra + 1)).^2);

% sphindxl: array in shape of 'distances' with ones where the distance is
% less than the monomer radius.
ciro_ = find(distances <= (ra + 0.5));

ciro = zeros(length(ciro_),2);
[ciro(:,1), ciro(:,2)] = ind2sub(size(distances), ciro_);

% plot the shape of the monomer
% figure(1)
% 
% ciroplt = bsxfun(@minus,ciro,[ra+1, ra+1]);
% scatter(ciroplt(:,1), ciroplt(:,2))
% axis equal
% set(gcf, 'outerposition',[0 0 600 600]);


%% Generate Random Locations

el = 101;

el_ = el + 2*ra;

nrand = 40;

micr = zeros(el_,el_);
xrand = round((el-1)*rand(nrand,1)+1) + ra;
yrand = round((el-1)*rand(nrand,1)+1) + ra; 
allrand = [xrand,yrand];

randsub = sub2ind([el_,el_],xrand,yrand);

micr(randsub) = 1;

% figure(2)
% 
% imagesc(micr,'CDataMapping','scaled');
% title_ = 'random locations';
% title(title_)
% axis equal tight;
% colorbar


%% Insert Circles

for rr = 1:length(xrand)
    
    sqinx_ = bsxfun(@plus,ciro-(ra+1),allrand(rr,:));
    
    sqinx = sub2ind(size(micr),sqinx_(:,1),sqinx_(:,2));
    
    micr(sqinx) = 1;

end

% figure(3)
% 
% imagesc(micr,'CDataMapping','scaled');
% title_ = 'random squares';
% title(title_)
% axis equal tight;
% colorbar

%% Show final microstructure

micr = micr(ra+1:end-ra, ... % now remove the extraeneous edges
            ra+1:end-ra);
        
figure(3)

imagesc(micr,'CDataMapping','scaled');
title_ = 'random squares';
title(title_)
axis equal tight;
colorbar

%% Assign properties to phases, Initialize conditions

E0 = 200;
nu0 = 0.33;
mu0 = E0/(2*(1+nu0));
lambda0 = (E*nu0)/((1+nu0)*(1-2*nu0));

E1 = 180;
nu1 = 0.30;
mu1 = E1/(2*(1+nu1));
lambda1 = (E*nu1)/((1+nu1)*(1-2*nu1));


Ebar = 0.01; %applied strain

epsilon0 = Ebar*zeros(el,el);
sigma0 = 


greenfourier = 

