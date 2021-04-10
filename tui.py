#!/usr/bin/env python3
import npyscreen
import curses

from metodos import *
from main import ProblemInitialValue


class App(npyscreen.StandardApp):
    def onStart(self):
        stdscr = curses.initscr()
        self.rows, self.cols = stdscr.getmaxyx()
        self.addForm('MAIN', MainForm, name='Aproximações Numéricas')

    
    def onInMainLoop(self):
        self.rows, self.cols = stdscr.getmaxyx()
        self.getForm('Main').cols = self.cols


class MainForm(npyscreen.FormBaseNewWithMenus):
    def __init__(self, *args, **kwords):
        super(MainForm, self).__init__(*args, **kwords)
        self.CANCEL_BUTTON_TEXT = 'Calcular'
        self.OK_BUTTON_TEXT = 'Sair'
        self.FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def create(self):

        self.quit = self.add_menu(name='Ações')
        self.quit.addItem("Exit Application", self.on_exit, "e")
        self.quit.addItem("Calculate", self.btn_press, "c")
        self.quit.addItem("Plot", self.plot, "p")

        self.fn = self.add(TitleTxt, name='f(t,y)')
        self.g = self.add(TitleTxt, name='g(t,y)')
        self.delta_h = self.add(TitleTxt, name='Delta t')
        self.t0 = self.add(TitleTxt, name='t0')
        self.y0 = self.add(TitleTxt, name='y0')
        self.point = self.add(TitleTxt, name='Ponto')
        self.result = self.add(npyscreen.BoxTitle,
                               name='Aproximações',
                               editable=False)

    # Override method that triggers when you click the 'ok'
    def btn_press(self):
        try:
            fn = lambda t, y: eval(self.fn.value)
            t0 = float(self.t0.value)
            y0 = float(self.y0.value)
            point = float(self.point.value)
            amp = float(self.delta_h.value)

            euler = Euler(fn, t0, y0)
            euler_melhor = EulerMelhorado(fn, t0, y0)
            rk = RungeKutta(fn, t0, y0)

            self.result.values = [
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
        try:
            amp = float(self.delta_h.value)
            t0, y0 = float(self.t0.value), float(self.y0.value)
            f, g = self.fn.value, self.g.value
            problem = ProblemInitialValue(f, g, t0, y0)
            problem.solve()
            problem.plot(amp)
        except ValueError:
            self.do_nothing()


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
