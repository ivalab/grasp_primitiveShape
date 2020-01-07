clc;
close all;
clear all;

% position in caerma frame
Matrix_aruco2camera=[[-0.76894616  0.63805079  0.04016215  0.01376286]
[ 0.40205538  0.53146733 -0.74558296  0.08859092]
[-0.49706466 -0.55716574 -0.66520151  0.89069931]
[ 0.          0.          0.          1.        ]];

Matrix_camera2aruco=inv(Matrix_aruco2camera);

pos=Matrix_camera2aruco*[0;0;0;1]+0.01*[35;0;-9.35;0]

Rotation_camera2aruco=Matrix_camera2aruco(1:3,1:3);

Rotation_euler=rad2deg(rotm2eul(Rotation_camera2aruco))

% First set Aruco as the parent of the camera
% Then rotate camera according to the euler angle we achieved just now
% Finally, move the camera according to the translation matrix



