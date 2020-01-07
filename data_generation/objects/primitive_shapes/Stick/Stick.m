% Stick v1
% Reference object: hammer and screw-driver
% Hammer: diameter 2.72cm, radius 1.36cm, length 20.43cm
% Screw-driver: diameter 2.41cm, 1.2cm, length 7.87cm
close;
clear;
clc;

% size = input("Please input object size (from 1 to 10): ");
% if (size <= 0) || (size > 10)
%     error("Input size is out of range");
% end

for size = 1:10
    
scaleReduceFactor = 100;

% Rotation angles
alpha = linspace(0, 2*pi, 101);
rin = 0; rout =1.25/scaleReduceFactor;
xin = rin * cos(alpha); xout = rout * cos(alpha);
yin = rin * sin(alpha); yout = rout * sin(alpha);
height = (4 + size*1.5)/scaleReduceFactor;
h1 = -height/2; h2 = height/2;

% Plot bottom, top, outer and inner surfaces
hold on
bottom=surf([xin;xout], [yin;yout], h1 * ones(2, length(xout)));
top=surf([xin;xout], [yin;yout], h2 * ones(2, length(xout)));
[x,y,z] = cylinder(1, length(xin));
outer = surf(rout*x, rout*y, z*(h2-h1) + h1);
inner = surf (rin*x, rin*y, z*(h2-h1) + h1);

X=[rout*x rin*x [xin;xout] [xin;xout]];
Y=[rout*y rin*y [yin;yout] [yin;yout]];
Z=[z*(h2-h1) + h1  z*(h2-h1) + h1 h1 * ones(2, length(xout)) h2 * ones(2, length(xout))];

% View
grid on
axis equal
xlabel('x axis');ylabel('y axis');zlabel('z axis')

formatSpec = '%s_%05d%s';
A = sprintf(formatSpec, "Stick", size, '.stl');
surf2stl(A, X,Y,Z)


end