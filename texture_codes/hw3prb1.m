
n=5000;
phi1=(pi/2)*rand(1,n);
Phi=acos(rand(1,n));
phi2=(pi/2)*rand(1,n);

scatter(phi1,Phi,'.');
axis([0 pi/2 0 pi/2]);	
title('Random Orientation Distribution');
xlabel('\phi_1');	
ylabel('\Phi');