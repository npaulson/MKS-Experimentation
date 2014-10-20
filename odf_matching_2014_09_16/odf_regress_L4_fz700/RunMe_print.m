clear
clc

load X_coeff
load Y_coeff

indXl = [4:6 11:15];% 28:2:40 29:2:41];% 49:56];
indYl = [2 4:2:6 7 9:2:15];% 16 18:2:28 29 31:2:41];% 42 44:2:56];

X_coeff = X_coeff(indXl,:);
Y_coeff = Y_coeff(indYl,:);

f = @(V) sum(conj(Y_coeff - X_coeff*V).*(Y_coeff - X_coeff*V) );

%%
tic
Vo = rand(size(X_coeff,2),1);
Aeq = ones(size(X_coeff,2),size(X_coeff,2));
beq = ones(size(X_coeff,2),1);
lb = zeros(size(X_coeff,2),1);
ub = ones(size(X_coeff,2),1);

optimoptions('fmincon')

options = optimoptions('fmincon','Display','iter','MaxFunEvals',10000000,'MaxIter',10000);

[x,fval,exitflag,output] = fmincon(f,Vo,[],[],Aeq,beq,lb,ub,[],options);

save(['results', int2str(getfield(output,'iterations'))],'x','fval','exitflag','output')

toc


