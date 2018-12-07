import numpy as np

def euler_explicit(funcs, x_start, t_stop, h=0.1):
    x = x_start
    y = [x_start.copy()]
    while x[0] < t_stop:
        x += h*funcs(x)
        y.append(x.copy())
    return y

def euler_implicit(funcs, x_start, t_stop, h=0.1):
    x = x_start
    y = [x_start.copy()]
    while x[0] < t_stop:
        x_tmp_tmp = x + h*funcs(x)
        x_tmp = x + h*(funcs(x) + funcs(x_tmp_tmp))/2
        x += h*(funcs(x) + funcs(x_tmp))/2
        y.append(x.copy())
    return y

def euler_central_point(funcs, x_start, t_stop, h=0.1):
    x = x_start
    y = [x_start.copy()]
    while x[0] < t_stop:
        x_tmp = (funcs(x + h*funcs(x)) + funcs(x))/2
        x += h*x_tmp
        y.append(x.copy())
    return y

def adams_2(funcs, x_start, t_stop, h=0.001):
    init_method = RungeExplicit(np.array([[0,0,0],[0.5,0.5,0.5],[0,0,1]]))
    y = init_method(funcs, x_start, x_start[0]+h, h)
    x = y[-1]
    y = y[:-1]
    while x[0] < t_stop:
        x += h*((3/2)*funcs(x)-(1/2)*funcs(y[-1]))
        y.append(x.copy())
    return y

def adams_3(funcs, x_start, t_stop, h=0.001):
    init_method = RungeExplicit(np.array([[0,0,0,0], [0.5, 0.5, 0, 0], [1, 0, 1, 0], [0, 1/6, 2/3, 1/6]]))
    y = init_method(funcs, x_start, x_start[0]+2*h, h)
    x = y[-1]
    y = y[:-1]
    while x[0] < t_stop:
        x += h*((23/12)*funcs(x)-(16/12)*funcs(y[-1])+(5/12)*funcs(y[-2]))
        y.append(x.copy())
    return y

def adams_4(funcs, x_start, t_stop, h=0.001):
    init_method = RungeExplicit(np.array([[0,0,0,0,0],[0.5,0.5,0,0,0],[0.5,0,0.5,0,0],[1,0,0,1,0],[0,1/8,3/8,3/8,1/8]]))
    y = init_method(funcs, x_start, x_start[0]+3*h, h)
    x = y[-1]
    y = y[:-1]
    while x[0] < t_stop:
        x += h*((55/24)*funcs(x)-(59/24)*funcs(y[-1])+(37/24)*funcs(y[-2])-(9/24)*funcs(y[-3]))
        y.append(x.copy())
    return y

class RungeExplicit:
    def __init__(self, butcher):
        self.alphas = butcher[:-1, 0]
        self.order = len(self.alphas)
        self.gammas = butcher[-1, 1:]
        self.betas = butcher[:-1, 1:]
    def __call__(self, funcs, x_start, t_stop, h=0.1):
        x = np.array(x_start)
        y = [x_start.copy()]
        while x[0] < t_stop:
            K = []
            for i in range(self.order):
                addition = np.zeros(len(x))
                addition[0] = self.alphas[i]*h
                for j in range(len(K)):
                    addition[1:] += h*K[j]*self.betas[i, j]
                K.append(funcs(x+addition)[1:])
            for i in range(len(K)):
                x += np.array([0] + list(h*K[i]*self.gammas[i]))
            x += np.array([h] + [0]*(len(x)-1))
            y.append(x.copy())
        return y
