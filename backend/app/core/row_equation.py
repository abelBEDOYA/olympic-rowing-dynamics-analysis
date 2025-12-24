import numpy as np
from scipy.integrate import solve_ivp
from typing import List, Optional, Dict, Any


class RowEquation:
    """
    Physics model for the rower-boat-water 1D system during the aerial phase.
    
    This class calculates the dynamics of a rower moving on a boat,
    considering water friction and momentum exchange.
    """
    
    def __init__(
        self,
        m: float = 80,      # Rower mass (kg)
        M: float = 20,      # Boat mass (kg)
        L: float = -1,      # Total displacement (m)
        T: float = 1,       # Phase duration (s)
        rho: float = 1000,  # Water density (kg/m³)
        S: float = 0.5,     # Cross-sectional area (m²)
        Cd: float = 0.004,  # Drag coefficient
        y0_dot: float = 10  # Initial boat velocity (m/s)
    ):
        self.m = m
        self.M = M
        self.L = L
        self.T = T
        self.mu = 1 / (M + m)
        self.B = self.m * self.mu
        self.Cd = Cd
        self.rho = rho
        self.S = S
        self.A = -0.5 * self.S * self.rho * self.Cd * self.mu
        self.coeffs: List[float] = []
        self.polinomical_grade: Optional[int] = None
        self.y0 = 0
        self.y0_dot = y0_dot
        self.solution: Optional[Dict[str, Any]] = None

    def set_rower_cinematic(self, high_coeffs: List[float] = []) -> tuple:
        """
        Define the coefficients of the polynomial rower cinematic.
        Coefficients a0, a1, a2, a3 are derived from boundary conditions.
        
        Args:
            high_coeffs: Free coefficients (a4, a5, ..., an)
            
        Returns:
            Tuple of (number of coefficients, polynomial grade)
        """
        high_coeffs = list(high_coeffs)
        n = len(high_coeffs) + 3

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

    def x(self, t) -> np.ndarray:
        """Calculate rower position relative to boat."""
        t = np.atleast_1d(t)
        return sum(self.coeffs[k] * t**k for k in range(len(self.coeffs)))

    def x_dot(self, t) -> np.ndarray:
        """Calculate rower velocity relative to boat."""
        t = np.atleast_1d(t)
        return sum(k * self.coeffs[k] * t**(k-1) for k in range(1, len(self.coeffs)))

    def x_ddot(self, t) -> np.ndarray:
        """Calculate rower acceleration relative to boat."""
        t = np.atleast_1d(t)
        return sum(k * (k-1) * self.coeffs[k] * t**(k-2) for k in range(2, len(self.coeffs)))

    def dynamic_edo(self, t: float, v: float) -> float:
        """Dynamic ODE relating water friction and rower's movement."""
        x_ddot_val = self.x_ddot(t)
        # Ensure we return a scalar
        if hasattr(x_ddot_val, '__len__'):
            x_ddot_val = float(x_ddot_val[0])
        return float(self.A * np.abs(v) * v - self.B * x_ddot_val)

    def solve_edo(
        self,
        y0: float = 0,
        y0_dot: Optional[float] = None,
        n_t_intervals: int = 5000
    ) -> Dict[str, Any]:
        """
        Solve the differential equation numerically.
        
        Args:
            y0: Initial boat position
            y0_dot: Initial boat velocity (uses self.y0_dot if None)
            n_t_intervals: Number of time intervals
            
        Returns:
            Dictionary with time series and computed magnitudes
        """
        y0_dot = self.y0_dot if y0_dot is None else y0_dot
        t_span = (0, self.T)
        t_eval = np.linspace(0, self.T, n_t_intervals)
        
        sol = solve_ivp(
            lambda t, y: [self.dynamic_edo(t, y[0]), y[0]],
            t_span,
            [y0_dot, y0],
            t_eval=t_eval
        )

        yy_dot = sol.y[0]  # Boat velocity
        yy = sol.y[1]      # Boat position
        
        # Calculate x_ddot for each time point, ensuring scalar output
        x_ddot_vals = np.array([float(self.x_ddot(np.array([ti]))[0]) for ti in t_eval])
        yy_ddot = self.A * yy_dot**2 - self.B * x_ddot_vals

        tt = np.linspace(0, self.T, n_t_intervals)
        xx = np.array(self.x(tt)).flatten()
        xx_dot = np.array(self.x_dot(tt)).flatten()
        xx_ddot = np.array(self.x_ddot(tt)).flatten()

        self.solution = {
            'tt': tt.tolist(),
            'xx': xx.tolist(),
            'xx_dot': xx_dot.tolist(),
            'xx_ddot': xx_ddot.tolist(),
            'yy': yy.tolist(),
            'yy_dot': yy_dot.tolist(),
            'yy_ddot': yy_ddot.tolist()
        }
        
        self._calculate_magnitudes()
        return self.solution

    def _calculate_magnitudes(self) -> None:
        """Calculate energy and other physical magnitudes."""
        if not self.solution:
            return
            
        V_i = self.y0_dot
        V_f = self.solution['yy_dot'][-1]
        p_f = self.solution['yy'][-1]

        # System mechanical energy change
        Ei = 0.5 * (self.M + self.m) * V_i**2
        Ef = 0.5 * (self.M + self.m) * V_f**2
        dE_sistema = Ef - Ei
        
        # Energy spent by rower
        dE_rower = self._calculate_energy()

        self.solution['magnitudes'] = {
            'Ei': float(Ei),
            'Ef': float(Ef),
            'dE_sist': float(dE_sistema),
            'dE_rower': float(dE_rower),
            'p_f': float(p_f),
            'v_f': float(V_f),
            'dv': float(V_f - V_i)
        }

    def _calculate_energy(self) -> float:
        """Calculate energy spent by the rower."""
        if self.solution is None:
            raise ValueError("Must solve ODE first with solve_edo()")

        tt = np.array(self.solution['tt'])
        xx_ddot = np.array(self.solution['xx_ddot'])
        xx_dot = np.array(self.solution['xx_dot'])
        yy_ddot = np.array(self.solution['yy_ddot'])

        F_persona = self.m * (xx_ddot + yy_ddot)
        dt = tt[1] - tt[0]
        E_persona = np.sum(F_persona * xx_dot) * dt

        return float(E_persona)

    def get_polynomial_latex(self) -> str:
        """Get LaTeX representation of the polynomial."""
        terms = []
        for i, c in enumerate(self.coeffs):
            if abs(c) > 1e-10:
                coef = round(c, 3)
                # Format coefficient
                if i == 0:
                    terms.append(f"{coef}")
                elif i == 1:
                    if coef == 1:
                        terms.append("t")
                    elif coef == -1:
                        terms.append("-t")
                    else:
                        terms.append(f"{coef}t")
                else:
                    if coef == 1:
                        terms.append(f"t^{{{i}}}")
                    elif coef == -1:
                        terms.append(f"-t^{{{i}}}")
                    else:
                        terms.append(f"{coef}t^{{{i}}}")
        
        if not terms:
            return "x(t) = 0"
        
        # Join with proper + and - signs
        result = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                result += f" - {term[1:]}"
            else:
                result += f" + {term}"
        return f"x(t) = {result}"

    def summary(self) -> Dict[str, Any]:
        """Get summary of current configuration and state."""
        return {
            'M': self.M,
            'm': self.m,
            'L': self.L,
            'T': self.T,
            'pol_grade': self.polinomical_grade,
            'pol_coeffs': self.coeffs,
            'y0': self.y0,
            'y0_dot': self.y0_dot,
            'has_solution': self.solution is not None
        }
