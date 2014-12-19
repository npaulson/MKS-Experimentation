% this script generates a list of random integers
% unique_list1 contains indices of repeating elements
% unique_list2 contains group id's for the indices in unique_list1

gsh = round(10*rand(1,15))

orilist_old = 1:length(gsh);
orilist_new = 1:length(gsh);

unique_list1 = [];
unique_list2 = [];

for cc = 1:length(gsh)
    
    if sum(orilist_old == cc) == 0 
        continue
    end
        
    for dd = orilist_old
        
        if all(abs(gsh(:,cc)-gsh(:,dd)) < 1E-10) == 1        
            orilist_new(orilist_new == dd) = [];
            unique_list1 = [unique_list1, dd];
            unique_list2 = [unique_list2, cc];
        end
    end
    
    orilist_old = orilist_new;
    
end

unique_list1
unique_list2