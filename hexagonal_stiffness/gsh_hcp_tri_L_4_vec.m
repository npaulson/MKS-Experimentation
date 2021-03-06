function [out_tvalues, index_lmn] =gsh_hcp_tri_L_4_vec(phi1,phi)

zvec = abs(phi) < 10e-17;
randvec = round(rand(size(zvec)));
randvecopp = ones(size(zvec)) - randvec;
phi = phi + (1e-7)*zvec.*(randvec - randvecopp);
 
index_lmn = [];
t2 = exp((-2*1i) .* phi1);
t3 = sqrt(0.6e1);
t5 = cos(phi);
t6 = 0.1e1 - t5;
t7 = 0.1e1 + t5;
t8 = t6 .* t7;
t12 = exp((-1*1i) .* phi1);
t15 = sqrt(t6);
t16 = 0.1e1 ./ t15;
t17 = sqrt(t7);
t18 = t16 .* t17;
t19 = t6 .^ 2;
t23 = t7 .^ 2;
t27 = exp((1i) .* phi1);
t30 = 0.1e1 ./ t17;
t31 = t15 .* t30;
t36 = exp((2*1i) .* phi1);
t41 = exp((-4*1i) .* phi1);
t42 = sqrt(0.70e2);
t44 = t19 .* t23;
t48 = exp((-3*1i) .* phi1);
t50 = sqrt(0.35e2);
t52 = t15 .* t6;
t53 = 0.1e1 ./ t52;
t54 = t17 .* t7;
t55 = t53 .* t54;
t56 = t19 .* t6;
t57 = t56 .* t7;
t58 = t19 .^ 2;
t62 = sqrt(0.10e2);
t64 = 0.1e1 ./ t6;
t65 = t64 .* t7;
t66 = 0.360e3 .* t44;
t74 = sqrt(0.5e1);
t76 = t23 .* t7;
t77 = t6 .* t76;
t79 = 0.720e3 .* t44;
t85 = t23 .^ 2;
t99 = 0.1e1 ./ t7;
t100 = t6 .* t99;
t108 = exp((3*1i) .* phi1);
t111 = 0.1e1 ./ t54;
t112 = t52 .* t111;
t117 = exp((4*1i) .* phi1);

out_tvalues = zeros(15,length(phi1));
out_tvalues(1,:) = 1;
out_tvalues(2,:) = -(t2 .* t3 .* t8 ./ 4);
out_tvalues(3,:) = ((-0.1e1 / 0.4e1*1i) .* t12 .* t3 .* t18 .* (t8 - t19));
out_tvalues(4,:) = (t23 ./ 0.4e1 - t8 + t19 ./ 0.4e1);
out_tvalues(5,:) = ((0.1e1 / 0.4e1*1i) .* t27 .* t3 .* t31 .* (-t23 + t8));
out_tvalues(6,:) = -(t36 .* t3 .* t8 ./ 4);
out_tvalues(7,:) = (t41 .* t42 .* t44 ./ 16);
out_tvalues(8,:) = ((0.1e1 / 0.8e1*1i) .* t48 .* t50 .* t55 .* (t57 - t58));
out_tvalues(9,:) = -(t2 .* t62 .* t65 .* (t66 - 0.960e3 .* t57 + 0.360e3 .* t58) ./ 1920);
out_tvalues(10,:) = ((-0.1e1 / 0.960e3*1i) .* t12 .* t74 .* t18 .* (0.120e3 .* t77 - t79 + 0.720e3 .* t57 - 0.120e3 .* t58));
out_tvalues(11,:) = (t85 ./ 0.16e2 - t77 + 0.9e1 / 0.4e1 .* t44 - t57 + t58 ./ 0.16e2);
out_tvalues(12,:) = ((0.1e1 / 0.960e3*1i) .* t27 .* t74 .* t31 .* (-0.120e3 .* t85 + 0.720e3 .* t77 - t79 + 0.120e3 .* t57));
out_tvalues(13,:) = -(t36 .* t62 .* t100 .* (0.360e3 .* t85 - 0.960e3 .* t77 + t66) / 1920);
out_tvalues(14,:) = ((-0.1e1 / 0.8e1*1i) .* t108 .* t50 .* t112 .* (-t85 + t77));
out_tvalues(15,:) = (t117 .* t42 .* t44 ./ 16);


