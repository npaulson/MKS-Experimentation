function [ gsh ] = euler2gsh( euler, H )

gsh = zeros(size(euler,1),H);

for k = 1 : size(euler,1)
   
    gsh = GSH_Hexagonal_Triclinic_vec(...
        euler(:,1),...
        euler(:,2),...
        euler(:,3));
    
end

end