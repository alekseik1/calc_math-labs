import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# pure function
def make_grid(x_min, x_max, t_min, 
              t_max, h, tau, fictive_x=True):
    if fictive_x:
        x_grid = np.arange(x_min-h/2, x_max+h/2+h/4, h/2)
    else:
        x_grid = np.arange(x_min, x_max+h/4, h/2)
    t_grid = np.arange(t_min, t_max+tau/2, tau)
    # Матрица решений
    T = np.zeros((x_grid.shape[0], t_grid.shape[0]))
    return T, x_grid, t_grid
    
    
# pure function
def calculate_all(kernel, timezero_funcs, xzero_funcs,
                  a, h, tau, 
                  x_min=0, x_max=1, t_min=0, t_max=1):
    """
    Делает подсчеты с заданным ядром метода для всех компонент
    """
    tmp = []
    # Создаем сетку
    T, x_grid, t_grid = make_grid(x_min, x_max, t_min, 
                                   t_max, h, tau, fictive_x=True)
    # Для каждой компоненты
    for i in range(len(timezero_funcs)):
        # Считаем значения
        func_t, func_x, a_curr = timezero_funcs[i], xzero_funcs[i], np.float64(a[i])
        # Начальные условия
        T[:,0] = func_t(x_grid)
        # Граничные условия
        T[-1,:] = func_x(t_grid)
        # Приводим все к double
        T = T.astype('double')
        # Высчитываем sigma
        sigma = np.double(a_curr*tau/h)
        # Вызываем калькулятор
        tmp.append(kernel(T, sigma).T)
    return tmp, x_grid[1:-1], t_grid
    
 
# pure class
class AnimationHelper:
    """
    Класс не общий. Сделан только для избежания повторений кода
    """
    
    def __init__(self, solution, x_grid, t_grid, ylabel, fig=None, axes=None):
        self.solution, self.ylabel = solution, ylabel
        self.x_grid, self.t_grid = x_grid, t_grid
        self.fig, self.axes = fig, axes
        self.ani = None
        
    def _init_anim(self):
        self.line.set_ydata([np.nan] * len(self.x_grid))
        self.initial.set_ydata([np.nan] * len(self.x_grid))
        return self.line, self.initial,
    
    def _animate(self, i):
        self.line.set_ydata(self.solution[:,i*10])  # update the data.
        self.initial.set_ydata(self.solution[:,0])  # update the data.x
        return self.line, self.initial,
        
    def set_ylabel(self, new_ylabel):
        self.ylabel = new_ylabel
        return self
        
    def set_data(self, new_data):
        self.data = data
        return self
        
    def make_animation(self):
        if self.fig is None or self.axes is None:
            self.fig, self.ax = plt.subplots(figsize=(17, 10))
        self.line, = self.ax.plot(self.x_grid, self.solution[:, 0], label='Решение')
        self.initial, = self.ax.plot(self.x_grid, self.solution[:, 0], label='Начальное условие')
        abs_max = max(self.solution.min(), self.solution.max(), key=abs)
        self.ax.set_ylim([-abs_max*1.1, abs_max*1.1])
        self.ax.title.set_text('Численное решение ${}(t, x)$'.format(self.ylabel))
        self.ax.set_xlabel("x")
        self.ax.set_ylabel('${}(t, x)$'.format(self.ylabel))
        self.ax.legend()
        self.ax.grid()
        
        self.ani = animation.FuncAnimation(
            self.fig, self._animate, init_func=self._init_anim, 
            interval=30, blit=True, save_count=(self.solution.shape[1]-1)/10)
        return self
        
    def save_as_file(self, filepath):
        if self.ani is None:
            raise ValueError('Nothing to save, call `make_animation` before saving!')
        self.ani.save(filepath, writer='ffmpeg')