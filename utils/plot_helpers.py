import matplotlib.pyplot as plt
import numpy as np


def compare_results(theor, predicted):
    print('  Вычисленное x(101) = ' + str(predicted))
    print('  Теоретическое x(101) = ' + str(theor))


def plot_lines(*args, **kwargs):
    """
    Рисует графики. Пример (нарисует линии):

    >>> plot_lines(([1, 2], [2, 3], 'name'), ([3, 4, 5], [9, 16, 25], 'name2'))

    :param args: Кортеж из данных
    :param kwargs: Сюда можно передать 'title', и он отобразится в графике
    """
    title = kwargs.get('title')
    x_label, y_label = kwargs.get('x_label'), kwargs.get('y_label')
    for (x_data, *y_data) in args:
        # Если передали title, то его
        has_label = False
        if len(y_data) > 1:
            has_label = True
            label = y_data[1]
            y_data = y_data[0]
        elif len(y_data) == 1:
            y_data = y_data[0]
        if has_label:
            plt.plot(x_data, y_data, label=label)
            plt.legend()
        else:
            plt.plot(x_data, y_data)
    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)

    plt.grid()
    plt.show()


def count_error(x_predicted, theor_function):
    x_predicted = np.array(x_predicted)
    return (x_predicted[0],
            np.abs(x_predicted[1] - theor_function(x_predicted[0])))


def describe_after_execution(t_theor, h_range=[]):
    """
    Декоратор для описания результатов после вычисления

    :param t_theor: Теоретическое уравнение
    :param h_range: Диапазон h. Для задач, где просят сравнить результаты с другим шагом
    """
    def real_decorator(func):
        def func_wrapper(*args, **kwargs):
            t_stop = args[2]                 # Потому что третьим параметром передается конечное время

            print('----------------------------------------------------------')
            print('                   T = {}'.format(
                # Потому что третьим параметром передается конечное время
                t_stop
            ))
            # Если передан диапазон h, то мы подменяем переданный `h=(что-то)` kwarg функции на свой.
            # Это плохое проектирование, но мне нужно уже быстрее спихнуть вычматы
            solutions = []
            plot_data = []
            do_once = True
            if len(h_range) != 0 and kwargs.get('h'):
                for h in h_range:
                    # Подменяем h
                    kwargs['h'] = h


                    # Выполняем
                    solution = func(*args, **kwargs)

                    # Функция обязательно должна возвращать данные в виде [t, x]
                    t_pred, x_pred = solution[0], solution[1]

                    # Получаем теоретические предсказания
                    t_range = np.linspace(min(t_pred), max(t_pred), 1000)
                    # WARNING: тут находится нечисть! Небоходимо, чтобы t_theor был в общем пространстве имен!!!
                    x_range = t_theor(t_range)

                    if do_once:

                        plot_data.append( (t_range, x_range, 'Теоретическое') )

                        do_once = False

                    plot_data.append( (t_pred, x_pred, 'h={}'.format(h)) )
            else:
                h = kwargs.get('h')
                solution = func(*args, **kwargs)
                # Функция обязательно должна возвращать данные в виде [t, x]
                t_pred, x_pred = solution[0], solution[1]

                t_range = np.linspace(min(t_pred), max(t_pred), 1000)
                # WARNING: тут находится нечисть! Небоходимо, чтобы t_theor был в общем пространстве имен!!!
                x_range = t_theor(t_range)

                plot_data.append( (t_range, x_range, 'Теоретическое') )
                plot_data.append( (t_pred, x_pred, 'h={}'.format(h)) )

            plot_lines(*plot_data,
                       title='Теор. и подсчитанное решение', x_label=r't', y_label=r'y')
            error_plot_data = [(*count_error([*data], t_theor),
                                # Здесь data[2] -- подпись к графику. См. коммент про порядок в массиве ниже
                                data[2])
                               # Заметьте, первым в plot_data идет теоретическое решение.
                               # Его невязку рисовать нет смысла.
                               # Да, я ориентируюсь на порядок в массиве. Не бейте за это
                               for data in plot_data[1:]]
            plot_lines(*error_plot_data,
                       title='Невязка в зависимости от t', x_label=r't', y_label=r'Невязка')

            compare_results(t_theor(t_stop), solution[1][-1])
            print('----------------------------------------------------------')
            return solution
        return func_wrapper
    return real_decorator
