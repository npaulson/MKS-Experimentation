function [out_tvalues]=gsh_hex_tri_L2_4(phi1, phi, phi2)

zvec = abs(phi) < 10e-17;
randvec = round(rand(size(zvec)));
randvecopp = ones(size(zvec)) - randvec;
phi = phi + (1e-7)*zvec.*(randvec - randvecopp);

out_tvalues = zeros(14, length(phi1));

out_tvalues(1, :) = -exp((-2*i) * phi1) * sqrt(0.6e1) * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) / 4;
out_tvalues(2, :) = (-0.1e1 / 0.24e2*i) * exp((-1*i) * phi1) * sqrt(0.6e1) * ((0.1e1 - cos(phi)) ^ (-0.1e1 / 0.2e1)) * sqrt(0.1e1 + cos(phi)) * (0.6e1 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) - 0.6e1 * (0.1e1 - cos(phi)) ^ 2);
out_tvalues(3, :) = (0.1e1 + cos(phi)) ^ 2 / 0.4e1 - (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) + (0.1e1 - cos(phi)) ^ 2 / 0.4e1;
out_tvalues(4, :) = (0.1e1 / 0.24e2*i) * exp((i) * phi1) * sqrt(0.6e1) * sqrt(0.1e1 - cos(phi)) * ((0.1e1 + cos(phi)) ^ (-0.1e1 / 0.2e1)) * (-0.6e1 * (0.1e1 + cos(phi)) ^ 2 + 0.6e1 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)));
out_tvalues(5, :) = -exp((2*i) * phi1) * sqrt(0.6e1) * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) / 4;
out_tvalues(6, :) = exp((-4*i) * phi1) * sqrt(0.70e2) * ((0.1e1 - cos(phi)) ^ 2) * ((0.1e1 + cos(phi)) ^ 2) / 16;
out_tvalues(7, :) = (0.1e1 / 0.6720e4*i) * exp((-3*i) * phi1) * sqrt(0.35e2) * ((0.1e1 - cos(phi)) ^ (-0.3e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (0.3e1 / 0.2e1)) * (0.840e3 * (0.1e1 - cos(phi)) ^ 3 * (0.1e1 + cos(phi)) - 0.840e3 * (0.1e1 - cos(phi)) ^ 4);
out_tvalues(8, :) = -exp((-2*i) * phi1) * sqrt(0.10e2) / (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) * (0.360e3 * (0.1e1 - cos(phi)) ^ 2 * (0.1e1 + cos(phi)) ^ 2 - 0.960e3 * (0.1e1 - cos(phi)) ^ 3 * (0.1e1 + cos(phi)) + 0.360e3 * (0.1e1 - cos(phi)) ^ 4) / 1920;
out_tvalues(9, :) = (-0.1e1 / 0.960e3*i) * exp((-1*i) * phi1) * sqrt(0.5e1) * ((0.1e1 - cos(phi)) ^ (-0.1e1 / 0.2e1)) * sqrt(0.1e1 + cos(phi)) * (0.120e3 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) ^ 3 - 0.720e3 * (0.1e1 - cos(phi)) ^ 2 * (0.1e1 + cos(phi)) ^ 2 + 0.720e3 * (0.1e1 - cos(phi)) ^ 3 * (0.1e1 + cos(phi)) - 0.120e3 * (0.1e1 - cos(phi)) ^ 4);
out_tvalues(10, :) = (0.1e1 + cos(phi)) ^ 4 / 0.16e2 - (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) ^ 3 + 0.9e1 / 0.4e1 * (0.1e1 - cos(phi)) ^ 2 * (0.1e1 + cos(phi)) ^ 2 - (0.1e1 - cos(phi)) ^ 3 * (0.1e1 + cos(phi)) + (0.1e1 - cos(phi)) ^ 4 / 0.16e2;
out_tvalues(11, :) = (0.1e1 / 0.960e3*i) * exp((i) * phi1) * sqrt(0.5e1) * sqrt(0.1e1 - cos(phi)) * ((0.1e1 + cos(phi)) ^ (-0.1e1 / 0.2e1)) * (-0.120e3 * (0.1e1 + cos(phi)) ^ 4 + 0.720e3 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) ^ 3 - 0.720e3 * (0.1e1 - cos(phi)) ^ 2 * (0.1e1 + cos(phi)) ^ 2 + 0.120e3 * (0.1e1 - cos(phi)) ^ 3 * (0.1e1 + cos(phi)));
out_tvalues(12, :) = -exp((2*i) * phi1) * sqrt(0.10e2) * (0.1e1 - cos(phi)) / (0.1e1 + cos(phi)) * (0.360e3 * (0.1e1 + cos(phi)) ^ 4 - 0.960e3 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) ^ 3 + 0.360e3 * (0.1e1 - cos(phi)) ^ 2 * (0.1e1 + cos(phi)) ^ 2) / 1920;
out_tvalues(13, :) = (-0.1e1 / 0.6720e4*i) * exp((3*i) * phi1) * sqrt(0.35e2) * ((0.1e1 - cos(phi)) ^ (0.3e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (-0.3e1 / 0.2e1)) * (-0.840e3 * (0.1e1 + cos(phi)) ^ 4 + 0.840e3 * (0.1e1 - cos(phi)) * (0.1e1 + cos(phi)) ^ 3);
out_tvalues(14, :) = exp((4*i) * phi1) * sqrt(0.70e2) * ((0.1e1 - cos(phi)) ^ 2) * ((0.1e1 + cos(phi)) ^ 2) / 16;

