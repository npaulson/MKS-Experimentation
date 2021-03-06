fz_f_CT = zeros(222,3);
% fz_f_CT stands for "the faces of the fundamental zone with cubic crystal
% symmetry and triclinic sample symmetry"
% where fz_f_CT(?,1) is phi1, fz_f_CT(?,2) is Phi and
% fz_f_CT(?,3) is phi2

c = 0;
phi1_num = 15;
Phi_num = 4;
phi2_num = 5;

for ii = 1:phi1_num
    for jj = 1:Phi_num
        for kk = 1:phi2_num
            if ii==1 || ii==phi1_num || jj==1 || jj==Phi_num || kk==1 || kk==phi2_num
                c = c + 1;
                fz_f_CT(c,1) = (ii-1)*((2*pi())/(phi1_num-1));
                fz_f_CT(c,3) = (kk-1)*((pi()/4)/(phi2_num-1));
                Phi_min = acos(cos(fz_f_CT(c,3))/(1+cos(fz_f_CT(c,3))^2));
                if jj==1
                    fz_f_CT(c,2) = Phi_min;
                elseif jj==Phi_num
                    fz_f_CT(c,2) = pi()/2;
                else
                    Phi = (jj-1)*(((pi()/2)-Phi_min)/(Phi_num-1))+Phi_min;
                    fz_f_CT(c,2) = Phi;
%                     fz_f_CT(c,2) = Phi * sin(Phi);
                end
                    
                    
            end
        end
    end
end

% extremeorienth = fz_f_CT;
% for k = 1 : c
%     extremeorienth_fr = GSH_Cubic_Triclinic(fz_f_CT(k,1),fz_f_CT(k,2),fz_f_CT(k,3));
% end
% save('extremeorientc_cube.mat','extremeorienth','extremeorienth_fr')


figure(1)
scatter3(fz_f_CT(:,1),fz_f_CT(:,2),fz_f_CT(:,3))
axis equal
axis([-.2 2*pi+.2 -.2+pi/4 pi/2+.2 -.2 pi/4+.2])
xlabel('\phi1')
ylabel('\Phi')
zlabel('\phi2')

figure(2)
scatter(fz_f_CT(:,2),fz_f_CT(:,3))
axis equal
axis([-.2+pi/4 pi/2+.2 -.2 pi/4+.2])
xlabel('\Phi')
ylabel('\phi2')

