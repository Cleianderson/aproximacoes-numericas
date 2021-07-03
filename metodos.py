class Euler:
    def __init__(self, fn, t0, y0):
        self.t0 = t0
        self.y0 = y0
        self.fn = fn
        pass

    def approach_to(self, point, amp) -> float:
        approx = 0
        t, y = self.t0, self.y0

        # y_n+1 = y_n + hf(t_n,y_n)
        for i in range(int(point / amp)):
            approx = self.fn(t, y)
            t = t + amp
            y = y + amp * approx
        return y


class EulerMelhorado(Euler):
    def approach_to(self, point, amp) -> float:
        approx_n = 0
        approx_n1 = 0
        t, y = self.t0, self.y0

        # y_n+1 = y_n + h [f(t,y)+f(t_n1, y_n1)]/2
        for i in range(int(point / amp)):
            approx_n = self.fn(t, y)
            t = t + amp
            approx_n1 = self.fn(t, y + approx_n * amp)
            y = y + amp * (approx_n + approx_n1) / 2
        return y


class RungeKutta(Euler):
    def approach_to(self, point, amp) -> float:
        t, y = self.t0, self.y0

        # y_n+1 = y_n + hf(t_n,y_n)
        for i in range(int(point / amp)):
            k1 = self.fn(t, y)
            k2 = self.fn(t + amp / 2, y + amp * k1 / 2)
            k3 = self.fn(t + amp / 2, y + amp * k2 / 2)
            k4 = self.fn(t + amp, y + amp * k3)
            y = y + amp * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            t = t + amp
        return y


if __name__ == "__main__":
    fn = lambda t, y: 1 - t + 4 * y
    t0 = 0
    y0 = 1
    h = 0.01
    point = 2

    euler = Euler(fn, t0, y0)
    euler_melhor = EulerMelhorado(fn, t0, y0)
    runge_kutta = RungeKutta(fn, t0, y0)

    print(euler.approach_to(point, h))
    print(euler_melhor.approach_to(point, h))
    print(runge_kutta.approach_to(point, h))