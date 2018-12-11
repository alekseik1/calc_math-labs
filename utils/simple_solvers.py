import numpy as np


def eiler_1(funcs, x_start, t_stop, h=0.1):
    """
    Явный метод Эйлера, самый простой, с o(h)
    :param funcs: Массив функций
    :param x_start:
    :param t_stop:
    :param h:
    :return:
    """
    # Начальное значение
    x = x_start.copy()
    y = [x_start.copy()]
    while x[0] < t_stop:
        x += h*funcs(x)
        y.append(x.copy())
    return np.array(y).T


def eiler_2(funcs, x_start, t_stop, h=0.1):
    """
    Неявный метод Эйлера с предиктором и корректором
    :param funcs:
    :param x_start:
    :param t_stop:
    :param h:
    :return:
    """
    # Начальное значение
    x = x_start.copy()
    y = [x_start.copy()]
    while x[0] < t_stop:
        # Прогноз
        x_tmp_tmp = x + h*funcs(x)
        # Пересчет
        x_tmp = x + h*(funcs(x) + funcs(x_tmp_tmp))/2
        x += h*(funcs(x) + funcs(x_tmp))/2
        y.append(x.copy())
    return np.array(y).T


def eiler_3(funcs, x_start, t_stop, h=0.1):
    """
    Метод Эйлера с центральной точкой
    :param funcs:
    :param x_start:
    :param t_stop:
    :param h:
    :return:
    """
    # Начальное значение
    x = x_start.copy()
    y = [x_start.copy()]
    while x[0] < t_stop:
        # Нам придется "подгядеть" f_(i+1), а затем взять полусумму с f_i
        x_tmp = (funcs(x + h*funcs(x)) + funcs(x))/2
        # Результат прибавлять в качестве вектора касательной
        x += h*x_tmp
        y.append(x.copy())
    return np.array(y).T


# TODO: придумай, что делать с методом трапеций
def trapezium(funcs, x_start, t_stop, h=0.1):
    """
    Метод трапеций. Пока подгоняет
    :param funcs:
    :param x_start:
    :param t_stop:
    :param h:
    :return:
    """
    return eiler_3(funcs, x_start, t_stop, h)
    # Начальное значение
    x = x_start.copy()
    y = [x_start.copy()]
    while x[0] < t_stop:
        # Нам придется "подгядеть" f_(i+1), а затем взять полусумму с f_i
        x_tmp = x + h*funcs(0, x)
        # Результат прибавлять в качестве вектора касательной
        x += h*x_tmp
        y.append(x.copy())
    return np.array(y).T
