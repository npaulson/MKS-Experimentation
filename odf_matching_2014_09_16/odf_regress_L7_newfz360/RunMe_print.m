%% ODF Matching with fmincon
% Pen Patel, Noah Paulson 2014-10-17
%
% Use fmincon to find volume fractions for a set of orientations to
% match the ODF from the OIM software.

clear
clc

%% Load Data

load X_coeff
load Y_coeff

% order the GSH coefficients from our code and the OIM software the same
% way. The user should only leave the desired set of coefficients
% uncovered. The first set is for L == 4, the second set is for L == 6, and
% the third set is for L == 7.

% indXl = [4:6 11:15];
% indYl = [2 4:2:6 7 9:2:15];
% indXl = [4:6 11:15 28:2:40 29:2:41];
% indYl = [2 4:2:6 7 9:2:15 16 18:2:28 29 31:2:41];
indXl = [4:6 11:15 28:2:40 29:2:41 49:56];
indYl = [2 4:2:6 7 9:2:15 16 18:2:28 29 31:2:41 42 44:2:56];

X_coeff = X_coeff(indXl,:);
Y_coeff = Y_coeff(indYl,:);

%% Define equation to be optimized

% here we have arranged the optimization equation to give a single output,
% instead of being a system of linear equations.
f = @(V) sum(conj(Y_coeff - X_coeff*V).*(Y_coeff - X_coeff*V) );

%% Set up the fmincon optimization and get results

tic

% an initial guess for the volume fractions of each orientation
Vo = (1/size(X_coeff,2))*ones(size(X_coeff,2),1);
% Aeq * x = beq
Aeq = ones(size(X_coeff,2),size(X_coeff,2));
beq = ones(size(X_coeff,2),1);
% lb =< x <= ub
lb = zeros(size(X_coeff,2),1);
ub = ones(size(X_coeff,2),1);

% print the standard fmincon options
optimoptions('fmincon')
% options for fmincon: display info for each iterations, increase the
% maximum number of iterations and function evaluations.
options = optimoptions('fmincon','Display','iter',...
    'MaxFunEvals',10000000,'MaxIter',10000);

[x,fval,exitflag,output] = fmincon(f,Vo,[],[],Aeq,beq,lb,ub,[],options);

save('results','x','fval','exitflag','output')

% calculate array to compare the fmincon ODF to the OIM ODF.
rescomp = [X_coeff*x,Y_coeff]

toc


