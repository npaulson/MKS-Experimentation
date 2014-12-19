%This script creates a set of 3, 3x3 matricies that make up all of the
%symmetry operations active on the 222 space group. To call a matrix '#',
%type 'sym(:,:,#)'

for ind = 1:4
    symorth(:,:,ind)=zeros(3);
end

%1
symorth(1,1,1)=1;
symorth(2,2,1)=1;
symorth(3,3,1)=1;
%2
symorth(1,1,2)=1;
symorth(2,2,2)=-1;
symorth(3,3,2)=-1;
%3
symorth(1,1,3)=-1;
symorth(2,2,3)=1;
symorth(3,3,3)=-1;
%4
symorth(1,1,4)=-1;
symorth(2,2,4)=-1;
symorth(3,3,4)=1;
