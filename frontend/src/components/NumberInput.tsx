import React, { useState, useEffect, useRef } from 'react';

interface NumberInputProps {
    label: string;
    value: number;
    onChange: (value: number) => void;
    min?: number;
    max?: number;
    step?: number;
    unit?: string;
}

export function NumberInput({
    label,
    value,
    onChange,
    min = 0,
    max = 100,
    step = 1,
    unit
}: NumberInputProps) {
    const [localValue, setLocalValue] = useState(String(value));
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        setLocalValue(String(value));
    }, [value]);

    const handleBlur = () => {
        let num = parseFloat(localValue);
        if (isNaN(num)) {
            num = value; // Revert if invalid
        } else {
            // Clamp
            if (min !== undefined && num < min) num = min;
            if (max !== undefined && num > max) num = max;
        }
        setLocalValue(String(num));
        onChange(num);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            inputRef.current?.blur();
        }
    };

    const increment = (e: React.MouseEvent) => {
        e.preventDefault(); // Prevent form submit
        const newValue = Math.min(value + step, max);
        // Fix float precision issues
        const fixed = parseFloat(newValue.toFixed(10));
        onChange(fixed);
    };

    const decrement = (e: React.MouseEvent) => {
        e.preventDefault(); // Prevent form submit
        const newValue = Math.max(value - step, min);
        const fixed = parseFloat(newValue.toFixed(10));
        onChange(fixed);
    };

    const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(e.target.value);
        onChange(val);
    };

    return (
        <div className="number-input-container">
            <div className="number-input-header">
                <label className="number-input-label">{label}</label>
                <div className="number-input-value-display">
                    {value} {unit && <span className="unit">{unit}</span>}
                </div>
            </div>

            <div className="number-input-controls">
                <button
                    className="control-btn"
                    onClick={decrement}
                    type="button"
                    disabled={value <= min}
                >
                    −
                </button>

                <div className="slider-container">
                    <input
                        type="range"
                        min={min}
                        max={max}
                        step={step}
                        value={value}
                        onChange={handleSliderChange}
                        className="range-slider"
                    />
                </div>

                <button
                    className="control-btn"
                    onClick={increment}
                    type="button"
                    disabled={value >= max}
                >
                    +
                </button>

                <input
                    ref={inputRef}
                    type="number"
                    className="direct-input"
                    value={localValue}
                    onChange={(e) => setLocalValue(e.target.value)}
                    onBlur={handleBlur}
                    onKeyDown={handleKeyDown}
                    step={step}
                />
            </div>
        </div>
    );
}
