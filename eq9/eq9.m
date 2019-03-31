function du = eq9(t, u)
x_0 = 0;
x_e = 1;
x_steps = 20;
h = (x_e-x_0)/(x_steps-1);

du = zeros(x_steps-2, 1);
du(1) = (exact(t, 0)-2*u(1)+u(2))/(h^2);
du(x_steps-2) = (u(x_steps-3)-2*u(x_steps-2)+exact(t, x_e))/(h^2);

for i = 2:x_steps-3
    du(i) = (u(i-1)-2*u(i)+u(i+1))/(h^2);
end
