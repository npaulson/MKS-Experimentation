function [out_tvalues]=gsh_hex_tri_L2_2(phi1, phi, phi2)

zvec = abs(phi) < 10e-17;
randvec = round(rand(size(zvec)));
randvecopp = ones(size(zvec)) - randvec;
phi = phi + (1e-7)*zvec.*(randvec - randvecopp);

out_tvalues = zeros(5, length(phi1));

out_tvalues(1, :) = -exp((-2*i) * phi1) * sqrt(0.6e1) * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) / 4;
out_tvalues(2, :) = (-0.1e1 / 0.24e2*i) * exp((-1*i) * phi1) * sqrt(0.6e1) * ((0.1e1 - cos(phi)) ^ (-0.1e1 / 0.2e1)) * sqrt(0.1e1 + cos(phi)) * (0.6e1 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) - 0.6e1 * (0.1e1 - cos(phi)) ^ 2);
out_tvalues(3, :) = (0.1e1 + cos(phi)) ^ 2 / 0.4e1 - (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) + (0.1e1 - cos(phi)) ^ 2 / 0.4e1;
out_tvalues(4, :) = (0.1e1 / 0.24e2*i) * exp((i) * phi1) * sqrt(0.6e1) * sqrt(0.1e1 - cos(phi)) * ((0.1e1 + cos(phi)) ^ (-0.1e1 / 0.2e1)) * (-0.6e1 * (0.1e1 + cos(phi)) ^ 2 + 0.6e1 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)));
out_tvalues(5, :) = -exp((2*i) * phi1) * sqrt(0.6e1) * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) / 4;

