function [ Cs, CsM ] = stiffness_calc_hex( phi )

% phi: vector of bunge euler angles [phi1,Phi,phi2]
% Cs: 3x3x3x3 stiffness tensor
% CsM: 6x6 stiffness matrix

% These are the Elastic Stiffness Constants
C11 = 154;
C12 = 86;
C13 = 67;
C33 = 183;
C44 = 46;


z1 = [   cos(phi(1)), sin(phi(1)),           0;...
        -sin(phi(1)), cos(phi(1)),           0;...
                   0,           0,           1];

x =  [             1,           0,           0;...
                   0, cos(phi(2)), sin(phi(2));...
                   0,-sin(phi(2)), cos(phi(2))];

z2 = [   cos(phi(3)), sin(phi(3)),           0;...
        -sin(phi(3)), cos(phi(3)),           0;...
                   0,           0,           1];


g = (z2*x*z1)'; % transformation matrix from crystal to sample

%    g = zeros([3,3])    
%    
%    g[0,0] = cos(phi[0])*cos(phi[2])-sin(phi[0])*sin(phi[2])*cos(phi[1]);
%    g[0,1] = np.sin(phi[0])*np.cos(phi[2])+np.cos(phi[0])*np.sin(phi[2])*np.cos(phi[1]);
%    g[0,2] = np.sin(phi[2])*np.sin(phi[1]);
%    g[1,0] = -np.cos(phi[0])*np.sin(phi[2])-np.sin(phi[0])*np.cos(phi[2])*np.cos(phi[1]);
%    g[1,1] = -np.sin(phi[0])*np.sin(phi[2])+np.cos(phi[0])*np.cos(phi[2])*np.cos(phi[1]);
%    g[1,2] = np.cos(phi[2])*np.sin(phi[1]);
%    g[2,0] = np.sin(phi[0])*np.sin(phi[1]);
%    g[2,1] = -np.cos(phi[0])*np.sin(phi[1]);
%    g[2,2] = np.cos(phi[1]);    

Cs = zeros([3,3,3,3]);

for cc = 1 : 3^4
    [ii,jj,kk,ll] = ind2sub(size(Cs), cc);

    A1 = 0;   
    for tt = 1:3    
        A1 = A1 + g(ii,tt)*g(jj,tt)*g(kk,tt)*g(ll,tt);
    end
   
    A2 = 0.5*(g(ii,1)*g(jj,2)*g(kk,1)*g(ll,2)...
            + g(ii,1)*g(jj,2)*g(kk,2)*g(ll,1)...
            + g(ii,2)*g(jj,1)*g(kk,1)*g(ll,2)...
            + g(ii,2)*g(jj,1)*g(kk,2)*g(ll,1));  

    A =  A1 + A2 ;

    B = 0;

    for tt = 1:2
        B = B + g(ii,tt)*g(jj,tt)*g(kk,3)*g(ll,3)...
        + g(ii,3)*g(jj,3)*g(kk,tt)*g(ll,tt);
    end

    D = g(ii,3)*g(jj,3)*g(kk,3)*g(ll,3);    

    Cs(ii,jj,kk,ll) = C12*(ii==jj)*(kk==ll) +...
                      C44*((ii==kk)*(jj==ll) + (ii==ll)*(kk==jj)) +...
                      (C11 - C12 - 2*C44)*A +...
                      (C13 - C12)*B + ...
                      (C33 - C11)*D;
end

CsM = [Cs(1,1,1,1),Cs(1,1,2,2),Cs(1,1,3,3),Cs(1,1,2,3),Cs(1,1,1,3),Cs(1,1,1,2);...
       Cs(1,1,2,2),Cs(2,2,2,2),Cs(2,2,3,3),Cs(2,2,2,3),Cs(2,2,1,3),Cs(2,2,1,2);...
       Cs(1,1,3,3),Cs(2,2,3,3),Cs(3,3,3,3),Cs(3,3,2,3),Cs(3,3,1,3),Cs(3,3,1,2);...
       Cs(1,1,2,3),Cs(2,2,2,3),Cs(3,3,2,3),Cs(2,3,2,3),Cs(2,3,1,3),Cs(2,3,1,2);...
       Cs(1,1,1,3),Cs(2,2,1,3),Cs(3,3,1,3),Cs(2,3,1,3),Cs(1,3,1,3),Cs(1,3,1,2);...
       Cs(1,1,1,2),Cs(2,2,1,2),Cs(3,3,1,2),Cs(2,3,1,2),Cs(1,3,1,2),Cs(1,2,1,2)];
   
end
