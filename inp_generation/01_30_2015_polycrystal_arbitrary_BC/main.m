%% Set up / specify variables

clear; clc; close('all'); rng('shuffle')

set_id = 'cal_rand_delta';
el = 21;
H = 15;
ns = 2;


%% angles for phi2 = 0 zero faces

v_phi1 = linspace(0,2*pi(),20);
v_Phi = acos(linspace(0,.95,5));

[X,Y] = meshgrid(v_phi1,v_Phi);

Xtop = X(1:end,1:end);
Ytop = Y(1:end,1:end);
top = [Xtop(:),Ytop(:)];

euler = [top; 0, 0];  euler = [euler, zeros(size(euler(:,1)))];


%% generate 'full' hexagonal-triclinic fundamental zone

% phi1len = 50;
% 
% v_phi1 = linspace(0,2*pi(),phi1len);
% v_Phi = acos(linspace(0,1,0.25*phi1len));
% v_phi2 = linspace(0,pi()/3,round(phi1len/6));
% [X,Y,Z] = meshgrid(v_phi1,v_Phi,v_phi2);
% 
% euler = [X(:),Y(:),Z(:)];
% 
% disp(length(X(:)))


%% plot the selected set of euler angles

figure(1)

scatter3(euler(:,1),euler(:,2),euler(:,3),'bo')
xlabel('\phi_1'); ylabel('\Phi'); zlabel('\phi_2');
axis equal
axis([ min(euler(:,1))-.1 max(euler(:,1))+.1 min(euler(:,2))-.1 max(euler(:,2))+.1 min(euler(:,3))-.1 max(euler(:,3))+.1])

%% convert euler angles to GSH coefficents

[gsh] = euler2gsh(euler,H);
gsh = gsh';

filename = sprintf('angleset_H%i_%s.mat',H,set_id);

save(filename,'euler','gsh')

%% generate nodesets

nodesets(el)


%% generate main .inp files

inpgenerator(set_id,ns)


%% generate orientation .inp files

angleset = ori_file_generator(el,ns,set_id,euler);

%% generate gsh coefficients

gshS = zeros(el^3,ns,H);

for sn = 1:ns
    gshS(:,sn,:) = gsh(angleset(:,sn),:);
end

filename = sprintf('micr_H%i_%s.mat',H,set_id);
save(filename,'gshS')
