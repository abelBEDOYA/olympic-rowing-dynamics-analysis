import { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

interface LatexProps {
    math: string;
    displayMode?: boolean;
}

export function Latex({ math, displayMode = false }: LatexProps) {
    const containerRef = useRef<HTMLSpanElement>(null);

    useEffect(() => {
        if (containerRef.current && math) {
            try {
                katex.render(math, containerRef.current, {
                    throwOnError: false,
                    displayMode,
                });
            } catch (e) {
                if (containerRef.current) {
                    containerRef.current.textContent = math;
                }
            }
        }
    }, [math, displayMode]);

    return <span ref={containerRef} />;
}
