% Cuboid1 v1
% Reference object: Salonpas
% Size: 11.9cm * 8.15cm * 1.9cm

close;
clear;
clc;

% size = input("Please input object size (from 1 to 10): ");
% if (size <= 0) || (size > 10)
%     error("Input size is out of range");
% end

for size = 1:5

% Cuboid vertices
ver = [ 0.95 -9.245 -6.045;
        0.95  9.245 -6.045; 
       -0.95  9.245 -6.045;
       -0.95 -9.245 -6.045;
        0.95  9.245  6.045;
        0.95 -9.245  6.045;
       -0.95  9.245  6.045; 
       -0.95 -9.245  6.045];

% Unit: m
ver = ver * (0.4+size*0.2) / 100;
w = abs(ver(1,1));
l = abs(ver(1,2));
h = abs(ver(1,3));

% Cuboid faces
face = [1 2 5 6; 
        5 6 8 7; 
        7 8 4 3;
        3 4 1 2;
        2 3 7 5;
        1 4 8 6];
% specify patch (polygons) in patch() function
face3 = triangulateFaces(face);
% Create cuboid
hold on 
patch('Faces',face,'Vertices',ver,'FaceColor','r'); 
axis equal;
material shiny; % Control reflectance properties of patches
alphamap('rampdown'); % Specify figure transparency
view(30,30); % Camera line of sight
xlabel('x axis'); ylabel('y axis'); zlabel('z axis');


formatSpec = '%s_%05d%s';
A = sprintf(formatSpec, "Cuboid", size, '.stl');
stlwrite(A, face3, ver)

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


for size = 1:5

% Cube vertices
ver = [ 2 -5.5 -3.175;
        2  5.5 -3.175; 
       -2  5.5 -3.175;
       -2 -5.5 -3.175;
        2  5.5  3.175;
        2 -5.5  3.175;
       -2  5.5  3.175; 
       -2 -5.5  3.175];

% Unit: m
ver = ver * (0.4+size*0.2) / 100;
w = abs(ver(1,1));
l = abs(ver(1,2));
h = abs(ver(1,3));

% Cuboid faces
face = [1 2 5 6; 
        5 6 8 7; 
        7 8 4 3;
        3 4 1 2;
        2 3 7 5;
        1 4 8 6];
% specify patch (polygons) in patch() function
face3 = triangulateFaces(face);
% Create cuboid
hold on 
patch('Faces',face,'Vertices',ver,'FaceColor','r'); 
axis equal;
material shiny; % Control reflectance properties of patches
alphamap('rampdown'); % Specify figure transparency
view(30,30); % Camera line of sight
xlabel('x axis'); ylabel('y axis'); zlabel('z axis');


formatSpec = '%s_%05d%s';
A = sprintf(formatSpec, "Cuboid", size+3, '.stl');
stlwrite(A, face3, ver)

end
