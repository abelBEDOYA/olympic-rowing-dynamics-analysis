// Translations for Spanish and English

export type Language = 'es' | 'en';

export const translations = {
    es: {
        // Navigation
        nav: {
            home: 'Inicio',
            docs: 'Documentación',
            analysis: 'Análisis',
            theme: 'Tema',
            language: 'Idioma',
            video: 'Video AI',
        },
        // Video Analysis page
        videoAnalysis: {
            title: 'Análisis de Eficiencia con IA',
            subtitle: 'Evaluación biomecánica mediante visión artificial',
            description: 'Sube un video de tu sesión de remo para analizar tu técnica. Nuestro modelo de visión artificial procesará la secuencia para evaluar la eficiencia de tu palada, detectar asimetrías y calcular métricas de potencia.',
            uploadTitle: 'Sube tu video',
            uploadText: 'Arrastra y suelta tu archivo aquí, o haz clic para seleccionar',
            supportedFormats: 'Formatos soportados: MP4, MOV, AVI (Max 50MB)',
            analyzing: 'Procesando video...',
            analyzeBtn: 'Analizar Video',
            demoNote: 'Nota: Esta es una demostración de la interfaz. La conexión con el motor de IA se implementará próximamente.',
        },
        // Home page
        home: {
            title: 'RowLab',
            subtitle: 'Simulador interactivo de dinámica de remo olímpico',
            description: 'Este proyecto modela y simula el sistema físico unidimensional remero–barco–agua durante la fase aérea de la modalidad de remo de banco móvil. Permite estudiar la dinámica del conjunto controlando la cinemática del remero, ofreciendo métricas detalladas de eficiencia, potencia perdida y cinemática del barco.',
            cta: 'Comenzar Análisis',
            viewDocs: 'Ver Documentación',
            madeBy: 'Desarrollado por',
        },
        // Docs page
        docs: {
            title: 'Documentación',
            subtitle: 'Referencias bibliográficas y documentación técnica',
            mathFoundations: 'Fundamentos Matemáticos',
            systemDynamics: 'Dinámica del Sistema',
            polynomialBoundary: 'Polinomio con Condiciones de Contorno',
            downloadPdf: 'Descargar PDF',
        },
        // Analysis page
        analysis: {
            title: 'Análisis de Dinámica',
            parameters: 'Parámetros',
            rowerMass: 'Masa Remero (m)',
            boatMass: 'Masa Barco (M)',
            displacement: 'Desplazamiento (L)',
            duration: 'Duración (T)',
            waterDensity: 'Densidad Agua (ρ)',
            crossSection: 'Área Transversal (S)',
            dragCoeff: 'Coef. Arrastre (Cd)',
            initialVelocity: 'Velocidad Inicial (y₀\')',
            polyDegree: 'Grado Polinomio',
            calculate: 'Calcular',
            calculating: 'Calculando...',
            results: 'Resultados',
            initialEnergy: 'Energía Inicial',
            finalEnergy: 'Energía Final',
            systemDeltaE: 'ΔE Sistema',
            rowerEnergy: 'E Remero',
            finalPosition: 'Posición Final',
            finalVelocity: 'Velocidad Final',
            deltaV: 'ΔV',
            fittingPoints: 'Puntos de Ajuste',
            clickToAdd: 'Haz clic en el gráfico de aceleración para añadir puntos',
            clear: 'Limpiar',
            fitPolynomial: 'Ajustar Polinomio',
            selectPointsError: 'Selecciona puntos en el gráfico de aceleración',
            // Charts
            rowerPosition: 'Posición Remero',
            rowerVelocity: 'Velocidad Remero',
            rowerAcceleration: 'Aceleración Remero',
            boatPosition: 'Posición Barco',
            boatVelocity: 'Velocidad Barco',
            boatAcceleration: 'Aceleración Barco',
            interactive: 'Interactivo',
            emptyState: 'Configura los parámetros y pulsa Calcular para visualizar la simulación.',
        },
        // Units
        units: {
            kg: 'kg',
            m: 'm',
            s: 's',
            mps: 'm/s',
            mps2: 'm/s²',
            j: 'J',
        },
    },
    en: {
        // Navigation
        nav: {
            home: 'Home',
            docs: 'Documentation',
            analysis: 'Analysis',
            theme: 'Theme',
            language: 'Language',
            video: 'Video AI',
        },
        // Video Analysis page
        videoAnalysis: {
            title: 'AI Efficiency Analysis',
            subtitle: 'Biomechanical evaluation using computer vision',
            description: 'Upload a video of your rowing session to analyze your technique. Our computer vision model will process the sequence to evaluate your stroke efficiency, detect asymmetries, and calculate power metrics.',
            uploadTitle: 'Upload your video',
            uploadText: 'Drag and drop your file here, or click to select',
            supportedFormats: 'Supported formats: MP4, MOV, AVI (Max 50MB)',
            analyzing: 'Processing video...',
            analyzeBtn: 'Analyze Video',
            demoNote: 'Note: This is an interface demo. Connection to the AI engine will be implemented soon.',
        },
        // Home page
        home: {
            title: 'RowLab',
            subtitle: 'Interactive Olympic rowing dynamics simulator',
            description: 'This project models and simulates the one-dimensional rower–boat–water physical system during the aerial phase of sliding seat rowing. It allows studying the system dynamics by controlling the rower kinematics, offering detailed metrics on efficiency, power loss, and boat kinematics.',
            cta: 'Start Analysis',
            viewDocs: 'View Documentation',
            madeBy: 'Developed by',
        },
        // Docs page
        docs: {
            title: 'Documentation',
            subtitle: 'Bibliographic references and technical documentation',
            mathFoundations: 'Mathematical Foundations',
            systemDynamics: 'System Dynamics',
            polynomialBoundary: 'Polynomial with Boundary Conditions',
            downloadPdf: 'Download PDF',
        },
        // Analysis page
        analysis: {
            title: 'Dynamics Analysis',
            parameters: 'Parameters',
            rowerMass: 'Rower Mass (m)',
            boatMass: 'Boat Mass (M)',
            displacement: 'Displacement (L)',
            duration: 'Duration (T)',
            waterDensity: 'Water Density (ρ)',
            crossSection: 'Cross Section (S)',
            dragCoeff: 'Drag Coeff. (Cd)',
            initialVelocity: 'Initial Velocity (y₀\')',
            polyDegree: 'Polynomial Degree',
            calculate: 'Calculate',
            calculating: 'Calculating...',
            results: 'Results',
            initialEnergy: 'Initial Energy',
            finalEnergy: 'Final Energy',
            systemDeltaE: 'ΔE System',
            rowerEnergy: 'Rower Energy',
            finalPosition: 'Final Position',
            finalVelocity: 'Final Velocity',
            deltaV: 'ΔV',
            fittingPoints: 'Fitting Points',
            clickToAdd: 'Click on the acceleration chart to add points',
            clear: 'Clear',
            fitPolynomial: 'Fit Polynomial',
            selectPointsError: 'Select points on the acceleration chart',
            // Charts
            rowerPosition: 'Rower Position',
            rowerVelocity: 'Rower Velocity',
            rowerAcceleration: 'Rower Acceleration',
            boatPosition: 'Boat Position',
            boatVelocity: 'Boat Velocity',
            boatAcceleration: 'Boat Acceleration',
            interactive: 'Interactive',
            emptyState: 'Configure parameters and click Calculate to visualize the simulation.',
        },
        // Units
        units: {
            kg: 'kg',
            m: 'm',
            s: 's',
            mps: 'm/s',
            mps2: 'm/s²',
            j: 'J',
        },
    },
};

export const getTranslation = (lang: Language) => translations[lang];

export default translations;
