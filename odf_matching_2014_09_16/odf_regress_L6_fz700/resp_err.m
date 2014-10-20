load X_coeff
load Y_coeff
load results320

% indXl = [4:6 11:15];
% indYl = [2 4:2:6 7 9:2:15];
indXl = [4:6 11:15 28:2:40 29:2:41];
indYl = [2 4:2:6 7 9:2:15 16 18:2:28 29 31:2:41];
% indXl = [4:6 11:15 28:2:40 29:2:41 49:56];
% indYl = [2 4:2:6 7 9:2:15 16 18:2:28 29 31:2:41 42 44:2:56];

X_coeff = X_coeff(indXl,:);
Y_coeff = Y_coeff(indYl,:);

errvec = 100*(abs(X_coeff*x - Y_coeff)./abs(Y_coeff))

errmeas = mean(errvec)