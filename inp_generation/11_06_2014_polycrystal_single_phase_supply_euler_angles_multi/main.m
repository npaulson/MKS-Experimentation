%% Set up / specify variables

clear; clc; close('all'); rng('shuffle')

set_id_gen = 'phi2is0edgeV3';
set_id_d = 'phi2is0edgeV3';
% set_id_y = 'phi2is0faceY';
el = 21;
H = 15;
ns = 150;


%% angles for phi2 = 0 zero faces (orientation invariant)

% phi1stop = 6.23;
% 
% v_phi1 = linspace(0,phi1stop,20);
% v_Phi = acos(0:1/(6-1):1);
% 
% [X,Y] = meshgrid(v_phi1,v_Phi);
% 
% topX = X(1:end-1,:);
% topY = Y(1:end-1,:);
% 
% eulerX = [topX(:);0;phi1stop];
% eulerY = [topY(:);0;0];
% 
% euler = [eulerX,eulerY,zeros(size(eulerX))];

%% angles for phi2 = 0 zero faces (not orientation invariant in Phi)

phi1stop = 6.23;

v_phi1 = linspace(0,phi1stop,20);
v_Phi = linspace(0,pi/2,6);

[X,Y] = meshgrid(v_phi1,v_Phi);

topX = X(1:end-1,:);
topY = Y(1:end-1,:);

eulerX = [topX(:);0;phi1stop];
eulerY = [topY(:);0;0];

euler = [eulerX,eulerY,zeros(size(eulerX))];

%% angles for phi2 = 0 face exterior w/ Phi = 0 edge gone

phi1edge = linspace(0,6.23,72);
top = ones(size(phi1edge))*(pi()/2); 

Phiedge = acos(linspace(0,1,16));
Phiedge = Phiedge(2:end);
left = zeros(size(Phiedge));
right = 6.23*ones(size(Phiedge));

euler = [phi1edge',top';...
         left',Phiedge';...
         right',Phiedge'];
         
euler = [euler, zeros(size(euler(:,1)))];


%% generate 'full' hexagonal-triclinic fundamental zone

% phi1len = 100;
% 
% v_phi1 = linspace(0,2*pi(),phi1len);
% v_Phi = acos(0:1/(0.25*phi1len-1):1);
% v_phi2 = linspace(0,pi()/3,round(phi1len/6));
% [X,Y,Z] = meshgrid(v_phi1,v_Phi,v_phi2);
% 
% euler = [X(:),Y(:),Z(:)];
% 
% disp(length(X(:)))

%% plot the selected set of euler angles

figure(1)

scatter(euler(:,1),euler(:,2),'bo')
xlabel('\phi_1'); ylabel('\Phi'); %zlabel('\phi_2')
axis equal
axis([ min(euler(:,1))-.1 max(euler(:,1))+.1 min(euler(:,2))-.1 max(euler(:,2))+.1])

%% convert euler angles to GSH coefficents

[gsh_d, gsh_y] = euler2gsh(euler,H);

filename = sprintf('angleset_H%i_%s.mat',H,set_id_d);
gsh = gsh_d;
save(filename,'euler','gsh')

% filename = sprintf('angleset_H%i_%s.mat',H,set_id_y);
% gsh = gsh_y;
% save(filename,'euler','gsh')

%% generate nodesets

nodesets(el)


%% generate main .inp files

inpgenerator(set_id_gen,ns)


%% generate orientation .inp files

angleset = ori_file_generator(el,ns,set_id_d,euler);

%% generate gsh coefficients

gshS_d = zeros(el^3,ns,H);
% gshS_y = zeros(el^3,ns,H);

for sn = 1:ns

    gshS_d(:,sn,:) = gsh_d(angleset(:,sn),:);
%     gshS_y(:,sn,:) = gsh_y(angleset(:,sn),:);

end

filename = sprintf('micr_H%i_%s.mat',H,set_id_d);
gshS = gshS_d;
save(filename,'gshS')

% filename = sprintf('micr_H%i_%s.mat',H,set_id_y);
% gshS = gshS_y;
% save(filename,'gshS')