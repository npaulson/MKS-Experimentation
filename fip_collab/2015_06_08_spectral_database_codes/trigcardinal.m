function tau = trigcardinal(x,N)
ws = warning('off','MATLAB:divideByZero');
% Form is different for even and odd N.
if rem(N,2)==1   % odd
  tau = sin(N*pi*x/2) ./ (N*sin(pi*x/2));
else             % even
  tau = sin(N*pi*x/2) ./ (N*tan(pi*x/2));
end
warning(ws)
tau(x==0) = 1;     % fix value at x=0