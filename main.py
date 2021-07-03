import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from types import FunctionType

from matplotlib.patches import Patch
from math import *
from metodos import *

sen = sin


class ProblemInitialValue:
    def __init__(self, fn, g, t0, y0):
        self.fn = fn
        self.g = g
        self.t0 = t0
        self.y0 = y0
        self._cached_lambda = None

        self._fn = lambda t, y: eval(self.fn) + eval(self.g)
        self.euler = Euler(self._fn, self.t0, self.y0)
        self.euler_melhor = EulerMelhorado(self._fn, self.t0, self.y0)
        self.runge_kutta = RungeKutta(self._fn, self.t0, self.y0)

    def solve(self):
        if self._cached_lambda != None:
            return [self._cached_lambda, self._cached_sol]
            pass
        t = sp.symbols('t')
        y = sp.Function('y')(t)
        f = sp.parse_expr(self.fn, {'t': t, 'y': y})
        _g = sp.parse_expr(self.g, {'t': t, 'y': y})
        dydt = y.diff(t)
        eq = sp.Eq(dydt - f, _g)
        dsol = sp.dsolve(eq, y)
        condicion = dsol.subs(t, self.t0).replace(y.subs(t, self.t0), self.y0)
        c = sp.solve(condicion)
        C1 = sp.Symbol('C1')
        sol = sp.simplify(dsol.replace(C1, c[0]))
        y_t = sp.lambdify(t, sol.args[1])
        self.sol_lambda = y_t
        self._cached_lambda = y_t
        self._cached_sol = sol
        return y_t, sol

    def plot(self, amp, a=0, b=10, n=8, plot_solution=True):
        fig, ax = plt.subplots()

        X = np.linspace(a, b, n)

        y_euler = [self.euler.approach_to(x, amp) for x in X]
        y_euler_melhor = [self.euler_melhor.approach_to(x, amp) for x in X]
        y_runge_kutta = [self.runge_kutta.approach_to(x, amp) for x in X]

        handles=[]
        if plot_solution:
            if self._cached_lambda == None:
                self.solve()
            ax.plot(X, self._cached_lambda(X), '-o', color='green')
            sol_patch = Patch(color='green', label='Solução')
            handles.append(sol_patch)

        ax.plot(X, y_euler, '-o', color='red')
        ax.plot(X, y_euler_melhor, '-o', color='purple')
        ax.plot(X, y_runge_kutta, '-o', color='blue')

        e_patch = Patch(color='red', label='Método de Euler')
        handles.append(e_patch)
        e_m_patch = Patch(color='purple', label='Método de Euler Melhorado')
        handles.append(e_m_patch)
        rk_patch = Patch(color='blue', label='Método de Runge-Kutta')
        handles.append(rk_patch)
        plt.legend(handles=handles)

        plt.show()

    def plot_table(self, method='e', t_values=[], h_values=[]):
        self.solve()

        fig, ax = plt.subplots()

        ax.patch.set_visible(False)
        plt.axis('off')

        if len(t_values) == 0: t_values = list(np.linspace(0, 2, 4))

        data = [t_values]
        cols = ['t']
        for i, h in enumerate(h_values):
            data.append([])
            for t in t_values:
                if method == 'em':
                    data[i + 1].append(self.euler_melhor.approach_to(t, h))
                elif method == 'rk':
                    data[i + 1].append(self.runge_kutta.approach_to(t, h))
                else:
                    data[i + 1].append(self.euler.approach_to(t, h))

            cols.append(f'h={h}')

        cols.append('Solução')
        data.append([self.sol_lambda(t) for t in t_values])

        ax.table(cellText=data, rowLabels=cols, loc='center', rowLoc='center')

        # X = np.linspace(a, b, n)

        # y_euler = [self.euler.approach_to(x, amp) for x in X]
        # y_euler_melhor = [self.euler_melhor.approach_to(x, amp) for x in X]
        # y_runge_kutta = [self.runge_kutta.approach_to(x, amp) for x in X]

        # p1 = ax.plot(t_values, data[1], '-o')
        # plt.subplots_adjust(left=0.2)
        # plt.xticks([])
        # ax.plot(X, y_euler, '-o', color='red')
        # ax.plot(X, y_euler_melhor, '-o', color='purple')
        # ax.plot(X, y_runge_kutta, '-o', color='blue')

        # sol_patch = Patch(color='green', label='Solução')
        # e_patch = Patch(color='red', label='Método de Euler')
        # e_m_patch = Patch(color='purple', label='Método de Euler Melhorado')
        # rk_patch = Patch(color='blue', label='Método de Runge-Kutta')
        # plt.legend(handles=[sol_patch, e_patch, e_m_patch, rk_patch])

        plt.show()


def main():
    fn = '1-t+4*y'
    g = '0'
    t0 = float(0)
    y0 = float(2)
    # fn = input('f(t,y) = ')
    # g = input('g(t,y) = ')
    # t0 = float(input('t0 = '))
    # y0 = float(input('y0 = '))
    # h = float(input('passo: '))

    problem = ProblemInitialValue(fn, g, t0, y0)
    t_values = np.linspace(1,2, 5)
    problem.solve()
    problem.plot(0.01)

    # print(f'{y}     {_}')
    # fig, ax = plt.subplots()

    # _fn = lambda t, y: eval(fn) + eval(g)

    # euler = Euler(_fn, t0, y0)
    # euler_melhor = EulerMelhorado(_fn, t0, y0)
    # self.runge_kutta = RungeKutta(_fn, t0, y0)

    # X = np.linspace(0, 10, 8)

    # y_euler = [euler.approach_to(x, h) for x in X]
    # y_euler_melhor = [euler_melhor.approach_to(x, h) for x in X]
    # y_runge_kutta = [runge_kutta.approach_to(x, h) for x in X]

    # ax.plot(X, y(X), '-o', color='green')
    # ax.plot(X, y_euler, '-o', color='red')
    # ax.plot(X, y_euler_melhor, '-o', color='purple')
    # ax.plot(X, y_runge_kutta, '-o', color='blue')

    # sol_patch = Patch(color='green', label='Solução')
    # e_patch = Patch(color='red', label='Método de Euler')
    # e_m_patch = Patch(color='purple', label='Método de Euler Melhorado')
    # rk_patch = Patch(color='blue', label='Método de Runge-Kutta')
    # plt.legend(handles=[sol_patch, e_patch, e_m_patch, rk_patch])

    # plt.show()


if __name__ == '__main__':
    main()
