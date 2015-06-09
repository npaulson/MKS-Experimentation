function [ g ] = BungeMtrxMult( euler )
%BungeMtrx converts a set of Bunge Euler angles to a 3x3 matrix

phi1=euler(:,1);
Phi=euler(:,2);
phi2=euler(:,3);

g(1,1,:)=cos(phi1).*cos(phi2)-sin(phi1).*sin(phi2).*cos(Phi);
g(1,2,:)=sin(phi1).*cos(phi2)+cos(phi1).*sin(phi2).*cos(Phi);
g(1,3,:)=sin(phi2).*sin(Phi);
g(2,1,:)=-cos(phi1).*sin(phi2)-sin(phi1).*cos(phi2).*cos(Phi);
g(2,2,:)=-sin(phi1).*sin(phi2)+cos(phi1).*cos(phi2).*cos(Phi);
g(2,3,:)=cos(phi2).*sin(Phi);
g(3,1,:)=sin(phi1).*sin(Phi);
g(3,2,:)=-cos(phi1).*sin(Phi);
g(3,3,:)=cos(Phi);

end

