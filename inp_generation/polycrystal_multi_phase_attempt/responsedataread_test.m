
% sn == set number
sn = 1;

% Number of data
na=200;

% Number of element in an edge
elm=21;

% stressgl=zeros(elm^3,6,na);

strainglt=zeros(elm^3*8,6,na);
straingl=zeros(elm^3,6,na);

% Coordinates and Displacements

for ii=1:na
    
    datafile=['hcp_' int2str(elm) 'el_' int2str(na) 's_' int2str(ii) '.dat'];
    datfile=fopen(datafile,'r');
    
    for j=1:251
        fgetl(datfile);
    end
    
    location=ftell(datfile);
    fseek(datfile,location,'bof');
    strainraw=fscanf(datfile,'%g %g %*s %g %g %g %g %g %g',[8 elm^3*8]);
    strainrow=strainraw(3:8,:).';
    strainglt(:,:,ii)=strainrow;
    
    fclose(datfile);
    
    for jj=1:elm^3
        straingl(jj,:,ii)=sum(strainglt((jj-1)*8+1:jj*8,:,ii),1)./8;
    end
    
end

%% Transformation of stresses and strains to global frame

orifile=['orientation' int2str(sn) '.mat'];
load(orifile);

strain=zeros(elm^3,6,na);

for ms=1:na
    for ii=1:elm^3
        
        % Transformation of stress from local to global
        elstrainloc=[straingl(ii,1,ms) straingl(ii,4,ms)/2 straingl(ii,5,ms)/2;...
            straingl(ii,4,ms)/2 straingl(ii,2,ms) straingl(ii,6,ms)/2;...
            straingl(ii,5,ms)/2 straingl(ii,6,ms)/2 straingl(ii,3,ms)];
        elstraingl=squeeze(orientation(:,:,ii,ms)).'*elstrainloc*...
            squeeze(orientation(:,:,ii,ms));
        
        if ms == 1 && ii == 1
            normal = squeeze(orientation(:,:,ii,ms))
            transpose = squeeze(orientation(:,:,ii,ms)).'
            elstraingl
        end
            
        
        strain(ii,:,ms)=[elstraingl(1,1) elstraingl(2,2) elstraingl(3,3) ...
            elstraingl(1,2) elstraingl(1,3) elstraingl(2,3)];
        
    end
    
    fprintf('Transformation done RVE %i\n',ms);
    
end

strainfile=['strain' int2str(sn) '.mat'];
save(strainfile,'strain')

fprintf('Done reading responses !\n')