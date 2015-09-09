function [ euler ] = rotmat2euler( g )

if abs(g(3,3) - 1) < .01

    Phi = 0;
    phi1 = 0.5*atan2(g(1,2),g(1,1));
    phi2 = phi1;
    
else
    
    Phi = acos(g(3,3));
    phi1 = atan2(g(3,1)/sin(Phi),-g(3,2)/sin(Phi));
    phi2 = atan2(g(1,3)/sin(Phi),g(2,3)/sin(Phi));
    
end

euler = [phi1,Phi,phi2];

end