import { useRef, useCallback, useState, useEffect } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceDot,
} from 'recharts';

interface ChartDataPoint {
    t: number;
    value: number;
}

interface Point {
    t: number;
    a: number;
}

interface InteractiveChartProps {
    data: ChartDataPoint[];
    color: string;
    yLabel: string;
    points: Point[];
    onAddPoint: (point: Point) => void;
    T: number; // Duration for x-axis max
}

export function InteractiveChart({
    data,
    color,
    yLabel,
    points,
    onAddPoint,
    T,
}: InteractiveChartProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const [chartBounds, setChartBounds] = useState<{
        left: number;
        right: number;
        top: number;
        bottom: number;
        xMin: number;
        xMax: number;
        yMin: number;
        yMax: number;
    } | null>(null);

    // Calculate data bounds
    const yValues = data.map((d) => d.value);
    const yMin = Math.min(...yValues, ...points.map((p) => p.a));
    const yMax = Math.max(...yValues, ...points.map((p) => p.a));
    const yPadding = (yMax - yMin) * 0.1 || 1;

    // Update chart bounds when data changes
    useEffect(() => {
        // Recharts uses margins: left=60, right=10, top=10, bottom=30
        const leftMargin = 60;
        const rightMargin = 10;
        const topMargin = 10;
        const bottomMargin = 30;

        if (containerRef.current) {
            const rect = containerRef.current.getBoundingClientRect();
            setChartBounds({
                left: leftMargin,
                right: rect.width - rightMargin,
                top: topMargin,
                bottom: rect.height - bottomMargin,
                xMin: 0,
                xMax: T,
                yMin: yMin - yPadding,
                yMax: yMax + yPadding,
            });
        }
    }, [data, T, yMin, yMax, yPadding]);

    const handleClick = useCallback(
        (e: React.MouseEvent<HTMLDivElement>) => {
            if (!chartBounds || !containerRef.current) return;

            const rect = containerRef.current.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Check if click is within chart area
            if (
                x < chartBounds.left ||
                x > chartBounds.right ||
                y < chartBounds.top ||
                y > chartBounds.bottom
            ) {
                return;
            }

            // Convert pixel coordinates to data coordinates
            const chartWidth = chartBounds.right - chartBounds.left;
            const chartHeight = chartBounds.bottom - chartBounds.top;

            const tValue =
                ((x - chartBounds.left) / chartWidth) *
                (chartBounds.xMax - chartBounds.xMin) +
                chartBounds.xMin;
            const aValue =
                ((chartBounds.bottom - y) / chartHeight) *
                (chartBounds.yMax - chartBounds.yMin) +
                chartBounds.yMin;

            // Ensure within bounds
            const clampedT = Math.max(0, Math.min(T, tValue));

            onAddPoint({ t: clampedT, a: aValue });
        },
        [chartBounds, onAddPoint, T]
    );

    return (
        <div
            ref={containerRef}
            style={{ width: '100%', height: 220, cursor: 'crosshair', position: 'relative' }}
            onClick={handleClick}
        >
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    data={data}
                    margin={{ left: 50, right: 10, top: 10, bottom: 30 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3a" />
                    <XAxis
                        dataKey="t"
                        stroke="#606070"
                        tickFormatter={(v) => v.toFixed(2)}
                        fontSize={11}
                        domain={[0, T]}
                        type="number"
                    />
                    <YAxis
                        stroke="#606070"
                        tickFormatter={(v) => v.toFixed(2)}
                        fontSize={11}
                        domain={[yMin - yPadding, yMax + yPadding]}
                    />
                    <Tooltip
                        contentStyle={{
                            background: '#16161f',
                            border: '1px solid #2a2a3a',
                            borderRadius: '8px',
                        }}
                        labelFormatter={(v) => `t = ${Number(v).toFixed(3)} s`}
                        formatter={(v) => [`${Number(v).toFixed(4)} ${yLabel}`, '']}
                    />
                    <Line
                        type="monotone"
                        dataKey="value"
                        stroke={color}
                        strokeWidth={2}
                        dot={false}
                        activeDot={{ r: 4, fill: color }}
                    />
                    {points.map((p, i) => (
                        <ReferenceDot
                            key={i}
                            x={p.t}
                            y={p.a}
                            r={8}
                            fill="#ef4444"
                            stroke="#ffffff"
                            strokeWidth={2}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
            <div
                style={{
                    position: 'absolute',
                    bottom: 5,
                    left: '50%',
                    transform: 'translateX(-50%)',
                    fontSize: '0.7rem',
                    color: '#606070',
                }}
            >
                Haz clic en cualquier punto para añadir un objetivo
            </div>
        </div>
    );
}
