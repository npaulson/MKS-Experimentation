clear; clc; close all;

el = 21;

M = single(rand(el,el,el) > .5);

figure(1)
plot_micr(reshape(M,[1,el^3]),el)

% M_ = imgaussfilt3(M,10,'FilterSize',[5,5,5]);
M_ = imgaussfilt3(M,1,'FilterSize',[21,21,21],'Padding','circular');


max_v = max(M_(:));
min_v = min(M_(:));

M_ = (M_- min_v)/(max_v-min_v);

figure(2)
plot_micr(reshape(M_,[1,el^3]),el)

M_thresh = M_ > mean(M_(:))+0*std(M_(:));

disp(mean(M_thresh(:)))

figure(3)
plot_micr(reshape(M_thresh,[1,el^3]),el)