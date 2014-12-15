function [Tsym]=GSH_Hexagonal_Triclinic(phi1,Phi,phi2)
% This code was modified to solve issues when Phi ~= 0

if abs(Phi) < 10e-17
    lil_const = 1e-7;
    binary = round(rand());
    if binary == 0
        random_num = -lil_const;
    elseif binary == 1
        random_num = lil_const;
    end
    Phi = Phi + random_num;
end

t1 = sqrt(0.6e1);
t3 = exp((-2*i) * phi1);
t5 = sin(Phi);
t6 = t5 ^ 2;
t9 = (-0.5e1 / 0.2e1*i) * t1;
t10 = cos(Phi);
t11 = 0.1e1 - t10;
t12 = sqrt(t11);
t14 = 0.1e1 + t10;
t15 = sqrt(t14);
t16 = t15 * t10;
t18 = exp((-1*i) * phi1);
t21 = t10 ^ 2;
t24 = exp((i) * phi1);
t29 = exp((2*i) * phi1);
t33 = sqrt(0.70e2);
t35 = exp((-4*i) * phi1);
t37 = t6 ^ 2;
t40 = sqrt(0.35e2);
t44 = t15 * t14;
t47 = exp((-3*i) * phi1);
t50 = sqrt(0.10e2);
t52 = 0.7e1 * t21;
t54 = t6 * (-0.1e1 + t52);
t57 = sqrt(0.5e1);
t66 = t21 ^ 2;
t75 = 0.1e1 / t12;
t87 = exp((3*i) * phi1);
t93 = exp((4*i) * phi1);
Tsym(1,1) = 1;
Tsym(2,1) = -((0.5e1 / 0.4e1) * t1 * t3 * t6);
Tsym(3,1) = (t9 * t12 * t16 * t18);
Tsym(4,1) = (-0.5e1 / 0.2e1 + 0.15e2 / 0.2e1 * t21);
Tsym(5,1) = (t9 * t24 * t16 * t12);
Tsym(6,1) = -((0.5e1 / 0.4e1) * t1 * t29 * t6);
Tsym(7,1) = ((0.9e1 / 0.16e2) * t33 * t35 * t37);
Tsym(8,1) = ((0.9e1 / 0.4e1*i) * t40 * t12 * t11 * t44 * t10 * t47);
Tsym(9,1) = -((0.9e1 / 0.8e1) * t50 * t3 * t54);
Tsym(10,1) = ((-0.9e1 / 0.4e1*i) * t57 * t18 * t12 * t15 * t10 * (-0.3e1 + t52));
Tsym(11,1) = (0.27e2 / 0.8e1 - 0.135e3 / 0.4e1 * t21 + 0.315e3 / 0.8e1 * t66);
Tsym(12,1) = ((0.9e1 / 0.4e1*i) * t57 * t24 * t16 * (0.3e1 - t52 - 0.3e1 * t10 + 0.7e1 * t21 * t10) * t75);
Tsym(13,1) = -((0.9e1 / 0.8e1) * t50 * t29 * t54);
Tsym(14,1) = ((0.9e1 / 0.4e1*i) * t10 * t44 * (0.1e1 + t21 - 0.2e1 * t10) * t87 * t40 * t75);
Tsym(15,1) = ((0.9e1 / 0.16e2) * t33 * t93 * t37);

Tsym=conj(Tsym);