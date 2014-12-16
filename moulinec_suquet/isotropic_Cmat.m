function [ Cmat ] = isotropic_Cmat( mu, lambda )

% multiply Cmat by strain in vector form:
% [e11,e22,e33,2*e23,2*e13,2*e12]'
% and get stress in vector form:
% [sig11, sig22, sig33, sig23, sig13, sig12]'
Cmat = zeros(6,6);
Cmat(1,1) = 2*mu + lambda;
Cmat(2,2) = 2*mu + lambda;
Cmat(3,3) = 2*mu + lambda;
Cmat(4,4) = mu;
Cmat(5,5) = mu;
Cmat(6,6) = mu;
Cmat(1,2) = lambda;
Cmat(1,3) = lambda;
Cmat(2,3) = lambda;
Cmat(2,1) = lambda;
Cmat(3,1) = lambda;
Cmat(3,2) = lambda;

end