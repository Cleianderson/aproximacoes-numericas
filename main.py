import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from types import FunctionType

from matplotlib.patches import Patch
from math import *
from metodos import *

sen = sin


class ProblemInitialValue:
    fn: str
    g: str
    t0: float
    y0: float
    sol_lambda: FunctionType

    def __init__(self, fn, g, t0, y0):
        self.fn = fn
        self.g = g
        self.t0 = t0
        self.y0 = y0

    def solve(self):
        t = sp.symbols('t')
        y = sp.Function('y')(t)
        f = sp.parse_expr(self.fn, {'t': t, 'y': y})
        _g = sp.parse_expr(self.g, {'t': t, 'y': y})
        dydt = y.diff(t)
        eq = sp.Eq(dydt - f, _g)
        dsol = sp.dsolve(eq)
        condicion = dsol.subs(t, self.t0).replace(y.subs(t, self.t0), self.y0)
        c = sp.solve(condicion)
        C1 = sp.Symbol('C1')
        sol = sp.simplify(dsol.replace(C1, c[0]))
        y_t = sp.lambdify(t, sol.args[1])
        self.sol_lambda = y_t
        return y_t, sol

    def plot(self, amp, a=0, b=10, n=8):
        fig, ax = plt.subplots()

        _fn = lambda t, y: eval(self.fn) + eval(self.g)

        euler = Euler(_fn, self.t0, self.y0)
        euler_melhor = EulerMelhorado(_fn, self.t0, self.y0)
        runge_kutta = RungeKutta(_fn, self.t0, self.y0)

        X = np.linspace(a, b, n)

        y_euler = [euler.approach_to(x, amp) for x in X]
        y_euler_melhor = [euler_melhor.approach_to(x, amp) for x in X]
        y_runge_kutta = [runge_kutta.approach_to(x, amp) for x in X]

        ax.plot(X, self.sol_lambda(X), '-o', color='green')
        ax.plot(X, y_euler, '-o', color='red')
        ax.plot(X, y_euler_melhor, '-o', color='purple')
        ax.plot(X, y_runge_kutta, '-o', color='blue')

        sol_patch = Patch(color='green', label='Solução')
        e_patch = Patch(color='red', label='Método de Euler')
        e_m_patch = Patch(color='purple', label='Método de Euler Melhorado')
        rk_patch = Patch(color='blue', label='Método de Runge-Kutta')
        plt.legend(handles=[sol_patch, e_patch, e_m_patch, rk_patch])

        plt.show()


def main():
    fn = input('f(t,y) = ')
    g = input('g(t,y) = ')
    t0 = float(input('t0 = '))
    y0 = float(input('y0 = '))
    h = float(input('passo: '))

    problem = ProblemInitialValue(fn)
    y, _ = problem.solve(t0, y0, g)

    fig, ax = plt.subplots()

    _fn = lambda t, y: eval(fn) + eval(g)

    euler = Euler(_fn, t0, y0)
    euler_melhor = EulerMelhorado(_fn, t0, y0)
    runge_kutta = RungeKutta(_fn, t0, y0)

    X = np.linspace(0, 10, 8)

    y_euler = [euler.approach_to(x, h) for x in X]
    y_euler_melhor = [euler_melhor.approach_to(x, h) for x in X]
    y_runge_kutta = [runge_kutta.approach_to(x, h) for x in X]

    ax.plot(X, y(X), '-o', color='green')
    ax.plot(X, y_euler, '-o', color='red')
    ax.plot(X, y_euler_melhor, '-o', color='purple')
    ax.plot(X, y_runge_kutta, '-o', color='blue')

    sol_patch = Patch(color='green', label='Solução')
    e_patch = Patch(color='red', label='Método de Euler')
    e_m_patch = Patch(color='purple', label='Método de Euler Melhorado')
    rk_patch = Patch(color='blue', label='Método de Runge-Kutta')
    plt.legend(handles=[sol_patch, e_patch, e_m_patch, rk_patch])

    plt.show()


if __name__ == '__main__':
    main()
