import os
import matplotlib.pyplot as plt
import numpy as np
import Activator as act


class Plotter:
    col_red = '#D56489'
    col_yellow = '#ECE6A6'
    col_blue = '#009D9D'
    col_green = '#41BA90'
    def create_plot(self, path_result, act_object):
        fig = plt.figure()
        ax = fig.add_subplot()

        for _c in act_object.curves:
            if self.whole_num(_c.d):
                data_size = 40
                ax.text(_c.T[0] - 0.05, _c.SNR[0], f'{int(_c.d)}mm')
                _alpha = 0.9
                linew = 3
            else:
                data_size = 15
                _alpha = 0.2
                linew = 1

            plt.scatter(_c.T, _c.SNR, label=f'{_c.d}mm', marker='o', alpha=_alpha, c=col_red, s=data_size)
            a, b, c = np.polyfit(_c.T, _c.SNR, deg=2)
            x = np.linspace(_c.T[0], _c.T[-1], 141)
            y = self.func_poly(x, a, b, c)
            plt.plot(x, y, c=self.col_red, alpha=_alpha, linewidth=linew)

        ax.text(0, 0, '$kV_opt = {}$'.format(act_object.kV_opt))
        plt.scatter( act_object.X_opt, act_object.Y_opt, marker='x', c='black', s=70)
        plt.title(f'$SRN(T)$ with $U_{0} = {act_object.U0}$kV       FIT: $f(x) = a x^{2} + bx + c$')
        plt.xlabel('Transmission a.u.')
        plt.ylabel('SNR/s')
        plt.xlim(act_object.curves[-1].T[0] - 0.05, act_object.curves[0].T[-1] + 0.02)
        plt.plot(act_object.c_U0_x, act_object.c_U0_y, c=col_green, linestyle='-', linewidth=2)
        plt.axvline(x=act_object.min_T, c=col_green, linestyle='--', linewidth=1)
        plt.scatter(act_object.intercept_x, act_object.intercept_y, c=col_red, marker='x', s=50)
        plt.show()
        fig.savefig(os.path.join(path_result, f'MAP_kVopt{act_object.kV_opt}.pdf'), dpi=600)


    @staticmethod
    def func_poly(x, a, b, c):
        return a * x ** 2 + b * x + c

    @staticmethod
    def whole_num(num):
        if num - int(num) == 0:
            return True
        else:
            return False