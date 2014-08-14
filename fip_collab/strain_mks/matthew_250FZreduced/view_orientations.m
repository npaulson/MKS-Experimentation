load euler_250cal.mat

st = 1;
en = 500;
sn = 1;

close all

figure(1)
scatter3(euler(st:en,sn,1),euler(st:en,sn,2),euler(st:en,sn,3),'kx')
axis equal

figure(2)
scatter(euler(st:en,sn,1),euler(st:en,sn,2),'kx')
axis equal
