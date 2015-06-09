function [ g ] = BungeMtrx_v2( phis )
%BungeMtrx converts a set of Bunge Euler angles (deg) to a 3x3 matrix


phi1=phis(1)*(pi/180);
Phi=phis(2)*(pi/180);
phi2=phis(3)*(pi/180);

g(1,1)=cos(phi1)*cos(phi2)-sin(phi1)*sin(phi2)*cos(Phi);
g(1,2)=sin(phi1)*cos(phi2)+cos(phi1)*sin(phi2)*cos(Phi);
g(1,3)=sin(phi2)*sin(Phi);
g(2,1)=-cos(phi1)*sin(phi2)-sin(phi1)*cos(phi2)*cos(Phi);
g(2,2)=-sin(phi1)*sin(phi2)+cos(phi1)*cos(phi2)*cos(Phi);
g(2,3)=cos(phi2)*sin(Phi);
g(3,1)=sin(phi1)*sin(Phi);
g(3,2)=-cos(phi1)*sin(Phi);
g(3,3)=cos(Phi);

end

