import { useState, useRef } from 'react';
import { useLang } from '../contexts';
import { getTranslation } from '../translations';

export function VideoAnalysisPage() {
    const { lang } = useLang();
    const t = getTranslation(lang);
    const [file, setFile] = useState<File | null>(null);
    const [analyzing, setAnalyzing] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const handleAnalyze = () => {
        if (!file) return;
        setAnalyzing(true);
        // Mock analysis delay
        setTimeout(() => {
            setAnalyzing(false);
            alert(t.videoAnalysis.demoNote);
        }, 2000);
    };

    return (
        <div className="video-page">
            <header className="page-header">
                <h1>{t.videoAnalysis.title}</h1>
                <p>{t.videoAnalysis.subtitle}</p>
            </header>

            <div className="video-content">
                <div className="video-description">
                    <p>{t.videoAnalysis.description}</p>
                </div>

                <div
                    className={`upload-zone ${file ? 'has-file' : ''}`}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        accept="video/*"
                        style={{ display: 'none' }}
                    />

                    {file ? (
                        <div className="file-info">
                            <span className="file-icon">🎬</span>
                            <span className="file-name">{file.name}</span>
                            <span className="file-size">{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
                        </div>
                    ) : (
                        <>
                            <div className="upload-icon">☁️</div>
                            <h3>{t.videoAnalysis.uploadTitle}</h3>
                            <p>{t.videoAnalysis.uploadText}</p>
                            <span className="supported-formats">{t.videoAnalysis.supportedFormats}</span>
                        </>
                    )}
                </div>

                <div className="actions">
                    <button
                        className="btn btn-primary btn-lg"
                        disabled={!file || analyzing}
                        onClick={(e) => {
                            e.stopPropagation();
                            handleAnalyze();
                        }}
                    >
                        {analyzing ? t.videoAnalysis.analyzing : t.videoAnalysis.analyzeBtn}
                    </button>
                </div>
            </div>
        </div>
    );
}
