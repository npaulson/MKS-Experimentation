ns = 50;
el = 21;

load euler_50val.mat

euler_GSH = zeros(el^3,10,ns);

for sn = 1 : ns
    for k = 1 : el^3
        euler_GSH(k,:,sn)= GSH_Cubic_Triclinic(euler(k,sn,1),euler(k,sn,2),euler(k,sn,3));
    end
    sn
end

euler_GSH = permute(euler_GSH,[1 3 2]);

save('euler_cubic_GSH_50val','euler_GSH');