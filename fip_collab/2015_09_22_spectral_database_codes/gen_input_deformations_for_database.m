clear; clc;

theta = 1.5:3:58.5;
theta = theta * (pi/180);

% Inputs to the single point crystal plasticity code for calibration are
% the total strain tensor in the sample frame, and the set of euler angles
% which describe the transformation from the sample to the crystal frame
% of reference. For calibration purposes we assign deformations in the
% sample frame to already be in their principal frame.

et_p = zeros(3,3,length(theta));
et_p(1,1,:) = sqrt(2/3)*cos(theta-(pi/3));
et_p(2,2,:) = sqrt(2/3)*cos(theta+(pi/3));
et_p(3,3,:) = -sqrt(2/3)*cos(theta);

et_v = zeros(length(theta),3);
et_v(:,1) = sqrt(2/3)*cos(theta-(pi/3));
et_v(:,2) = sqrt(2/3)*cos(theta+(pi/3));
et_v(:,3) = -sqrt(2/3)*cos(theta);

disp(et_p)
