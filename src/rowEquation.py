import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


class RowEquation():
    def __init__(self,m=80, M=20, L=-1, T=1, rho: float = 1000, S: float = 0.5, Cd: float = 0.004, y0_dot: float = 10):
        self.m = m
        self.M = M
        self.L = L
        self.T = T
        self.mu = 1/(M+m)
        self.B = self.m*self.mu
        self.Cd = Cd #N s^2 / m^2
        self.rho = rho # kg/m^3
        self.S = S
        self.A = -0.5*self.S*self.rho*self.Cd*self.mu
        self.coeffs = []
        self.polinomical_grade = None
        self.y0 = 0
        self.y0_dot = y0_dot
        self.solution = None

    def set_rower_cinematic(self, high_coeffs: list = []):
        """
        Define the coefficients of the polynomial rower cinematic.
        Coefficients a0, a1, a2, a3 are not free — they are derived from the others.
        """
        high_coeffs = list(high_coeffs)   # ✅ convierte arrays a listas

        n = len(high_coeffs) + 3  # grado del polinomio

        a2 = 3 * self.L / self.T**2 + sum(
            (k - 3) * high_coeffs[k - 4] * self.T**(k - 2)
            for k in range(4, n + 1)
        )
        a3 = -2 * self.L / self.T**3 - sum(
            (k - 2) * high_coeffs[k - 4] * self.T**(k - 3)
            for k in range(4, n + 1)
        )

        self.coeffs = [0, 0, a2, a3] + high_coeffs
        self.polinomical_grade = len(self.coeffs) - 1

        return len(self.coeffs), self.polinomical_grade

    def x(self,t):
        """
        Calculates the rower position according to his/her polinomical cinematic. Depens on time.
        Ship position is the rower frame of reference. 
        """
        return sum(self.coeffs[k]*t**k for k in range(len(self.coeffs)))

    def x_dot(self,t):
        """
        Calculates the rower speed according to his/her polinomical cinematic. Depens on time.
        Ship position is the rower frame of reference. 
        """
        return sum(k*self.coeffs[k]*t**(k-1) for k in range(1, len(self.coeffs)))

    def x_ddot(self,t):
        """
        Calculates the rower acceleration according to his/her polinomical cinematic. Depens on time.
         Ship position is the rower frame of reference. 
        """
        return sum(k*(k-1)*self.coeffs[k]*t**(k-2) for k in range(2, len(self.coeffs)))

    def dynamic_edo(self, t, v):
        """Dynamic EDO which relates water frictional force and the rower's movement on the ship."""
        return self.A*np.abs(v)*v - self.B*self.x_ddot(t)

    def solve_edo(self, y0: float =0, y0_dot: float = None, n_t_intervals: int = 5000):

        # ----------------------
        # Resolver numéricamente
        # ----------------------
        y0_dot = self.y0_dot if y0_dot is None else y0_dot
        t_span = (0, self.T)
        t_eval = np.linspace(0, self.T, n_t_intervals)
        sol = solve_ivp(lambda t, y: [self.dynamic_edo(t, y[0]), y[0]], t_span, [y0_dot, y0], t_eval=t_eval)

        yy_dot = sol.y[0]  # y'(t)
        yy = sol.y[1]  # y(t)
        yy_ddot = self.A * yy_dot**2 - self.B * np.array([self.x_ddot(ti) for ti in t_eval])

        tt = np.linspace(0, self.T, n_t_intervals)
        xx = self.x(tt)
        xx_dot = self.x_dot(tt)
        xx_ddot = self.x_ddot(tt)

        solution = {'tt': tt,
                    'xx': xx,
                    'xx_dot': xx_dot,
                    'xx_ddot': xx_ddot,
                    'yy': yy,
                    'yy_dot': yy_dot,
                    'yy_ddot': yy_ddot}
        self.solution = solution
        self.calculate_magnitudes()
        return solution
    
    def calculate_magnitudes(self):
        if not self.solution:
            return 
        V_i = self.y0_dot
        V_f = self.solution['yy_dot'][-1]
        # p_i = self.solution['yy'][0]
        p_f = self.solution['yy'][-1]

        ## Energía mecánica perdida del sistema:
        Ei = 0.5*(self.M+self.m)*V_i**2
        Ef = 0.5*(self.M+self.m)*V_f**2
        dE_sistema =Ef - Ei
        ## Energía gastaad por el remero:
        dE_rower = self.calculate_energy()

        self.solution['magnitudes'] = {
            'Ei': Ei,
            'Ef': Ef,
            'dE_sist': dE_sistema,
            'dE_rower': dE_rower,
            'p_f': p_f,
            'v_f': V_f,
            'dv': V_f-V_i}

    def calculate_energy(self):
        """
        Calcula la energía gastada por la persona al caminar sobre el barco
        usando la solución almacenada en self.solution.
        """
        if self.solution is None:
            raise ValueError("Primero debes resolver la EDO con solve_edo()")

        tt = self.solution['tt']
        xx_ddot = self.solution['xx_ddot']   # aceleración persona relativa al barco
        yy_dot = self.solution['yy_dot']     # velocidad barco relativa al agua
        xx_dot = self.solution['xx_dot']     # velocidad persona relativa al barco
        yy_ddot = self.solution['yy_ddot']     # velocidad barco relativa al agua

        # Fuerza que la persona aplica sobre el barco
        # F_persona = self.B * xx_ddot + self.A * np.abs(yy_dot) * yy_dot
        F_persona = self.m*(xx_ddot+yy_ddot)
        # Energía gastada = integral de F_persona * v_rel_persona dt
        dt = tt[1] - tt[0]
        E_persona = np.sum(F_persona * xx_dot)*dt

        return E_persona

    def plot_rower_cinematic(self, n_t:int = 1000):
        if not self.coeffs:
            print("Set the coefficients of the polinomical rower's cinematic before plotting the results.")
        tt = np.linspace(0, self.T, n_t)
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.plot(tt, self.x(tt), label='x(t) [L]', color='blue')
        plt.xlabel('t')
        # plt.ylabel('p(t)')
        plt.title('Polinomio p(t)')
        plt.grid(True)
        plt.legend()

        plt.subplot(1,2,1)
        plt.plot(tt, self.x_dot(tt), label="x'(t) [L/T]", color='red')
        plt.xlabel('t')
        # plt.ylabel("dp(t)")
        plt.title('Derivada dp(t)')
        plt.grid(True)
        plt.legend()

        plt.subplot(1,2,1)
        plt.plot(tt, self.x_ddot(tt), label="x''(t) [L/T^2]", color='green')
        plt.xlabel('t')
        # plt.ylabel("ddp(t)")
        plt.title('Derivada ddp(t)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

    def plot(self):
        if not self.solution:
            print('Solve the EDO with solve_edo() method before plotting results')
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.plot(self.solution['tt'], self.solution['xx'], label='x(t)[L]', color='blue')
        plt.xlabel('t')
        plt.ylabel('p(t)')
        plt.title('Polinomio p(t)')
        plt.grid(True)
        plt.legend()

        plt.subplot(1,2,1)
        plt.plot(self.solution['tt'], self.solution['xx_dot'], label="x'(t) [L/T]", color='red')
        plt.xlabel('t')
        plt.ylabel("dp(t)")
        plt.title('Derivada dp(t)')
        plt.grid(True)
        plt.legend()

        plt.subplot(1,2,1)
        plt.plot(self.solution['tt'], self.solution['xx_ddot'], label="x''(t) [L/T^2]", color='green')
        plt.xlabel('t')
        plt.ylabel("ddp(t)")
        plt.title('Derivada ddp(t)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        # plt.show()
        plt.figure(figsize=(10,5))
        plt.plot(self.solution['tt'], self.solution['yy'], label='y(t) [L]')
        plt.plot(self.solution['tt'], self.solution['yy_dot'], label="y'(t) [L/T]")
        plt.plot(self.solution['tt'], self.solution['yy_ddot'], label = "y''(t) [L/T^2]")
        plt.xlabel('t')
        plt.title('Solución de la EDO')
        plt.legend()
        plt.grid(True)
        plt.show()

    def summary(self):
        info = {'M': self.M,
                'm': self.m,
                'L': self.L,
                'T': self.T,
                'pol_grade': self.polinomical_grade,
                'pol_coeffs': self.coeffs,
                'y0': self.y0,
                'y0_dot': self.y0_dot,
                'solution': True if self.solution is not None else False}
        return info
