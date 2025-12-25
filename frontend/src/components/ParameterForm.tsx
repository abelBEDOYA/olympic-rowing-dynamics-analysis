import { useState, useEffect } from 'react';
import { getDefaultParameters } from '../api';
import type { SimulationParameters } from '../api';
import { NumberInput } from './NumberInput';
import { useLang } from '../contexts';
import { getTranslation } from '../translations';

interface ParameterFormProps {
    onCalculate: (params: SimulationParameters) => void;
    loading: boolean;
}

export function ParameterForm({ onCalculate, loading }: ParameterFormProps) {
    const { lang } = useLang();
    const t = getTranslation(lang);
    const [params, setParams] = useState<SimulationParameters | null>(null);

    useEffect(() => {
        getDefaultParameters().then(setParams).catch(() => {
            // Fallback defaults if API fails
            setParams({
                m: 80, M: 20, L: -1, T: 1, rho: 1000, S: 0.5, Cd: 0.004, y0_dot: 10, degree: 4
            });
        });
    }, []);

    if (!params) return <div className="loading-params">Loading parameters...</div>;

    const handleChange = (key: keyof SimulationParameters, value: number) => {
        setParams(prev => prev ? { ...prev, [key]: value } : null);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (params) onCalculate(params);
    };

    return (
        <form className="parameter-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.rowerMass}
                    value={params.m}
                    onChange={(v) => handleChange('m', v)}
                    min={40} max={120} step={1} unit="kg"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.boatMass}
                    value={params.M}
                    onChange={(v) => handleChange('M', v)}
                    min={10} max={50} step={0.5} unit="kg"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.displacement}
                    value={params.L}
                    onChange={(v) => handleChange('L', v)}
                    min={-2} max={0} step={0.05} unit="m"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.duration}
                    value={params.T}
                    onChange={(v) => handleChange('T', v)}
                    min={0.5} max={2.0} step={0.05} unit="s"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.waterDensity}
                    value={params.rho}
                    onChange={(v) => handleChange('rho', v)}
                    min={900} max={1100} step={10} unit="kg/m³"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.crossSection}
                    value={params.S}
                    onChange={(v) => handleChange('S', v)}
                    min={0.1} max={1.0} step={0.05} unit="m²"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.dragCoeff}
                    value={params.Cd}
                    onChange={(v) => handleChange('Cd', v)}
                    min={0.001} max={0.01} step={0.001}
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.initialVelocity}
                    value={params.y0_dot}
                    onChange={(v) => handleChange('y0_dot', v)}
                    min={0} max={20} step={0.5} unit="m/s"
                />
            </div>
            <div className="form-group">
                <NumberInput
                    label={t.analysis.polyDegree}
                    value={params.degree}
                    onChange={(v) => handleChange('degree', v)}
                    min={3} max={8} step={1}
                />
            </div>

            <hr className="section-divider" />

            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
                {loading ? t.analysis.calculating : `⚡ ${t.analysis.calculate}`}
            </button>
        </form>
    );
}
