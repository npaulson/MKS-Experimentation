ns = 200;
setid = 'cal';
el = 21;

c = 0;

for sn = 1 : 10 : ns
    
    load euler_200cal.mat
    euler = euler_200cal(:,sn:sn+9,:);
    clearvars euler_200cal

    eulerGSH = zeros(el^3,15,10);
    
    for sn_p = 1 : 10
        for k = 1 : el^3
            
            eulerGSH(k,:,sn_p)= GSH_Hexagonal_Triclinic(euler(k,sn_p,1),euler(k,sn_p,2),euler(k,sn_p,3));

            if any(isnan(eulerGSH(k,:,sn_p))) == 1
                c = c + 1;
%     %             bad_euler(c,:) = euler(k,sn,:);
            end

        end 
        
        sn_p
    end

    eulerGSH = permute(eulerGSH,[1 3 2]);
    
    save(['eulerGSH_', num2str(sn),'_to_',num2str(sn+9),'.mat'],'eulerGSH')
    
    clearvars eulerGSH
end

eulerGSH_tot = zeros(el^3,200,15);

for sn = 1 : 10 : ns
    filename = ['eulerGSH_', num2str(sn),'_to_',num2str(sn+9),'.mat'];
    load(filename,'eulerGSH')
    eulerGSH_tot(:,sn:sn+9,:) = eulerGSH;
    clearvars eulerGSH
end

any(isnan(eulerGSH_tot(:)))

save(['euler_GSH_',num2str(ns),setid,'.mat'],'eulerGSH_tot')