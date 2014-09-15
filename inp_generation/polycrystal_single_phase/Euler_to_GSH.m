ns = 200;
el = 21;

load euler_200cal.mat

euler_GSH = zeros(el^3,15,ns);

c = 0;

for sn = 1 : ns
    for k = 1 : el^3
        euler_GSH(k,:,sn)= GSH_Hexagonal_Triclinic(euler_200cal(k,sn,1),euler_200cal(k,sn,2),euler_200cal(k,sn,3));
        
        if any(isnan(euler_GSH(k,:,sn))) == 1
            c = c + 1;
            bad_euler(c,:) = euler_200cal(k,sn,:);
        end
        
    end
    sn
end

euler_GSH = permute(euler_GSH,[1 3 2]);

save('euler_GSH_200cal','euler_GSH');