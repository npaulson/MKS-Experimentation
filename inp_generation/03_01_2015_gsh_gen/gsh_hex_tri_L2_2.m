function [out_tvalues]=gsh_hex_tri_L2_2(phi1, phi, phi2)

zvec = abs(phi) < 10e-17;
randvec = round(rand(size(zvec)));
randvecopp = ones(size(zvec)) - randvec;
phi = phi + (1e-7)*zvec.*(randvec - randvecopp);

out_tvalues = zeros(5, length(phi1));

t4 = sin(phi);
t6 = sqrt(0.6e1);
t8 = -t4 ^ 2 * t6 / 0.4e1;
t5 = cos(phi);
t7 = (-0.1e1 / 0.2e1*i) * sqrt(0.1e1 + t5) * sqrt(0.1e1 - t5) * t5 * t6;

out_tvalues(1, :) = exp((-2*i) * phi1) * t8;
out_tvalues(2, :) = exp((-1*i) * phi1) * t7;
out_tvalues(3, :) = 0.3e1 / 0.2e1 * t5 ^ 2 - 0.1e1 / 0.2e1;
out_tvalues(4, :) = exp((i) * phi1) * t7;
out_tvalues(5, :) = exp((2*i) * phi1) * t8;

