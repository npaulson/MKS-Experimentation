function [out_tvalues]=gsh_cubic_triclinic_L0_4(e_angles)

phi1 = e_angles(1, :);
phi = e_angles(2, :);
phi2 = e_angles(3, :);

zvec = abs(phi) < 10e-17;
randvec = round(rand(size(zvec)));
randvecopp = ones(size(zvec)) - randvec;
phi = phi + (1e-7)*zvec.*(randvec - randvecopp);

out_tvalues = zeros(10, length(phi1));

out_tvalues(1, :) = 1;
out_tvalues(2, :) = exp((-4*i) * phi2) * exp((-4*i) * phi1) * ((0.1e1 + cos(phi)) ^ 4) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) / 1344 + exp((-4*i) * phi2) * sqrt(0.70e2) * ((0.1e1 + cos(phi)) ^ 2) * ((0.1e1 - cos(phi)) ^ 2) * sqrt(0.21e2) / 96 + exp((-4*i) * phi2) * exp((4*i) * phi1) * ((0.1e1 - cos(phi)) ^ 4) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) / 1344;
out_tvalues(3, :) = (-0.1e1 / 0.336e3*i) * exp((-3*i) * phi2) * exp((-4*i) * phi1) * sqrt(0.1e1 - cos(phi)) * ((0.1e1 + cos(phi)) ^ (0.7e1 / 0.2e1)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) + (0.1e1 / 0.40320e5*i) * exp((-3*i) * phi2) * sqrt(0.35e2) * ((0.1e1 - cos(phi)) ^ (-0.3e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (0.3e1 / 0.2e1)) * (-0.840e3 * (0.1e1 - cos(phi)) ^ 4 + 0.840e3 * (0.1e1 + cos(phi)) * (0.1e1 - cos(phi)) ^ 3) * sqrt(0.21e2) + (0.1e1 / 0.336e3*i) * exp((-3*i) * phi2) * exp((4*i) * phi1) * ((0.1e1 - cos(phi)) ^ (0.7e1 / 0.2e1)) * sqrt(0.1e1 + cos(phi)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1);
out_tvalues(4, :) = -exp((-2*i) * phi2) * exp((-4*i) * phi1) * ((0.1e1 + cos(phi)) ^ 3) * (0.1e1 - cos(phi)) * sqrt(0.21e2) * sqrt(0.5e1) * sqrt(0.2e1) / 96 - exp((-2*i) * phi2) * sqrt(0.10e2) * (0.1e1 + cos(phi)) / (0.1e1 - cos(phi)) * (0.360e3 * (0.1e1 - cos(phi)) ^ 4 - 0.960e3 * (0.1e1 + cos(phi)) * (0.1e1 - cos(phi)) ^ 3 + 0.360e3 * (0.1e1 + cos(phi)) ^ 2 * (0.1e1 - cos(phi)) ^ 2) * sqrt(0.21e2) / 11520 - exp((-2*i) * phi2) * exp((4*i) * phi1) * (0.1e1 + cos(phi)) * ((0.1e1 - cos(phi)) ^ 3) * sqrt(0.21e2) * sqrt(0.5e1) * sqrt(0.2e1) / 96;
out_tvalues(5, :) = (0.1e1 / 0.672e3*i) * exp((-1*i) * phi2) * exp((-4*i) * phi1) * sqrt(0.14e2) * ((0.1e1 - cos(phi)) ^ (0.3e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (0.5e1 / 0.2e1)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) + (-0.1e1 / 0.5760e4*i) * exp((-1*i) * phi2) * sqrt(0.5e1) * ((0.1e1 - cos(phi)) ^ (-0.1e1 / 0.2e1)) * sqrt(0.1e1 + cos(phi)) * (-0.120e3 * (0.1e1 - cos(phi)) ^ 4 + 0.720e3 * (0.1e1 + cos(phi)) * (0.1e1 - cos(phi)) ^ 3 - 0.720e3 * (0.1e1 + cos(phi)) ^ 2 * (0.1e1 - cos(phi)) ^ 2 + 0.120e3 * (0.1e1 + cos(phi)) ^ 3 * (0.1e1 - cos(phi))) * sqrt(0.21e2) + (-0.1e1 / 0.672e3*i) * exp((-1*i) * phi2) * exp((4*i) * phi1) * sqrt(0.14e2) * ((0.1e1 - cos(phi)) ^ (0.5e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (0.3e1 / 0.2e1)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1);
out_tvalues(6, :) = exp((-4*i) * phi1) * sqrt(0.70e2) * ((0.1e1 + cos(phi)) ^ 2) * ((0.1e1 - cos(phi)) ^ 2) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) / 1344 + (((0.1e1 - cos(phi)) ^ 4 / 0.16e2 - (0.1e1 + cos(phi)) * (0.1e1 - cos(phi)) ^ 3 + 0.9e1 / 0.4e1 * (0.1e1 + cos(phi)) ^ 2 * (0.1e1 - cos(phi)) ^ 2 - (0.1e1 + cos(phi)) ^ 3 * (0.1e1 - cos(phi)) + (0.1e1 + cos(phi)) ^ 4 / 0.16e2) * sqrt(0.21e2) / 0.6e1) + exp((4*i) * phi1) * sqrt(0.70e2) * ((0.1e1 + cos(phi)) ^ 2) * ((0.1e1 - cos(phi)) ^ 2) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) / 1344;
out_tvalues(7, :) = (-0.1e1 / 0.672e3*i) * exp((i) * phi2) * exp((-4*i) * phi1) * sqrt(0.14e2) * ((0.1e1 - cos(phi)) ^ (0.5e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (0.3e1 / 0.2e1)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) + (0.1e1 / 0.5760e4*i) * exp((i) * phi2) * sqrt(0.5e1) * sqrt(0.1e1 - cos(phi)) * ((0.1e1 + cos(phi)) ^ (-0.1e1 / 0.2e1)) * (0.120e3 * (0.1e1 + cos(phi)) * (0.1e1 - cos(phi)) ^ 3 - 0.720e3 * (0.1e1 + cos(phi)) ^ 2 * (0.1e1 - cos(phi)) ^ 2 + 0.720e3 * (0.1e1 + cos(phi)) ^ 3 * (0.1e1 - cos(phi)) - 0.120e3 * (0.1e1 + cos(phi)) ^ 4) * sqrt(0.21e2) + (0.1e1 / 0.672e3*i) * exp((i) * phi2) * exp((4*i) * phi1) * sqrt(0.14e2) * ((0.1e1 - cos(phi)) ^ (0.3e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (0.5e1 / 0.2e1)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1);
out_tvalues(8, :) = -exp((2*i) * phi2) * exp((-4*i) * phi1) * (0.1e1 + cos(phi)) * ((0.1e1 - cos(phi)) ^ 3) * sqrt(0.21e2) * sqrt(0.5e1) * sqrt(0.2e1) / 96 - exp((2*i) * phi2) * sqrt(0.10e2) / (0.1e1 + cos(phi)) * (0.1e1 - cos(phi)) * (0.360e3 * (0.1e1 + cos(phi)) ^ 2 * (0.1e1 - cos(phi)) ^ 2 - 0.960e3 * (0.1e1 + cos(phi)) ^ 3 * (0.1e1 - cos(phi)) + 0.360e3 * (0.1e1 + cos(phi)) ^ 4) * sqrt(0.21e2) / 11520 - exp((2*i) * phi2) * exp((4*i) * phi1) * ((0.1e1 + cos(phi)) ^ 3) * (0.1e1 - cos(phi)) * sqrt(0.21e2) * sqrt(0.5e1) * sqrt(0.2e1) / 96;
out_tvalues(9, :) = (0.1e1 / 0.336e3*i) * exp((3*i) * phi2) * exp((-4*i) * phi1) * ((0.1e1 - cos(phi)) ^ (0.7e1 / 0.2e1)) * sqrt(0.1e1 + cos(phi)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) + (-0.1e1 / 0.40320e5*i) * exp((3*i) * phi2) * sqrt(0.35e2) * ((0.1e1 - cos(phi)) ^ (0.3e1 / 0.2e1)) * ((0.1e1 + cos(phi)) ^ (-0.3e1 / 0.2e1)) * (0.840e3 * (0.1e1 + cos(phi)) ^ 3 * (0.1e1 - cos(phi)) - 0.840e3 * (0.1e1 + cos(phi)) ^ 4) * sqrt(0.21e2) + (-0.1e1 / 0.336e3*i) * exp((3*i) * phi2) * exp((4*i) * phi1) * sqrt(0.1e1 - cos(phi)) * ((0.1e1 + cos(phi)) ^ (0.7e1 / 0.2e1)) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1);
out_tvalues(10, :) = exp((4*i) * phi2) * exp((-4*i) * phi1) * ((0.1e1 - cos(phi)) ^ 4) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) / 1344 + exp((4*i) * phi2) * sqrt(0.70e2) * ((0.1e1 + cos(phi)) ^ 2) * ((0.1e1 - cos(phi)) ^ 2) * sqrt(0.21e2) / 96 + exp((4*i) * phi2) * exp((4*i) * phi1) * ((0.1e1 + cos(phi)) ^ 4) * sqrt(0.21e2) * sqrt(0.7e1) * sqrt(0.5e1) * sqrt(0.2e1) / 1344;

