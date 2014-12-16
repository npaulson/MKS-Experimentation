function [ greentensor ] = greensfourier( freq, mu, lambda )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

dim = 2;
greentensor = zeros(dim^4,1);


[]







for k = 1:dim^4
    [ii,jj,kk,hh] = ind2sub([dim,dim,dim,dim],k);
    
    greentensor(k) = (1/(4*mu*abs(freq)^2))*...
        (((kk==ii)*freq^2) + ((hh==ii)*freq^2) + ((kk==jj)*freq^2)+ ((hh==jj)*freq^2))-...
        ((lambda + mu)/(mu*(lambda+2*mu)))*...
        ((freq^4)/abs(freq)^4); 
        
end

