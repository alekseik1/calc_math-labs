import numpy as np

class RungeCoeffs:
    A = {
        '2': np.array(
            [
                [(2 + np.sqrt(2)) / 2, 0],
                [-np.sqrt(2), (2 + np.sqrt(2)) / 2]
            ]
        ),
        '3': np.array(
            [
                [(3 + np.sqrt(3)) / 6, 0],
                [(3 - 2 * np.sqrt(3)) / 6, (3 + np.sqrt(3)) / 6]
            ]
        )
    }

    b = {
        '2': np.array([1 / 2, 1 / 2]),
        '3': np.array([1 / 2, 1 / 2])
    }

    c = {
        '2': np.array(
            [(2 + np.sqrt(2)) / 2, (2 - np.sqrt(2)) / 2]
        ),
        '3': np.array(
            [(3 + np.sqrt(3)) / 6, (3 - np.sqrt(3)) / 6]
        )
    }


class RungeImplicit:

    def __init__(self, A, b, c):
        if (A is None) or (b is None) or (c is None):
            raise ValueError('Вы должны передать все `A, b, c` из таблицы Бутчера')
        self.A, self.b, self.c = A, b, c
        self.s = b.shape[0]

    def _count_k(self):
        from scipy.optimize import fsolve
        # Решим неявную систему через fsolve
        # Тут есть фишка: надо для каждого i делать fsolve(), потом
        # потом это сохранять

        def eq_to_solve(k):
            # Представим столбец в виде массива
            k = k.reshape(self.s, self.system_size)
            return np.array(
                [k[i] - self.f(
                    self.t[self.n_step] + self.c[i] * self.h,
                    # Вот тут самая тяжелая часть для понимания
                    # Короче говоря, в Аристовой берется только k[i]-компонента, а в уравнение входит весь k
                    # Поэтому я суммирую руками
                    self.y[self.n_step] + self.h *
                    np.sum(np.dot(self.A, k))
                    #np.sum([self.A[i][j] * k[j] for j in range(self.s)])
                ) for i in range(self.s)]
            ).reshape(-1)   # А потом обратно в столбец. Это костыль над fsolve() !!!

        self.k = fsolve(
            eq_to_solve,
            np.ones([self.s, self.system_size])
        ).reshape(self.s, self.system_size)

    def _step(self):
        # y[n+1] -- предполагается, что y[] имеет нужную длину
        # k[i] -- это вектор из (k_1,..,k_s), i=1,..,m
        self._count_k()
        self.y[self.n_step + 1] = self.y[self.n_step] \
                                  + self.h * np.dot(self.b, self.k)
        self.n_step += 1

    def _init_solver(self):
        # Обнулить все переменные и массивы
        # Текущий шаг
        try:
            self.t_start == 0
        except NameError as e:
            raise RuntimeError('Вы должны вызвать `set_params` перед решением системы')
        self.t = np.arange(self.t_start, self.t_stop, self.h)
        self.n_step = 0
        self.n_stop = self.t.shape[0]
        self.y = np.zeros([self.n_stop, self.system_size], dtype=np.float64)
        # Установим начальное значение
        self.y[0] = self.y_init
        self.k = np.empty([self.s, self.system_size])

    def set_params(self, h, y_init, t_limits, system_size):
        """
        Установить параметры решателя

        :param h: Шаг
        :param y_init: Начальный вектор
        :param t_limits: (t_min, t_max) - кортеж времен интегрирования
        :param system_size: Размер вектора правой части. Да, его нужно задать руками
        :return: Ничего
        """
        self.h, self.y_init, self.system_size = h, y_init, system_size
        self.t_start, self.t_stop = t_limits[0], t_limits[1]

    def solve(self, f):
        """
        Решить систему dy/dt = f(t, y) (может быть векторной)

        :param f: Функция [вектор-функция] вида f(t, y), которая возвращает число [вектор-столбец]
        :return: Массив расмера [N, m], где N - число шагов (высчитывается как (t_max-t_min)/h, а m - размер системы
        """
        # Решаем уравнение dy/dt = f(t, y), где y -- вектор, f -- вектор-функция
        # TODO: сделать проверки на входные данные
        self.f = f
        self._init_solver()
        for i in range(self.n_stop-1):
            self._step()
        return self.y


class MethodBuilder:

    """
    Обертка над методами.
    """

    @staticmethod
    def build(method_name: str):
        available_methods = ['RK2', 'RK3', 'BDF2', 'BDF3', 'BDF4']
        if method_name not in available_methods:
            raise NotImplemented('Этот метод еще не реализован')
        elif method_name.startswith('RK'):
            return RungeImplicit(
                A=RungeCoeffs.A[method_name[-1]],
                b=RungeCoeffs.b[method_name[-1]],
                c=RungeCoeffs.c[method_name[-1]]
            )
        #elif method_name.startswith('BDF'):
        #    return BDF(order=method_name[-1])


if __name__ == '__main__':
    rk2 = MethodBuilder.build('RK3')
    rk2.set_params(h=10**-2, y_init=(1, 1), t_limits=(0, 10**2), system_size=2)
    # Маятник!
    f = lambda t, y: np.array([
        y[1], -y[0]
    ])
    y = rk2.solve(f)

    import matplotlib.pyplot as plt
    plt.plot(rk2.t, rk2.y[:, 0])
    plt.show()
