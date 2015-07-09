%% Set up / specify variables

clear; clc; close('all'); rng('shuffle')

set_id_gen = 'phi2is0edgeV4';
set_id_d = 'phi2is0edgeV4';
% set_id_y = 'phi2is0faceY';
el = 21;
H = 15;
ns = 150;


%% angles for phi2 = 0 zero faces

v_phi1 = linspace(0,2*pi(),12);
v_Phi = acos(0:1/(8-1):1);

[X,Y] = meshgrid(v_phi1,v_Phi);

kaled = [X(:,1),Y(:,1);X(end,2:end)',Y(end,2:end)';X(2:end-1,end),Y(2:end-1,end)];
exte = [X(1,2:end)',Y(1,2:end)'];
Xcent = X(2:end-1,2:end-1);
Ycent = Y(2:end-1,2:end-1);
cent = [Xcent(:),Ycent(:)];

euler = [kaled ; exte; cent];  euler = [euler, zeros(size(euler(:,1)))];

%% angles for phi2 = 0 face exterior

% phi1edge = linspace(0,2*pi(),30);
% top = ones(size(phi1edge))*(pi()/2);
% bottom = zeros(size(phi1edge)); 
% Phiedge = acos(linspace(0,1,20));
% Phiedge = Phiedge(2:end-1);
% left = zeros(size(Phiedge));
% right = ones(size(Phiedge))*(2*pi());
% 
% euler = [phi1edge',top';...
%          phi1edge',bottom';...
%          left',Phiedge';...
%          right',Phiedge'];
%          
% euler = [euler, zeros(size(euler(:,1)))];

%% angles for phi2 = 0 face exterior w/ Phi = 0 edge gone

% phi1edge = linspace(0,2*pi(),60);
% top = ones(size(phi1edge))*(pi()/2); 
% 
% Phiedge = acos(linspace(0,1,37));
% Phiedge = Phiedge(2:end);
% left = zeros(size(Phiedge));
% 
% euler = [phi1edge',top';...
%          left',Phiedge'];
%          
% euler = [euler, zeros(size(euler(:,1)))];


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