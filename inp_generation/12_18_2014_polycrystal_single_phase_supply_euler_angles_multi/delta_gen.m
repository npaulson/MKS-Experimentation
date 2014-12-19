function [ pre_angleset ] = delta_gen(el,sn,euL)
% generate delta microstructures

pre_angleset = ones(el^3,1) * round(1+rand()*(euL - 1));
pre_angleset(ceil(0.5*el^3)) = round(1+rand()*(euL - 1));