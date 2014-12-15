clf

bins = 7;
n=20000;
phi1= rand(1,n);

Phi=sort( acos(rand(1,n)) );
% Phi=sort( acos(2*rand(1,n)-1) );

binlev = [Phi(1:round(n/bins):n),Phi(end)]

figure(1)

scatter(phi1,Phi,'.');

hold on

lines = repmat([0,pi/2],[bins+1,1]);
for ii = 1:length(binlev)
    plot([0,pi/2],[binlev(ii),binlev(ii)],'r-')
end

% hold off

axis([0 1 0 pi/2]);	
title('Random Orientation Distribution');
xlabel('\g_{\Phi}');	
ylabel('\Phi');


% figure(2)
vrange = 0: 1/bins :1;
length(vrange)
lvlrange = acos(vrange);
plot(vrange,lvlrange,'g-')
scatter(vrange,lvlrange,'go')

hold off
