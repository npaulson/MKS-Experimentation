clear; clc; close all;

%%

f = @(x) sin(x)+0.5*cos(5*x);
rcvec = linspace(-1,1,100)';

xvar = rcvec;
yvar = f(rcvec);


%% fit legendre polynomial to function values

% order of the legendre polynomial to use
N = 5;

% find the roots of the legendre polynomial for the given truncation level
syms x
roots = double(vpasolve(legendreP(N,x) == 0));

Fk = zeros(N,1); 

for kk = 0:N-1

    tmp = 0;

    for nn = 1:N
        pk = legendreP(kk,roots(nn));
        pNm1 = legendreP(N-1,roots(nn));
        tmpval = 1-roots(nn)^2;
        fval = f(tmpval);
%         fval = interp1(xvar,yvar,tmpval,'spline');
        
        tmp = tmp + (fval*pk)/pNm1;
    end

    Fk(kk+1) = ((2*kk+1)/(N^2))*tmp;

end

%% plot the interpolation
recon = zeros(length(rcvec),1);
    
for kk = 0:N-1
    recon = recon + Fk(kk+1)*legendreP(kk,rcvec);
end

figure(2)
plot(xvar,yvar)
hold on
scatter(xvar,recon)

