import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from math import *
from metodos import *

sen = sin

class ProblemInitialValue:
    fn: str

    def __init__(self, fn):
        self.fn = fn

    def solve(self, t0, y0):
        t = sp.symbols('t')
        y = sp.Function('y')(t)
        f = sp.parse_expr(self.fn, {'t': t, 'y': y})
        dydt = y.diff(t)
        eq = sp.Eq(dydt - f, 0)
        _class = sp.classify_ode(eq)
        dsol = sp.dsolve(eq, hint=_class[1])
        condicion = dsol.subs(t, t0).replace(y.subs(t, t0), y0)
        c = sp.solve(condicion)
        C1 = sp.Symbol('C1')
        sol = sp.simplify(dsol.replace(C1, c[0]))
        y_t = sp.lambdify(t, sol.args[1])
        return y_t, sol


def main():
    fn = input('f(t,y) = ')
    t0 = float(input('t0 = '))
    y0 = float(input('y0 = '))
    h = float(input('passo: '))

    problem = ProblemInitialValue(fn)
    y, _ = problem.solve(t0, y0)

    fig, ax = plt.subplots()

    _fn = lambda t, y: eval(fn)

    euler = Euler(_fn, t0, y0)
    euler_melhor = EulerMelhorado(_fn, t0, y0)
    runge_kutta = RungeKutta(_fn, t0, y0)

    X = np.linspace(0, 10)

    y_euler = [euler.approach_to(x, h) for x in X]
    y_euler_melhor = [euler_melhor.approach_to(x, h) for x in X]
    y_runge_kutta = [runge_kutta.approach_to(x, h) for x in X]

    ax.plot(X, y(X), color='green')
    ax.plot(X, y_euler, color='red')
    ax.plot(X, y_euler_melhor, color='purple')
    ax.plot(X, y_runge_kutta, color='blue')

    sol_patch = Patch(color='green', label='Solução')
    e_patch = Patch(color='red', label='Método de Euler')
    e_m_patch = Patch(color='purple', label='Método de Euler Melhorado')
    rk_patch = Patch(color='blue', label='Método de Runge-Kutta')
    plt.legend(handles=[sol_patch, e_patch, e_m_patch, rk_patch])

    plt.show()


if __name__ == '__main__':
    main()
