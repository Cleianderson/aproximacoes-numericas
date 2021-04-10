#!/usr/bin/env python3
import npyscreen
import curses
from metodos import *


class App(npyscreen.StandardApp):
    def onStart(self):
        stdscr = curses.initscr()
        self.rows, self.cols = stdscr.getmaxyx()
        self.addForm('MAIN',
                     MainForm,
                     name='Aproximações Numéricas',
                     minimum_columns=self.cols,
                     minimum_lines=self.rows)


class MainForm(npyscreen.ActionFormV2WithMenus):
    def __init__(self, *args, **kwords):
        super(MainForm, self).__init__(*args, **kwords)
        self.CANCEL_BUTTON_TEXT = 'Calcular'
        self.OK_BUTTON_TEXT = 'Sair'

    def create(self):
        y, x = self.curses_pad.getmaxyx()

        self.fn = self.add(TitleTxt, name='Função f(t,y)')
        self.delta_h = self.add(TitleTxt, name='Delta t')
        self.t0 = self.add(TitleTxt, name='t0')
        self.y0 = self.add(TitleTxt, name='y0')
        self.point = self.add(TitleTxt, name='Ponto')
        self.output1 = self.add(OutputText, name='Método de Euler')
        self.output2 = self.add(OutputText, name='Método de Euler Melhorado')
        self.output3 = self.add(OutputText, name='Runge-Kutta')

        self.btn_ok = self.add(npyscreen.MiniButtonPress,
                               name='calcular',
                               rely=-4)
        self.btn_cancel = self.add(npyscreen.MiniButtonPress,
                                   name='sair',
                                   rely=-4,
                                   relx=15)
        self.btn_cancel.when_pressed_function = self.on_exit
        self.btn_ok.when_pressed_function = self.btn_press

    # Override method that triggers when you click the 'ok'
    def btn_press(self):
        fn = lambda t, y: eval(self.fn.value)
        t0 = float(self.t0.value)
        y0 = float(self.y0.value)
        point = float(self.point.value)
        amp = float(self.delta_h.value)

        euler = Euler(fn, t0, y0)
        euler_melhor = EulerMelhorado(fn, t0, y0)
        rk = RungeKutta(fn, t0, y0)

        self.output1.value = euler.approach_to(point, amp)
        self.output2.value = euler_melhor.approach_to(point, amp)
        self.output3.value = rk.approach_to(point, amp)
        self.display()

    # Override method that triggers when you click the 'cancel'
    def on_exit(self):
        self.parentApp.setNextForm(None)
        self.exit_editing()
        # self.display()


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
