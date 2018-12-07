import matplotlib.pyplot as plt


def compare_results(theor, predicted):
    print('  Вычисленное x(101) = ' + str(predicted))
    print('  Теоретическое x(101) = ' + str(theor))


def plot_lines(*args):
    for (x_data, y_data) in args:
        plt.plot(x_data, y_data)
    plt.grid()
    plt.show()
