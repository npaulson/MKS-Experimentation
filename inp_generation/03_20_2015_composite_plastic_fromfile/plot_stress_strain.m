figure(1)

E1 = 115;
E2 = 145;
sigY_1 = 0.8;
sigY_2 = 1.2;
epsY_1 = sigY_1/E1;
epsY_2 = sigY_2/E2;

eps_dat_1 = [0,epsY_1,1.5*max([epsY_1,epsY_2])];
sig_dat_1 = [0, sigY_1, sigY_1];

eps_dat_2 = [0,epsY_2,1.5*max([epsY_1,epsY_2])];
sig_dat_2 = [0, sigY_2, sigY_2]; 

pc90to_yield = epsY_1 + 0.9*(epsY_2-epsY_1);

p1 = plot(eps_dat_1, sig_dat_1, 'b-');
hold on
p2 = plot(eps_dat_2, sig_dat_2, 'b-');

xlabel('\epsilon')
ylabel('\sigma (GPa)')
title('Responses for hard and soft \alpha-Ti crystal lattice orientations')

hold off