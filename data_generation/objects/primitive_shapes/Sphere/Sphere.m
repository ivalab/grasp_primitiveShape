% Sphere v1
% Reference object: NCAA baseball
% Diamater = 10cm

close;
clear;
clc;

% size = input("Please input object size (from 1 to 10): ");
% if (size <= 0) || (size > 10)
%     error("Input size is out of range");
% end

for size = 1:10
    
scaleReduceFactor = 90;
    
[x, y, z] = sphere;

x = x / scaleReduceFactor * (size*0.25+2);
y = y / scaleReduceFactor * (size*0.25+2);
z = z / scaleReduceFactor * (size*0.25+2);

% Plot sphere
hold on
axis equal
surf(x,y,z)

formatSpec = '%s_%05d%s';
A = sprintf(formatSpec, "Sphere", size, '.stl');
surf2stl(A, x, y, z);

end