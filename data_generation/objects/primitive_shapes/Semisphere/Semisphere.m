% Bowl
% No reference

close;
clear;
clc;

% size = input("Please input object size (from 1 to 10): ");
% if (size <= 0) || (size > 10)
%     error("Input size is out of range");
% end

for size = 1:10

scaleReduceFactor = 90; 

rout = 1 / scaleReduceFactor * (size*0.5 + 3);
rin = 0.9 * 1 / scaleReduceFactor * (size*0.5 + 3);
alpha = linspace(0, 2*pi, 21);
xin_top = rin * cos(alpha); xout_top = rout * cos(alpha);
yin_top = rin * sin(alpha); yout_top = rout * sin(alpha);

[x, y, z] = sphere(20);
z(z>0) = nan;

xout = x *rout;
yout = y *rout;
zout = z *rout;


xin = x *rin;
yin = y *rin;
zin = z *rin;



hold on
axis equal

surf([xin_top;xout_top], [yin_top;yout_top], 0 .* ones(2, length(xout_top)));
surf(xout,yout,zout);
surf(xin,yin,zin);
daspect([1 1 1]);
hold on;

X=[xout ; xin ; [xin_top;xout_top] ];
Y=[yout ;yin ;[yin_top;yout_top] ];
Z=[zout ;zin ;0* ones(2, length(xout_top))];



formatSpec = '%s_%05d%s';
A = sprintf(formatSpec, "Semisphere", size, '.stl');
surf2stl(A, X, Y, Z);

end