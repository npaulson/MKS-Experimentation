load orientations
load results

measct = round(1E4 * x);
oril = [];

for ii = 1:length(ori(:,1))
    oril = [orill; repmat(ori(ii,:),measct(ii),1)];
end

vlen = length(oril(:,1));

datamat = [oril,[0:vlen-1]',...
           zeros(vlen,1),...
           1400*ones(vlen,1),...
           0.8*ones(vlen,1),...
           ones(vlen,1),...
           ones(vlen,1),...
           .999*ones(vlen,1)];

ftop = fopen('front.ang','r');
ltop=fread(ftop,inf);
fclose(ftop);

wrtfil = fopen('odfdata.ang','w+');
fwrite(wrtfil,ltop);
% fwrite(wrtfil,'\n');

fprintf(wrtfil,' %8.5f %9.5f %9.5f %12.5f %12.5f %6.1f %6.3f %2d %6d %6.3f\n',datamat');

fclose(wrtfil);