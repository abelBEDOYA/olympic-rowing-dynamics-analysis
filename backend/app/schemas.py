from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SimulationParameters(BaseModel):
    """Input parameters for simulation."""
    m: float = Field(default=80, description="Rower mass (kg)")
    M: float = Field(default=20, description="Boat mass (kg)")
    L: float = Field(default=-1, description="Total displacement (m)")
    T: float = Field(default=1, description="Phase duration (s)")
    rho: float = Field(default=1000, description="Water density (kg/m³)")
    S: float = Field(default=0.5, description="Cross-sectional area (m²)")
    Cd: float = Field(default=0.004, description="Drag coefficient")
    y0_dot: float = Field(default=10, description="Initial boat velocity (m/s)")
    degree: int = Field(default=4, ge=3, description="Polynomial degree (>=3)")
    high_coeffs: Optional[List[float]] = Field(
        default=None,
        description="Free polynomial coefficients (a4, a5, ...). If None, uses [1] * (degree-3)"
    )


class Magnitudes(BaseModel):
    """Physical magnitudes computed from simulation."""
    Ei: float = Field(description="Initial kinetic energy (J)")
    Ef: float = Field(description="Final kinetic energy (J)")
    dE_sist: float = Field(description="System energy change (J)")
    dE_rower: float = Field(description="Energy spent by rower (J)")
    p_f: float = Field(description="Final boat position (m)")
    v_f: float = Field(description="Final boat velocity (m/s)")
    dv: float = Field(description="Velocity change (m/s)")


class SimulationResult(BaseModel):
    """Result of a simulation run."""
    tt: List[float] = Field(description="Time points")
    xx: List[float] = Field(description="Rower position")
    xx_dot: List[float] = Field(description="Rower velocity")
    xx_ddot: List[float] = Field(description="Rower acceleration")
    yy: List[float] = Field(description="Boat position")
    yy_dot: List[float] = Field(description="Boat velocity")
    yy_ddot: List[float] = Field(description="Boat acceleration")
    magnitudes: Magnitudes
    polynomial_latex: str = Field(description="LaTeX representation of polynomial")
    coefficients: List[float] = Field(description="Polynomial coefficients")


class FitPolynomialRequest(BaseModel):
    """Request to fit a polynomial through given points."""
    parameters: SimulationParameters
    points: List[Dict[str, float]] = Field(
        description="Points to fit: [{'t': time, 'a': acceleration}, ...]"
    )


class DefaultParametersResponse(BaseModel):
    """Default simulation parameters."""
    m: float
    M: float
    L: float
    T: float
    rho: float
    S: float
    Cd: float
    y0_dot: float
    degree: int
