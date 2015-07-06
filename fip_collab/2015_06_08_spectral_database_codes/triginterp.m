function P = triginterp(xi,x,y)
% TRIGINTERP Trigonometric interpolation.
% Input:
%   xi  evaluation points for the interpolant (vector)
%   x   equispaced interpolation nodes (vector, length N)
%   y   interpolation values (vector, length N)
% Output:
%   P   values of the trigonometric interpolant (vector)
N = length(x);
% Adjust the spacing of the given independent variable.
h = 2/N;
scale = (x(2)-x(1)) / h;
x = x/scale;  xi = xi/scale;
% Evaluate interpolant.
P = zeros(size(xi));
for k = 1:N
  P = P + y(k)*trigcardinal(xi-x(k),N);
end