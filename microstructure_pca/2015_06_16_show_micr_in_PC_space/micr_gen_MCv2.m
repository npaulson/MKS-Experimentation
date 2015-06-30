clear; clc; close all;

% number of elements per side
el=21;
ns = 302;
M = zeros(ns,el^3);

c = 1;
c1s = c;
% Delta microstructures (2 total)
M(c,4631)=1;
c = c + 1;
M(c,:)=1;
M(c,4631)=0;
c = c + 1;
c1e = c-1;

c2s = c;
% half black, half white microstructures (66 total)
for ii = 0:el
    
    tmp = zeros(el,el,el);
    tmp(1:ii,:,:) = 1;
    M(c,:) = reshape(tmp,[1,el^3]);
    c = c + 1;

    tmp = zeros(el,el,el);
    tmp(:,1:ii,:) = 1;
    M(c,:) = reshape(tmp,[1,el^3]);
    c = c + 1;
    
    tmp = zeros(el,el,el);
    tmp(:,:,1:ii) = 1;
    M(c,:) = reshape(tmp,[1,el^3]);
    c = c + 1;
    
end
c2e = c - 1;

c3s = c;
% Random microstructures (20 total)
n_rand = 20;
percentile = linspace(.01,.99,n_rand);
for sn = 1:n_rand
    M(c,:) = rand(1,el^3) > percentile(sn);
    c = c + 1;
end
c3e = c - 1;

% c4s = c;
% % Voronoi microstructures (200 total)
% N = round(linspace(250,5000,10));
% vf = linspace(0.05,.95,20);
% 
% for ii = 1:length(N)
%     for jj = 1:length(vf)
%         tmp = GenVoronoi(el, N(ii), vf(jj), 0);
%         M(c,:) = tmp(:)';
%         c = c + 1;        
% 
%         vf(jj)
%         N(ii)
%         mean(tmp(:))   
%     end
% end
% c4e = c-1;

c5s = c;
% gaussian filter generated microstructures
vol_frac1 = linspace(.1,.9,10);
sigma = linspace(.5,2,5);
vol_frac2 = linspace(.1,.9,10);

for vf1 = vol_frac1 
for sig = sigma
for vf2 = vol_frac2
    tmp = single(rand(el,el,el) > vf1);
    tmp = imgaussfilt3(tmp,sig);
    max_v = max(tmp(:));
    min_v = min(tmp(:));
    tmp = (tmp - min_v)/(max_v-min_v);
    tmp = reshape(tmp,[1,el^3]);
    M(c,:) = tmp > vf2;
    c = c + 1;
end 
end
end
c5e = c-1;

%% Get the 2pt statistics

ns = c-1;

M_2pt = zeros(ns,el^3);

for ii = 1:ns
    
    tmp = reshape(M(ii,:),[el,el,el]);
    tmp = FullConv('a','p','r',tmp);
    M_2pt(ii,:) = reshape(tmp,[1,el^3])/(21^3);
    
end

%% Prepare the 2pt statistics for PCA

% pca first subracts the mean from each measurement and then performs SVD
% COEFF contains the eigenvalues themselves and SCORE is the original data
% expressed in PC space. Since our number of variables exceeds the number
% of observations the number of dimensions (PC variables) is reduced to the
% number of observations minus 1.
[COEFF,SCORE] = pca(M_2pt);

M_2pt_mean = mean(M_2pt, 1);
% M_2pt_ = bsxfun(@minus, M_2pt, M_2pt_mean);
% trial = M_2pt_ * COEFF;

pc_A = 1; pc_B = 2; pc_C = 3;

colnum = 20;
color = hsv(colnum);

% figure(1)
% for cc = 1:colnum
%     plot(cc,5,...
%         'LineStyle','none','Marker','o','MarkerEdgeColor','k',...
%         'MarkerFaceColor',color(cc,:),'MarkerSize',7);
%     hold on
% end
% hold off

figure(2)
plot3(SCORE(c1s:c1e,pc_A),SCORE(c1s:c1e,pc_B),SCORE(c1s:c1e,pc_C),...
    'LineStyle','none',...
    'MarkerEdgeColor','k',...
    'Marker','o',...
    'MarkerFaceColor',color(1,:),...
    'MarkerSize', 8)
hold on
plot3(SCORE(c2s:c2e,pc_A),SCORE(c2s:c2e,pc_B),SCORE(c2s:c2e,pc_C),...
    'LineStyle','none',...
    'MarkerEdgeColor','k',...
    'Marker','s',...
    'MarkerFaceColor',color(13,:))
plot3(SCORE(c3s:c3e,pc_A),SCORE(c3s:c3e,pc_B),SCORE(c3s:c3e,pc_C),...
    'LineStyle','none',...
    'MarkerEdgeColor','k',...
    'Marker','v',...
    'MarkerFaceColor',color(8,:))
% plot3(SCORE(c4s:c4e,pc_A),SCORE(c4s:c4e,pc_B),SCORE(c4s:c4e,pc_C),...
%     'LineStyle','none',...
%     'MarkerEdgeColor','k',...
%     'Marker','v',...
%     'MarkerFaceColor',color(4,:))
plot3(SCORE(c5s:c5e,pc_A),SCORE(c5s:c5e,pc_B),SCORE(c5s:c5e,pc_C),...
    'LineStyle','none',...
    'MarkerEdgeColor','k',...
    'Marker','v',...
    'MarkerFaceColor',color(18,:))

%% Perturb the microstructure and plot in PC space

% m_st = rand(1,el^3) > 0.5;
% tmp = reshape(m_st,[el,el,el]);
% tmp = FullConv('a','p','r',tmp);
% m_st_2pt = reshape(tmp,[1,el^3])/(21^3);
% m_st_pc = (m_st_2pt - M_2pt_mean) * COEFF;
% 
% figure(2)
% 
% plot3(m_st_pc(1,pc_A),...
%       m_st_pc(1,pc_B),...
%       m_st_pc(1,pc_C),...
%       'LineStyle','none',...
%       'MarkerEdgeColor','k',...
%       'Marker','s',...
%       'MarkerFaceColor',color(16,:),...
%       'MarkerSize', 12)
% 
% % m_pbO is the "old" version of the perturbed microstructure
% m_pbO = m_st;
% m_pbN = m_st;
% m_pbO_pc = m_st_pc;
% 
% cnt = 0;
% 
% for ii = 1:1000
%     
%     pdS = round(rand()*2+1);
% 
%     % identify a random voxel in the microstructre to switch
%     idxX = round(rand()*((el)-1)+1)+pdS;
%     idxY = round(rand()*((el)-1)+1)+pdS;
%     idxZ = round(rand()*((el)-1)+1)+pdS;
%     
%     % change the microstructure into 3D format
%     tmp = reshape(m_pbN,[el,el,el]);    
%     
%     tmp = padarray(tmp,[pdS,pdS,pdS]);
%     tmp(idxX-pdS:idxX+pdS,idxY-pdS:idxY+pdS,idxZ-pdS:idxZ+pdS) = rand()>.5;
%     
%     tmp = tmp(pdS+1:end-pdS,pdS+1:end-pdS,pdS+1:end-pdS);
%     
%     m_pbN = reshape(tmp,[1,el^3]);
%     
%     % perform the periodic 2pt statistics
%     tmp = FullConv('a','p','r',tmp);
%     % reshape to vector format
%     m_pb_2pt = reshape(tmp,[1,el^3])/(el^3);
%     % find the representation of the perturbed microstructre in the
%     % original PC space
%     m_pbN_pc = (m_pb_2pt - M_2pt_mean) * COEFF;
%     
%     distO = sqrt((m_pbO_pc(2:5) - m_st_pc(2:5)).^2);
%     distN = sqrt((m_pbN_pc(2:5) - m_st_pc(2:5)).^2);
%     
%     if distN > distO
%         m_pbO = m_pbN;
%         m_pbO_pc = m_pbN_pc;
%         cnt = cnt + 1;
%     end
%     
% end
% 
% plot3(m_pbN_pc(1,pc_A),...
%       m_pbN_pc(1,pc_B),...
%       m_pbN_pc(1,pc_C),...
%       'LineStyle','none',...
%       'MarkerEdgeColor','k',...
%       'Marker','s',...
%       'MarkerFaceColor',color(16,:),...
%       'MarkerSize', 12)
% 
% legend('deltas','halves','randoms','equiaxed','orig','prtrb')
% xlabel(['PC',int2str(pc_A)]);
% ylabel(['PC',int2str(pc_B)]);
% zlabel(['PC',int2str(pc_C)]);
% axis tight;
% % axis equal;
% grid on;

legend('deltas','halves','randoms','equiaxed','gaussian')
xlabel(['PC',int2str(pc_A)]);
ylabel(['PC',int2str(pc_B)]);
zlabel(['PC',int2str(pc_C)]);
axis tight;
% axis equal;
grid on;


% set_id = 'cal008';
%
% % Read Dream3D microstructures
% load euler_val.mat
% 
% eul_sz = size(euler);
% ns = eul_sz(1);
% 
% vf = linspace(0.05,.95,ns);
% 
% for sn = 1:ns
%     tmp = micr_from_euler( euler, sn, el, vf(sn), 0);
%     M(:,sn) = tmp(:);
%     vf(sn)
%     mean(tmp(:))
% end

% filename = ['M_',int2str(ns),'cal','.mat'];
% % save(filename,'M')
% 
% M = load(filename);
% M = M.M;