import axios from 'axios';

// In production (served by nginx), use relative paths so requests go through nginx proxy
// In development, use the VITE_API_URL environment variable or default to localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface SimulationParameters {
    m: number;
    M: number;
    L: number;
    T: number;
    rho: number;
    S: number;
    Cd: number;
    y0_dot: number;
    degree: number;
    high_coeffs?: number[] | null;
}

export interface Magnitudes {
    Ei: number;
    Ef: number;
    dE_sist: number;
    dE_rower: number;
    p_f: number;
    v_f: number;
    dv: number;
}

export interface SimulationResult {
    tt: number[];
    xx: number[];
    xx_dot: number[];
    xx_ddot: number[];
    yy: number[];
    yy_dot: number[];
    yy_ddot: number[];
    magnitudes: Magnitudes;
    polynomial_latex: string;
    coefficients: number[];
}

export interface Point {
    t: number;
    a: number;
}

export interface FitPolynomialRequest {
    parameters: SimulationParameters;
    points: Point[];
}

export const getDefaultParameters = async (): Promise<SimulationParameters> => {
    const response = await api.get('/api/parameters/defaults');
    return response.data;
};

export const calculateSimulation = async (params: SimulationParameters): Promise<SimulationResult> => {
    const response = await api.post('/api/calculate', params);
    return response.data;
};

export const fitPolynomial = async (request: FitPolynomialRequest): Promise<SimulationResult> => {
    const response = await api.post('/api/fit-polynomial', request);
    return response.data;
};

export default api;
