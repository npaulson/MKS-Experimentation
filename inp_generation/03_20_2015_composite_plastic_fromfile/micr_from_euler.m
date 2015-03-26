function [ micr ] = micr_from_euler( euler, sn, el, vf, plotif)

euler_set = squeeze(euler(sn,:,:))';
unique_euler = unique(euler_set,'rows');
uni_num = size(unique_euler);

micr = zeros(1,el^3);

for ii = 1:uni_num(1)  
    row1 = euler_set(:,1) == unique_euler(ii,1);
    row2 = euler_set(:,2) == unique_euler(ii,2);
    row3 = euler_set(:,3) == unique_euler(ii,3);
    indx = logical(row1 .* row2 .* row3);
    
    micr(indx) = rand() < vf;
end

micr = reshape(micr,[el,el,el]);

if plotif == 1
    slc = 10;

    figure(1)
    image(micr(:,:,slc),'CDataMapping','scaled')
    set(gca,'YDir','normal')
    colorbar
    axis equal
    grid on
    axis([0.5 el+0.5 0.5 el+0.5])

    figure(2)
    euler_plt = reshape(euler(sn,1,:),[el,el,el]);
    image(euler_plt(:,:,slc),'CDataMapping','scaled')
    set(gca,'YDir','normal')
    colorbar
    axis equal
    grid on
    axis([0.5 el+0.5 0.5 el+0.5])
end

end