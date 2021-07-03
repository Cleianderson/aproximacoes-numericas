#!/usr/bin/env python3
import npyscreen
import curses

from metodos import *
from main import ProblemInitialValue
from math import *

class App(npyscreen.StandardApp):
    def onStart(self):
        stdscr = curses.initscr()
        self.rows, self.cols = stdscr.getmaxyx()
        self.addForm('MAIN', MainForm, name='Aproximações Numéricas')


class MainForm(npyscreen.FormBaseNewWithMenus):
    def __init__(self, *args, **kwords):
        super(MainForm, self).__init__(*args, **kwords)
        self.CANCEL_BUTTON_TEXT = 'Calcular'
        self.OK_BUTTON_TEXT = 'Sair'
        self.FIX_MINIMUM_SIZE_WHEN_CREATED = False
        self._cached_values = None

    def create(self):

        self.quit = self.add_menu(name='Ações')
        self.quit.addItem("Exit Application", self.on_exit, "e")
        self.quit.addItem("Calculate", self.btn_press, "c")
        self.quit.addItem("Plot", self.plot, "p")

        self.add(npyscreen.TitleFixedText,
                 value='dy/dt = f(t,y) + g(t,y),  y(t₀)=y₀',
                 name='Forma',
                 editable=False)
        self.fn = self.add(TitleTxt, name='f(t,y)')
        self.g = self.add(TitleTxt, name='g(t,y)')
        self.delta_h = self.add(TitleTxt, name='Δt')
        self.t0 = self.add(TitleTxt, name='t₀')
        self.y0 = self.add(TitleTxt, name='y₀')
        self.point = self.add(TitleTxt, name='Ponto')
        self.interval_start = self.add(TitleTxt, name='a')
        self.interval_end = self.add(TitleTxt, name='b')
        self.parts = self.add(TitleTxt, name='n')
        self.plot_solution = self.add(npyscreen.CheckBox,
                                      value=False,
                                      name='Solução')
        # self.plot_solution. = self.toggle_plot_solution
        self.result = self.add(npyscreen.BoxTitle,
                               name='Aproximações',
                               editable=False)

    # Override method that triggers when you click the 'ok'
    def btn_press(self):
        try:
            fn = lambda t, y: eval(self.fn.value) + eval(self.g.value)
            t0 = float(self.t0.value)
            y0 = float(self.y0.value)
            point = float(self.point.value)
            amp = float(self.delta_h.value)

            self.cache_soluctions(self.fn.value, self.g.value, t0, y0)

            euler = Euler(fn, t0, y0)
            euler_melhor = EulerMelhorado(fn, t0, y0)
            rk = RungeKutta(fn, t0, y0)

            sol_value = '-'
            if self.plot_solution.value:
                if self.problem._cached_lambda == None:
                    self.problem.solve()
                
                sol_value = self.problem._cached_lambda(point)
            self.result.values = [
                f'Solução                          {sol_value}',
                '',
                f'Método de Euler                  {euler.approach_to(point, amp)}',
                f'Método de Euler Melhorado        {euler_melhor.approach_to(point, amp)}',
                f'Método de Runge-Kutta            {rk.approach_to(point, amp)}',
            ]
            self.display()
        except ValueError:
            self.do_nothing()

    # Override method that triggers when you click the 'cancel'
    def on_exit(self, *args):
        self.parentApp.setNextForm(None)
        self.exit_editing()
        # self.display()

    def plot(self):
        # try:
        a = self.interval_start.value or 0
        b = self.interval_end.value or 10
        n = self.parts.value or 8
        amp = float(self.delta_h.value)
        t0, y0 = float(self.t0.value), float(self.y0.value)
        f, g = self.fn.value, self.g.value

        self.cache_soluctions(f, g, t0, y0)

        self.problem.plot(amp, float(a), float(b), int(n), plot_solution=self.plot_solution.value)

    # except ValueError:
    #     self.do_nothing()

    def cache_soluctions(self, f, g, t0, y0):
        if self._cached_values != [f, g, t0, y0]:
            self._cached_values = [f, g, t0, y0]
            self.problem = ProblemInitialValue(f, g, t0, y0)
            if self.plot_solution.value: self.problem.solve()
            pass


class TitleTxt(npyscreen.TitleText):
    TEXT_FIELD_BEGIN_AT = 30

    def __init__(self, *args, **kwords):
        super(TitleTxt, self).__init__(*args, **kwords)
        self.text_field_begin_at = self.TEXT_FIELD_BEGIN_AT
        pass


class OutputText(npyscreen.TitleText):
    def __init__(self, *args, **kwords):
        super(OutputText, self).__init__(*args, **{
            **kwords, 'begin_entry_at': 30
        })
        self.value = '0'
        self.editable = False
        self.labelColor = 'NO_EDIT'
        pass


MyApp = App()
MyApp.run()
