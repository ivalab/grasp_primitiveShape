% Ring v1
% Reference objects: tape & mug handle
% Tape: outter diameter 10.19cm, outter radius 5.095cm, inner 
% diameter 8.11cm, inner radius 4.055cm, thickness: 2.5cm
% Handle: outer diameter 7.59cm, outter radius 3.795cm, inner
% diameter 5.59cm, inner radius 2.795cm, thickness: 0.8cm

close;
clear;
clc;

% size = input("Please input object size (from 1 to 10): ");
% if (size <=0 ) || (size > 10)
%     error("Input size is out of range");
% end

for size = 1:10

scaleReduceFactor = 100;

% Parameters
alpha = linspace(0, 2*pi, 101); % Rotation angles
rin = (size*0.35+1.5)/scaleReduceFactor; rout = rin * 1.25;
xin = rin * cos(alpha); xout = rout * cos(alpha);
yin = rin * sin(alpha); yout = rout * sin(alpha);
thickness = rout/2;
h1 = -thickness/2; h2 = thickness/2;

% Plot bottom, top, outer and inner surfaces
hold on
bottom=surf([xin;xout], [yin;yout], h1 * ones(2, length(xout)));
top=surf([xin;xout], [yin;yout], h2 * ones(2, length(xout)));
[x,y,z] = cylinder(1, length(xin));
outer = surf(rout*x, rout*y, z*(h2-h1) + h1);
inner = surf(rin*x, rin*y, z*(h2-h1) + h1);

X=[rout*x rin*x [xin;xout] [xin;xout]];
Y=[rout*y rin*y [yin;yout] [yin;yout]];
Z=[z*(h2-h1) + h1  z*(h2-h1) + h1 h1 * ones(2, length(xout)) h2 * ones(2, length(xout))];

% View
grid on
axis equal
xlabel('x axis');ylabel('y axis');zlabel('z axis')

formatSpec = '%s_%05d%s';
A = sprintf(formatSpec, "Ring", size, '.stl');

surf2stl(A, X,Y,Z)

end
