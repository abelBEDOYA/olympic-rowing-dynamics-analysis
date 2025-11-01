import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
from rowEquation import RowEquation
import matplotlib.image as mpimg


class InteractiveRowEquationPlot:
    def __init__(self):
        self.eq = RowEquation()
        self.degree = 4
        self.points = []

        # Inicializar polinomio y solución
        self.eq.set_rower_cinematic([1])
        self.eq.solve_edo()

        # Figura con 3x2 subplots
        self.fig, self.axs = plt.subplots(4, 2, figsize=(15, 12))
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
        self.slider_deg = Slider(plt.axes([slider_ax+0.02, 0.85, 0.15, height]),
                                'Grado', 4, 10, valinit=self.degree, valstep=1)
        self.slider_deg.on_changed(self.change_degree)

        # Parámetros modificables
        params = ['M', 'm', 'L', 'T', 'rho', 'S', 'Cd', 'y0_dot']
        self.textboxes = {}
        for i, p in enumerate(params):
            ax_box = plt.axes([slider_ax+0.02, 0.75 - i * spacing, 0.15, height])
            box = TextBox(ax_box, f'{p}: ', initial=str(getattr(self.eq, p)))
            box.on_submit(self.update_param)
            self.textboxes[p] = box

        # NUEVO: y0_dot
        # ax_y0_dot = plt.axes([slider_ax+0.02, 0.75 - len(params)*spacing, 0.15, height])
        # self.box_y0_dot = TextBox(ax_y0_dot, 'y0_dot: ', initial=str(self.eq.y0_dot))
        # self.box_y0_dot.on_submit(self.update_param)

        # Botones
        self.ax_reset = plt.axes([slider_ax, 0.15, 0.15, 0.05])
        self.button_reset = Button(self.ax_reset, 'Reset puntos')
        self.button_reset.on_clicked(self.reset_points)

        self.ax_fit = plt.axes([slider_ax, 0.05, 0.15, 0.05])
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
        self.axs[0, 0].set_title('x(t) — Rower Position')
        self.axs[0, 0].set_xlabel('Time [s]')
        self.axs[0, 0].set_ylabel('Position [m]')

        self.axs[1, 0].plot(s['tt'], s['xx_dot'], color='red')
        self.axs[1, 0].set_title("x'(t) — Rower Speed")
        self.axs[1, 0].set_xlabel('Time [s]')
        self.axs[1, 0].set_ylabel('Speed [m/s]')

        self.axs[2, 0].plot(s['tt'], s['xx_ddot'], color='green')
        self.axs[2, 0].set_title("x''(t) — Rower Acceleration")
        self.axs[2, 0].set_xlabel('Time [s]')
        self.axs[2, 0].set_ylabel('Acceleration [m/s²]')

        if self.points:
            px, py = zip(*self.points)
            self.axs[2, 0].scatter(px, py, color='black', label='Puntos')
            self.axs[2, 0].legend()

        # --- y(t)
        self.axs[0, 1].plot(s['tt'], s['yy'], color='blue')
        self.axs[0, 1].set_title('y(t) — Boat Position')
        self.axs[0, 1].set_xlabel('Time [s]')
        self.axs[0, 1].set_ylabel('Position [m]')

        self.axs[1, 1].plot(s['tt'], s['yy_dot'], color='red')
        self.axs[1, 1].set_title("y'(t) — Boat Speed")
        self.axs[1, 1].set_xlabel('Time [s]')
        self.axs[1, 1].set_ylabel('Speed [m/s]')

        self.axs[2, 1].plot(s['tt'], s['yy_ddot'], color='green')
        self.axs[2, 1].set_title("y''(t) — Boat Acceleration")
        self.axs[2, 1].set_xlabel('Time [s]')
        self.axs[2, 1].set_ylabel('Acceleration [m/s²]')


        for i in range(3):
            for j in range(2):
                self.axs[i, j].grid(True)
                self.axs[i, j].set_xlim(0, self.eq.T)

        if 'magnitudes' in s and self.eq.solution['magnitudes'] is not None:
            for txt in self.fig.texts:
                txt.remove()
            mag = s['magnitudes']
            info_text = (
                f"Ei: {mag['Ei']:.2f} J\n"                
                f"Ef: {mag['Ef']:.2f} J\n"
                f"dE_sist: {mag['dE_sist']:.2f} J\n"
                f"dE_rower: {mag['dE_rower']:.2f} J\n"
                f"dx_f: {mag['p_f']:.2f} m\n"
                f"v_f: {mag['v_f']:.2f} m/s\n"
                f"dv: {mag['dv']:.2f} m/s"
            )
            # Posición fija en la ventana de la figura
            self.fig.text(0.81, 0.33, info_text, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))
        try:
            # Antes de dibujar la imagen
            for j in range(2):
                self.axs[3, j].remove()  # elimina los axes vacíos de la fila 4
            img = mpimg.imread('assets/diagram.png')  # reemplaza con tu archivo
            ax_img = self.fig.add_axes([0.05, 0.00, 0.9, 0.25])  # ajusta la posición y tamaño
            ax_img.imshow(img)
            ax_img.axis('off')
        except:
            pass

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
        # Actualiza parámetros generales
        for name, box in self.textboxes.items():
            try:
                val = float(box.text)
                print(f"Actualizando {name} a {val}")
                setattr(self.eq, name, val)
            except ValueError:
                print(f"Valor no válido para {name}: {box.text}")

        # Actualiza y0_dot
        # try:
        #     self.eq.y0_dot = float(self.box_y0_dot.text)
        # except ValueError:
        #     print(f"Valor no válido para y0_dot: {self.box_y0_dot.text}")

        # Recalcular dependencias internas
        self.eq.mu = 1 / (self.eq.M + self.eq.m)
        self.eq.B = self.eq.m * self.eq.mu
        self.eq.A = -0.5 * self.eq.S * self.eq.rho * self.eq.Cd * self.eq.mu
        high_coeffs = [0] * (self.degree - 3)
        high_coeffs[-1] = 1
        self.eq.set_rower_cinematic(high_coeffs)
        # Resolver de nuevo la EDO
        self.eq.solve_edo()
        print(self.eq.summary())
        self.draw_plots()


    def fit_polynomial(self, event):
        if not self.points:
            print("No hay puntos seleccionados para ajustar.")
            return

        t_points, a_target = zip(*self.points)
        t_points = np.array(t_points)
        a_target = np.array(a_target)
        n_free = self.degree - 3  # cantidad de coeficientes libres (a4,...,an)

        # Construimos la matriz de diseño A y el vector y
        A = np.zeros((len(t_points), n_free))
        y = np.zeros(len(t_points))

        for i, t in enumerate(t_points):
            # Inicializamos los coeficientes libres con 0 temporalmente para calcular a2 y a3
            dummy_free = [0]*n_free
            self.eq.set_rower_cinematic(dummy_free)
            
            # Término constante (x''(t) con coeficientes libres = 0)
            x_ddot_base = self.eq.x_ddot(np.array([t]))[0]
            y[i] = a_target[i] - x_ddot_base
            
            # Llenamos la fila de la matriz A para cada coeficiente libre
            for j in range(n_free):
                test_free = [0]*n_free
                test_free[j] = 1  # solo este coeficiente = 1
                self.eq.set_rower_cinematic(test_free)
                x_ddot_col = self.eq.x_ddot(np.array([t]))[0]
                A[i, j] = x_ddot_col - x_ddot_base

        # Resolver el sistema lineal en mínimos cuadrados
        best_a, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)

        # Guardar los coeficientes en RowEquation
        self.eq.set_rower_cinematic(best_a)
        self.eq.solve_edo()
        print(f"Ajuste analítico terminado. Error cuadrático: {np.sum((self.eq.x_ddot(t_points) - a_target)**2):.3e}")
        self.draw_plots()



if __name__ == "__main__":
    InteractiveRowEquationPlot()
