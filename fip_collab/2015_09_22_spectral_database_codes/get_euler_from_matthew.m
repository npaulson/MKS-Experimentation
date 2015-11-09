euler = zeros(8,3);

for ii = 1:8
   
    g = [rmat(ii,1),rmat(ii,2),rmat(ii,3);
         rmat(ii,4),rmat(ii,5),rmat(ii,6);
         rmat(ii,7),rmat(ii,8),rmat(ii,9)];

    euler(ii, :) = rotmat2euler(g')*(180/pi);
     
     
end