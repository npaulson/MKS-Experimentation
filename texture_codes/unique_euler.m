clear plot

phi1  = 0 : .01 : 2*pi();
ii_max = 200;

figure(1)

xlabel('\phi1')
ylabel('magnitude')


for ii = 1 : ii_max + 1
   Phi = ((ii - 1)/ii_max) * 2 * pi();
   y = -cos(phi1) * sin(Phi);
   pause(0.05)
   plot(phi1,y)
   axis([0 2*pi() -1 1])
%    hold on
end


% hold off