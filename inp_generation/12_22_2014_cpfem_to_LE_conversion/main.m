%% Set up / specify variables

clear; clc; close('all'); rng('shuffle')

load euler_cal.mat
set_id = 'cal_Priddy';
el = 21;
H = 15;
ns = 100;

%% plot the selected set of euler angles

figure(1)

scatter3(euler(1,1,:),euler(1,2,:),euler(1,3,:),'bo')
xlabel('\phi_1'); ylabel('\Phi'); zlabel('\phi_2');
axis equal
axis([ min(euler(1,1,:))-.1, max(euler(1,1,:))+.1, ...
       min(euler(1,2,:))-.1, max(euler(1,2,:))+.1, ...
       min(euler(1,3,:))-.1, max(euler(1,3,:))+.1 ])


%% generate nodesets

nodesets(el)


%% generate main .inp files

inpgenerator(set_id,ns)


%% generate orientation .inp files

ori_file_generator(el,ns,set_id,euler);

%% generate gsh coefficients

gshS = zeros(el^3,ns,H);

for sn = 1:ns
    
%     size(GSH_Hexagonal_Triclinic_vec(euler(:,sn,1)',euler(:,sn,2)',euler(:,sn,3)'))
%     size(gshS(:,sn,:))
    
    gshS(:,sn,:) = squeeze(GSH_Hexagonal_Triclinic_vec(euler(sn,1,:),euler(sn,2,:),euler(sn,3,:)))';
end

filename = sprintf('micr_H%i_%s.mat',H,set_id);
save(filename,'gshS')
