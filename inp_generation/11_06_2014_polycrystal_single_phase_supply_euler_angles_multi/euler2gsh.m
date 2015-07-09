function [ gsh_d, gsh_y ] = euler2gsh( euler, H )

gsh_d = zeros(size(euler,1),H);
gsh_y = zeros(size(euler,1),H);

for k = 1 : size(euler,1)
    
    gsh_d(k,:)= gsh_hcp_tri_L_7(...
        euler(k,1),...
        euler(k,2),...
        euler(k,3));

    gsh_y(k,:)= GSH_Hexagonal_Triclinic(...
        euler(k,1),...
        euler(k,2),...
        euler(k,3));
    
end

end