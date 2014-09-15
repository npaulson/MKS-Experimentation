ns = 200;
setid = 'cal';
num_per = 50;
el = 21;

c = 0;

for sn = 1 : num_per : ns
    
    load euler_200cal.mat
    euler = euler(:,sn:sn+num_per-1,:);

    eulerGSH = zeros(el^3,15,num_per);
    
    for sn_p = 1 : num_per
        for k = 1 : el^3
            eulerGSH(k,:,sn_p)= GSH_Hexagonal_Triclinic(euler(k,sn_p,1),euler(k,sn_p,2),euler(k,sn_p,3));
        end 
        
        disp(sn_p)
    end

    eulerGSH = permute(eulerGSH,[1 3 2]);
    
    save(['eulerGSH_', num2str(sn),'_to_',num2str(sn+num_per-1),'.mat'],'eulerGSH')
    
    clearvars eulerGSH
end

eulerGSH_tot = zeros(el^3,200,15);

for sn = 1 : num_per : ns
    filename = ['eulerGSH_', num2str(sn),'_to_',num2str(sn+num_per-1),'.mat'];
    load(filename,'eulerGSH')
    
    if any(isnan(eulerGSH(:))) == 1
        msg = ['sn ',num2str(sn), ': NaN exists'];
        disp(msg)
    else
        msg = ['sn ',num2str(sn), ': no NaNs present']; 
        disp(msg)
    end
    
    eulerGSH_tot(:,sn:sn+num_per-1,:) = eulerGSH;
    clearvars eulerGSH
end

if any(isnan(eulerGSH_tot(:))) == 1
    msg = 'total set: NaN exists';
    disp(msg)
else
    msg = 'total set: no NaNs present'; 
    disp(msg)
end

save(['euler_GSH_',num2str(ns),setid,'.mat'],'eulerGSH_tot')