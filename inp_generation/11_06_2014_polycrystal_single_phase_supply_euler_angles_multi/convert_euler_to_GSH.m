load angleset_H15_phi2is0faceB.mat

load orientation_phi2is0face_150.mat

clear gshS 

ns = 150;
el = 21;
H = 15;

gshS = zeros(H,el^3,ns);

% for sn = 1:ns
%     for ori = 1 : size(euler,1)
% 
%         vec = sum(squeeze(eulerS(:,ns,:)),2) == sum(euler(ori,:),2);
%         gshS(vec,ns,:) = repmat(gsh(ori,:),[sum(vec),1]);
%         
%         if sn == 1 && ori == 1
%             sum(euler(ori,:),2)
%             sum(vec)
%             size(gshS(vec,ns,:))
%             size(repmat(gsh(ori,:),[sum(vec),1]))
%            
%         end
%     end
% end

for sn = 1:ns
    for k = 1:el^3
        gshS(:,k,sn) = GSH_Hexagonal_Triclinic(eulerS(k,sn,1),eulerS(k,sn,2),eulerS(k,sn,3));
    end
    sn
end

gshS = permute(gshS, [2, 3, 1]);
size(gshS)

save orientation_phi2is0faceB_150.mat orientation eulerS gshS