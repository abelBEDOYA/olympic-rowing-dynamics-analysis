from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from typing import List

from app.core.row_equation import RowEquation
from app.schemas import (
    SimulationParameters,
    SimulationResult,
    FitPolynomialRequest,
    DefaultParametersResponse,
    Magnitudes
)

app = FastAPI(
    title="Rowing Dynamics API",
    description="API for simulating rower-boat-water 1D physics",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/parameters/defaults", response_model=DefaultParametersResponse)
async def get_default_parameters():
    """Get default simulation parameters."""
    return DefaultParametersResponse(
        m=80,
        M=20,
        L=-1,
        T=1,
        rho=1000,
        S=0.5,
        Cd=0.004,
        y0_dot=10,
        degree=4
    )


@app.post("/api/calculate", response_model=SimulationResult)
async def calculate_simulation(params: SimulationParameters):
    """
    Run simulation with given parameters.
    
    Returns time series for rower and boat kinematics,
    plus computed physical magnitudes.
    """
    try:
        # Create model instance
        model = RowEquation(
            m=params.m,
            M=params.M,
            L=params.L,
            T=params.T,
            rho=params.rho,
            S=params.S,
            Cd=params.Cd,
            y0_dot=params.y0_dot
        )
        
        # Generate polynomial coefficients
        if params.high_coeffs is not None:
            high_coeffs = params.high_coeffs
        else:
            n_free = params.degree - 3
            high_coeffs = [0.0] * n_free
            if n_free > 0:
                high_coeffs[-1] = 1.0
        
        model.set_rower_cinematic(high_coeffs)
        solution = model.solve_edo()
        print('calculate_simulation solution', solution)
        return SimulationResult(
            tt=solution['tt'],
            xx=solution['xx'],
            xx_dot=solution['xx_dot'],
            xx_ddot=solution['xx_ddot'],
            yy=solution['yy'],
            yy_dot=solution['yy_dot'],
            yy_ddot=solution['yy_ddot'],
            magnitudes=Magnitudes(**solution['magnitudes']),
            polynomial_latex=model.get_polynomial_latex(),
            coefficients=model.coeffs
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fit-polynomial", response_model=SimulationResult)
async def fit_polynomial(request: FitPolynomialRequest):
    """
    Fit polynomial coefficients to match given acceleration points.
    
    Uses least squares optimization to find the best-fit polynomial
    that passes through the specified (time, acceleration) points.
    """
    try:
        params = request.parameters
        points = request.points
        
        if not points:
            raise HTTPException(status_code=400, detail="No points provided for fitting")
        
        # Create model
        model = RowEquation(
            m=params.m,
            M=params.M,
            L=params.L,
            T=params.T,
            rho=params.rho,
            S=params.S,
            Cd=params.Cd,
            y0_dot=params.y0_dot
        )
        
        n_free = params.degree - 3
        if n_free <= 0:
            raise HTTPException(status_code=400, detail="Degree must be >= 4 for fitting")
        
        t_points = np.array([p['t'] for p in points])
        a_target = np.array([p['a'] for p in points])
        
        # Build design matrix for least squares
        A = np.zeros((len(t_points), n_free))
        y = np.zeros(len(t_points))
        
        for i, t in enumerate(t_points):
            # Base case: all free coeffs = 0
            dummy_free = [0.0] * n_free
            model.set_rower_cinematic(dummy_free)
            x_ddot_base = float(model.x_ddot(np.array([t]))[0])
            y[i] = a_target[i] - x_ddot_base
            
            # Contribution of each free coefficient
            for j in range(n_free):
                test_free = [0.0] * n_free
                test_free[j] = 1.0
                model.set_rower_cinematic(test_free)
                x_ddot_col = float(model.x_ddot(np.array([t]))[0])
                A[i, j] = x_ddot_col - x_ddot_base
        
        # Solve least squares
        best_coeffs, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
        
        # Apply fitted coefficients
        model.set_rower_cinematic(best_coeffs.tolist())
        solution = model.solve_edo()
        
        return SimulationResult(
            tt=solution['tt'],
            xx=solution['xx'],
            xx_dot=solution['xx_dot'],
            xx_ddot=solution['xx_ddot'],
            yy=solution['yy'],
            yy_dot=solution['yy_dot'],
            yy_ddot=solution['yy_ddot'],
            magnitudes=Magnitudes(**solution['magnitudes']),
            polynomial_latex=model.get_polynomial_latex(),
            coefficients=model.coeffs
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
