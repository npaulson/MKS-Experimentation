function [out_tvalues]=gsh_hex_tri_L0_4new(phi1, phi, phi2)

zvec = abs(phi) < 10e-17;
randvec = round(rand(size(zvec)));
randvecopp = ones(size(zvec)) - randvec;
phi = phi + (1e-7)*zvec.*(randvec - randvecopp);

out_tvalues = zeros(15, length(phi1));

t17 = cos(phi);
t10 = 0.1e1 + t17;
t39 = t17 * sqrt(t10);
t15 = t17 ^ 2;
t12 = 0.7e1 * t15;
t38 = t12 - 0.3e1;
t37 = (0.1e1 / 0.4e1*i) * t39;
t11 = 0.1e1 - t17;
t24 = sqrt(t11);
t35 = t24 * t39;
t16 = sin(phi);
t14 = t16 ^ 2;
t21 = sqrt(0.6e1);
t34 = -t14 * t21 / 0.4e1;
t33 = -t14 * sqrt(0.10e2) * (t12 - 0.1e1) / 0.8e1;
t32 = t10 * sqrt(0.35e2) * t37;
t31 = t14 ^ 2 * sqrt(0.70e2) / 0.16e2;
t30 = (-0.1e1 / 0.2e1*i) * t21 * t35;
t22 = sqrt(0.5e1);
t9 = exp((-2*i) * phi1);
t8 = exp((-1*i) * phi1);
t7 = exp((i) * phi1);
t6 = exp((2*i) * phi1);
t4 = 0.1e1 / t24;

out_tvalues(1, :) = 1;
out_tvalues(2, :) = t9 * t34;
out_tvalues(3, :) = t8 * t30;
out_tvalues(4, :) = 0.3e1 / 0.2e1 * t15 - 0.1e1 / 0.2e1;
out_tvalues(5, :) = t7 * t30;
out_tvalues(6, :) = t6 * t34;
out_tvalues(7, :) = exp((-4*i) * phi1) * t31;
out_tvalues(8, :) = (t15 - 2 * t17 + 1) * exp((-3*i) * phi1) * t4 * t32;
out_tvalues(9, :) = t9 * t33;
out_tvalues(10, :) = t8 * t22 * (t38 * t17 - 7 * t15 + 3) * t4 * t37;
out_tvalues(11, :) = 0.3e1 / 0.8e1 + (-0.15e2 / 0.4e1 + 0.35e2 / 0.8e1 * t15) * t15;
out_tvalues(12, :) = (-0.1e1 / 0.4e1*i) * t7 * t22 * t38 * t35;
out_tvalues(13, :) = t6 * t33;
out_tvalues(14, :) = exp((3*i) * phi1) * t24 * t11 * t32;
out_tvalues(15, :) = exp((4*i) * phi1) * t31;

