import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
from rowEquation import RowEquation


class InteractiveRowEquationPlot:
    def __init__(self):
        self.eq = RowEquation()
        self.degree = 4
        self.points = []

        # Inicializar polinomio y solución
        self.eq.set_rower_cinematic([1])
        self.eq.solve_edo()

        # Figura con 3x2 subplots
        self.fig, self.axs = plt.subplots(3, 2, figsize=(13, 8))
        plt.subplots_adjust(right=0.78, hspace=0.4)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self._add_controls()
        self.draw_plots()
        plt.show()

    # ------------------------------------------------------------------
    # Panel lateral (sliders, cajas de texto y botones)
    # ------------------------------------------------------------------
    def _add_controls(self):
        slider_ax = 0.8
        height = 0.04
        spacing = 0.06

        # Grado del polinomio
        self.slider_deg = Slider(plt.axes([slider_ax, 0.85, 0.15, height]),
                                 'Grado', 4, 10, valinit=self.degree, valstep=1)
        self.slider_deg.on_changed(self.change_degree)

        # Parámetros modificables
        params = ['M', 'm', 'L', 'T', 'rho', 'S', 'Cd']
        self.textboxes = {}
        for i, p in enumerate(params):
            ax_box = plt.axes([slider_ax, 0.75 - i * spacing, 0.15, height])
            box = TextBox(ax_box, f'{p}: ', initial=str(getattr(self.eq, p)))
            box.on_submit(self.update_param)
            self.textboxes[p] = box

        # Botones
        self.ax_reset = plt.axes([slider_ax, 0.22, 0.15, 0.05])
        self.button_reset = Button(self.ax_reset, 'Reset puntos')
        self.button_reset.on_clicked(self.reset_points)

        self.ax_fit = plt.axes([slider_ax, 0.14, 0.15, 0.05])
        self.button_fit = Button(self.ax_fit, 'Ajustar')
        self.button_fit.on_clicked(self.fit_polynomial)

    # ------------------------------------------------------------------
    # Gráficas
    # ------------------------------------------------------------------
    def draw_plots(self):
        for i in range(3):
            for j in range(2):
                self.axs[i, j].clear()

        s = self.eq.solution
        if s is None:
            return

        # --- x(t)
        self.axs[0, 0].plot(s['tt'], s['xx'], color='blue')
        self.axs[0, 0].set_title('x(t) — Posición')

        self.axs[1, 0].plot(s['tt'], s['xx_dot'], color='red')
        self.axs[1, 0].set_title("x'(t) — Velocidad")

        self.axs[2, 0].plot(s['tt'], s['xx_ddot'], color='green')
        self.axs[2, 0].set_title("x''(t) — Aceleración")

        if self.points:
            px, py = zip(*self.points)
            self.axs[2, 0].scatter(px, py, color='black', label='Puntos')
            self.axs[2, 0].legend()

        # --- y(t)
        self.axs[0, 1].plot(s['tt'], s['yy'], color='blue')
        self.axs[0, 1].set_title('y(t) — Posición dinámica')

        self.axs[1, 1].plot(s['tt'], s['yy_dot'], color='red')
        self.axs[1, 1].set_title("y'(t) — Velocidad dinámica")

        self.axs[2, 1].plot(s['tt'], s['yy_ddot'], color='green')
        self.axs[2, 1].set_title("y''(t) — Aceleración dinámica")

        for i in range(3):
            for j in range(2):
                self.axs[i, j].grid(True)
                self.axs[i, j].set_xlim(0, self.eq.T)

        self.fig.canvas.draw_idle()

    # ------------------------------------------------------------------
    # Eventos interactivos
    # ------------------------------------------------------------------
    def onclick(self, event):
        if event.inaxes == self.axs[2, 0]:
            self.points.append((event.xdata, event.ydata))
            self.draw_plots()

    def reset_points(self, event):
        self.points = []
        self.draw_plots()

    def change_degree(self, val):
        self.degree = int(val)
        high_coeffs = [0] * (self.degree - 3)
        high_coeffs[-1] = 1
        self.eq.set_rower_cinematic(high_coeffs)
        self.eq.solve_edo()
        self.draw_plots()

    def update_param(self, text):
        """Actualiza parámetros físicos de RowEquation."""
        for name, box in self.textboxes.items():
            try:
                val = float(box.text)
                setattr(self.eq, name, val)
            except ValueError:
                print(f"Valor no válido para {name}: {box.text}")

        # Recalcular dependencias internas
        self.eq.mu = 1 / (self.eq.M + self.eq.m)
        self.eq.B = self.eq.m * self.eq.mu
        self.eq.A = -0.5 * self.eq.S * self.eq.rho * self.eq.Cd * self.eq.mu

        # Resolver de nuevo la EDO
        self.eq.solve_edo()
        self.draw_plots()

    def fit_polynomial(self, event):
        if not self.points:
            print("No hay puntos seleccionados para ajustar.")
            return

        t_points, a_target = zip(*self.points)
        t_points = np.array(t_points)
        a_target = np.array(a_target)
        n_free = self.degree - 3

        def residuals(a_free):
            self.eq.set_rower_cinematic(a_free)
            a_pred = self.eq.x_ddot(t_points)
            return np.sum((a_pred - a_target) ** 2)

        best_a = None
        best_err = np.inf
        for test in np.random.uniform(-2, 2, size=(200, n_free)):
            err = residuals(test)
            if err < best_err:
                best_err = err
                best_a = test
        self.eq.set_rower_cinematic(best_a)
        self.eq.solve_edo()
        print(f"Ajuste terminado. Error cuadrático: {best_err:.3e}")
        self.draw_plots()


if __name__ == "__main__":
    InteractiveRowEquationPlot()
