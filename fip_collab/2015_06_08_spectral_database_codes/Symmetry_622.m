symhex = zeros(3,3,12);

a = sqrt(3)/2;

%1
symhex(1,1,1)=1;
symhex(2,2,1)=1;
symhex(3,3,1)=1;
%2
symhex(1,1,2)=-.5;
symhex(2,2,2)=-.5;
symhex(3,3,2)=1;
symhex(1,2,2)=a;
symhex(2,1,2)=-a;
%3
symhex(1,1,3)=-.5;
symhex(2,2,3)=-.5;
symhex(3,3,3)=1;
symhex(1,2,3)=-a;
symhex(2,1,3)=a;
%4
symhex(1,1,4)=.5;
symhex(2,2,4)=.5;
symhex(3,3,4)=1;
symhex(1,2,4)=a;
symhex(2,1,4)=-a;
%5
symhex(1,1,5)=-1;
symhex(2,2,5)=-1;
symhex(3,3,5)=1;
%6
symhex(1,1,6)=.5;
symhex(2,2,6)=.5;
symhex(3,3,6)=1;
symhex(1,2,6)=-a;
symhex(2,1,6)=a;
%7
symhex(1,1,7)=-.5;
symhex(2,2,7)=.5;
symhex(3,3,7)=-1;
symhex(1,2,7)=-a;
symhex(2,1,7)=-a;
%8
symhex(1,1,8)=1;
symhex(2,2,8)=-1;
symhex(3,3,8)=-1;
%9
symhex(1,1,9)=-.5;
symhex(2,2,9)=.5;
symhex(3,3,9)=-1;
symhex(1,2,9)=a;
symhex(2,1,9)=a;
%10
symhex(1,1,10)=.5;
symhex(2,2,10)=-.5;
symhex(3,3,10)=-1;
symhex(1,2,10)=a;
symhex(2,1,10)=a;
%11
symhex(1,1,11)=-1;
symhex(2,2,11)=1;
symhex(3,3,11)=-1;
%12
symhex(1,1,12)=.5;
symhex(2,2,12)=-.5;
symhex(3,3,12)=-1;
symhex(1,2,12)=-a;
symhex(2,1,12)=-a;

save symhex.mat symhex