import { useState, useCallback } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from 'recharts';
import type {
    SimulationParameters,
    SimulationResult,
    Point,
} from '../api';
import {
    calculateSimulation,
    fitPolynomial,
} from '../api';
import { InteractiveChart } from '../InteractiveChart';
import { Latex } from '../Latex';
import { ParameterForm } from '../components/ParameterForm';
import { useLang } from '../contexts';
import { getTranslation } from '../translations';

export function AnalysisPage() {
    const { lang } = useLang();
    const t = getTranslation(lang);

    const [result, setResult] = useState<SimulationResult | null>(null);
    const [points, setPoints] = useState<Point[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    // Keep track of last used params for fitting
    const [lastParams, setLastParams] = useState<SimulationParameters | null>(null);

    const handleCalculate = async (params: SimulationParameters) => {
        setLoading(true);
        setError(null);
        setLastParams(params);

        // On mobile, close sidebar after calculation to show results
        if (window.innerWidth < 768) {
            setSidebarOpen(false);
        }
        try {
            const data = await calculateSimulation(params);
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al calcular');
        } finally {
            setLoading(false);
        }
    };

    const handleFitPolynomial = async () => {
        if (points.length === 0) {
            setError(t.analysis.selectPointsError);
            return;
        }
        if (!lastParams) {
            setError("Calcula primero para establecer los parámetros base");
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const data = await fitPolynomial({ parameters: lastParams, points });
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al ajustar polinomio');
        } finally {
            setLoading(false);
        }
    };

    const addPoint = useCallback(
        (point: Point) => {
            setPoints((prev) => [...prev, point]);
        },
        []
    );

    const removePoint = (index: number) => {
        setPoints((prev) => prev.filter((_, i) => i !== index));
    };

    const clearPoints = () => {
        setPoints([]);
    };

    // Transform data for charts
    const getChartData = (key: keyof SimulationResult) => {
        if (!result) return [];
        const values = result[key] as number[];
        return result.tt.map((t, i) => ({ t, value: values[i] }));
    };

    const chartConfigs = [
        { key: 'xx', title: `x(t) — ${t.analysis.rowerPosition}`, color: '#6366f1', yLabel: t.units.m },
        { key: 'xx_dot', title: `x'(t) — ${t.analysis.rowerVelocity}`, color: '#8b5cf6', yLabel: t.units.mps },
        { key: 'xx_ddot', title: `x''(t) — ${t.analysis.rowerAcceleration}`, color: '#a855f7', yLabel: t.units.mps2, interactive: true },
        { key: 'yy', title: `y(t) — ${t.analysis.boatPosition}`, color: '#22c55e', yLabel: t.units.m },
        { key: 'yy_dot', title: `y'(t) — ${t.analysis.boatVelocity}`, color: '#14b8a6', yLabel: t.units.mps },
        { key: 'yy_ddot', title: `y''(t) — ${t.analysis.boatAcceleration}`, color: '#06b6d4', yLabel: t.units.mps2 },
    ];

    return (
        <div className="analysis-page">
            <button
                className="sidebar-toggle-btn"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                aria-label="Toggle parameters"
            >
                {sidebarOpen ? '◀' : '▶'} {t.analysis.parameters}
            </button>

            <div className={`analysis-container ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                {/* Sidebar */}
                <aside className="analysis-sidebar">
                    <div className="sidebar-header">
                        <h2>{t.analysis.parameters}</h2>
                    </div>

                    <ParameterForm onCalculate={handleCalculate} loading={loading} />

                    {/* Points section */}
                    {result && (
                        <div className="points-section">
                            <h4>{t.analysis.fittingPoints} ({points.length})</h4>
                            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                                {t.analysis.clickToAdd}
                            </p>
                            {points.length > 0 && (
                                <div className="points-list">
                                    {points.map((p, i) => (
                                        <span key={i} className="point-tag">
                                            t={p.t.toFixed(2)}, a={p.a.toFixed(2)}
                                            <button onClick={() => removePoint(i)}>×</button>
                                        </span>
                                    ))}
                                </div>
                            )}
                            <div style={{ display: 'flex', gap: '8px' }}>
                                <button
                                    type="button"
                                    className="btn btn-secondary"
                                    onClick={clearPoints}
                                    disabled={points.length === 0}
                                >
                                    {t.analysis.clear}
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-primary"
                                    onClick={handleFitPolynomial}
                                    disabled={loading || points.length === 0}
                                >
                                    {t.analysis.fitPolynomial}
                                </button>
                            </div>
                        </div>
                    )}

                    {error && (
                        <div style={{ color: 'var(--error)', fontSize: '0.85rem', padding: '8px' }}>
                            ⚠️ {error}
                        </div>
                    )}
                </aside>

                {/* Main content */}
                <main className="analysis-main">
                    {!result && !loading && (
                        <div className="empty-state">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z" />
                            </svg>
                            <p>{t.analysis.emptyState}</p>
                        </div>
                    )}

                    {loading && (
                        <div className="loading">
                            <div className="spinner"></div>
                            {t.analysis.calculating}
                        </div>
                    )}

                    {result && !loading && (
                        <>
                            {/* Results panel */}
                            <div className="results-panel">
                                <h3>📊 {t.analysis.results}</h3>
                                <div className="results-grid">
                                    <div className="result-item">
                                        <div className="label">{t.analysis.initialEnergy}</div>
                                        <div className="value">
                                            {result.magnitudes.Ei.toFixed(2)}
                                            <span className="unit">{t.units.j}</span>
                                        </div>
                                    </div>
                                    <div className="result-item">
                                        <div className="label">{t.analysis.finalEnergy}</div>
                                        <div className="value">
                                            {result.magnitudes.Ef.toFixed(2)}
                                            <span className="unit">{t.units.j}</span>
                                        </div>
                                    </div>
                                    <div className="result-item">
                                        <div className="label">{t.analysis.systemDeltaE}</div>
                                        <div className="value">
                                            {result.magnitudes.dE_sist.toFixed(2)}
                                            <span className="unit">{t.units.j}</span>
                                        </div>
                                    </div>
                                    <div className="result-item">
                                        <div className="label">{t.analysis.rowerEnergy}</div>
                                        <div className="value">
                                            {result.magnitudes.dE_rower.toFixed(2)}
                                            <span className="unit">{t.units.j}</span>
                                        </div>
                                    </div>
                                    <div className="result-item">
                                        <div className="label">{t.analysis.finalPosition}</div>
                                        <div className="value">
                                            {result.magnitudes.p_f.toFixed(3)}
                                            <span className="unit">{t.units.m}</span>
                                        </div>
                                    </div>
                                    <div className="result-item">
                                        <div className="label">{t.analysis.finalVelocity}</div>
                                        <div className="value">
                                            {result.magnitudes.v_f.toFixed(3)}
                                            <span className="unit">{t.units.mps}</span>
                                        </div>
                                    </div>
                                    <div className="result-item">
                                        <div className="label">{t.analysis.deltaV}</div>
                                        <div className="value">
                                            {result.magnitudes.dv.toFixed(4)}
                                            <span className="unit">{t.units.mps}</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="polynomial-display">
                                    <Latex math={result.polynomial_latex} displayMode />
                                </div>
                            </div>

                            {/* Charts grid */}
                            <div className="charts-grid">
                                {chartConfigs.map((config) =>
                                    config.interactive ? (
                                        <div key={config.key} className="chart-card interactive">
                                            <h3>
                                                {config.title}
                                                <span className="badge">{t.analysis.interactive}</span>
                                            </h3>
                                            <InteractiveChart
                                                data={getChartData(config.key as keyof SimulationResult)}
                                                color={config.color}
                                                yLabel={config.yLabel}
                                                points={points}
                                                onAddPoint={addPoint}
                                                T={lastParams?.T || 1}
                                            />
                                        </div>
                                    ) : (
                                        <div key={config.key} className="chart-card">
                                            <h3>{config.title}</h3>
                                            <ResponsiveContainer width="100%" height={220}>
                                                <LineChart data={getChartData(config.key as keyof SimulationResult)}>
                                                    <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3a" />
                                                    <XAxis
                                                        dataKey="t"
                                                        stroke="#606070"
                                                        tickFormatter={(v) => v.toFixed(2)}
                                                        fontSize={11}
                                                    />
                                                    <YAxis
                                                        stroke="#606070"
                                                        tickFormatter={(v) => v.toFixed(2)}
                                                        fontSize={11}
                                                    />
                                                    <Tooltip
                                                        contentStyle={{
                                                            background: '#16161f',
                                                            border: '1px solid #2a2a3a',
                                                            borderRadius: '8px',
                                                        }}
                                                        labelFormatter={(v) => `t = ${Number(v).toFixed(3)} s`}
                                                        formatter={(v) => [`${Number(v).toFixed(4)} ${config.yLabel}`, '']}
                                                    />
                                                    <Line
                                                        type="monotone"
                                                        dataKey="value"
                                                        stroke={config.color}
                                                        strokeWidth={2}
                                                        dot={false}
                                                        activeDot={{ r: 4, fill: config.color }}
                                                    />
                                                </LineChart>
                                            </ResponsiveContainer>
                                        </div>
                                    )
                                )}
                            </div>
                        </>
                    )}
                </main>
            </div>
        </div>
    );
}
