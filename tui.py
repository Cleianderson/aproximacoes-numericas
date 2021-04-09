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


class MainForm(npyscreen.FormBaseNew):
    def __init__(self, *args, **kwords):
        super(MainForm, self).__init__(*args, **kwords)
        self.CANCEL_BUTTON_TEXT = 'Calcular'
        self.OK_BUTTON_TEXT = 'Sair'

    def create(self):
        x, y = self.useable_space()

        self.on_cancel = self.btn_press

        self.fn = self.add(TitleTxt, name='Função f(t,y)')
        self.delta_h = self.add(TitleTxt, name='Delta t')
        self.t0 = self.add(TitleTxt, name='t0')
        self.y0 = self.add(TitleTxt, name='y0')
        self.point = self.add(TitleTxt, name='Ponto')
        self.output1 = self.add(OutputText,
                                name='Método de Euler',
                                rely=y - (y + 6))
        self.output2 = self.add(OutputText,
                                name='Método de Euler Melhorado',
                                rely=y - (y + 5))
        self.output3 = self.add(OutputText,
                                name='Runge-Kutta',
                                rely=y - (y + 4))
        self.btn_cancel = self.add(npyscreen.MiniButtonPress, relx=-x, rely=-self.parentApp.cols-10)


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
    def on_ok(self):
        self.parentApp.setNextForm(None)


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
