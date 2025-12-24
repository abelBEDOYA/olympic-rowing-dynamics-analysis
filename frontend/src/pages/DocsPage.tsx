import { useLang } from '../contexts';
import { getTranslation } from '../translations';
import siteConfig from '../config';
import { Latex } from '../Latex';

export function DocsPage() {
    const { lang } = useLang();
    const t = getTranslation(lang);

    return (
        <div className="docs-page">
            <header className="page-header">
                <h1>{t.docs.title}</h1>
                <p>{t.docs.subtitle}</p>
            </header>

            <section className="docs-section">
                <h2>{t.docs.mathFoundations}</h2>

                <article className="docs-article">
                    <h3>{t.docs.systemDynamics}</h3>
                    <p>
                        {lang === 'es'
                            ? 'El sistema se compone de un remero de masa m, un barco de masa M, y el rozamiento con el agua caracterizado por k.'
                            : 'The system consists of a rower of mass m, a boat of mass M, and water friction characterized by k.'}
                    </p>
                    <div className="math-block">
                        <Latex math={`m_r \\ddot{x}_r = F_{int}(x_r, x_b)`} displayMode />
                        <Latex math={`m_b \\ddot{x}_b = -F_{int}(x_r, x_b) - k \\dot{x}_b`} displayMode />
                    </div>
                </article>

                <article className="docs-article">
                    <h3>{t.docs.polynomialBoundary}</h3>
                    <p>
                        {lang === 'es'
                            ? 'Se construye un polinomio p(t) de grado n ≥ 3 que cumple las condiciones de contorno:'
                            : 'A polynomial p(t) of degree n ≥ 3 is constructed satisfying the boundary conditions:'}
                    </p>
                    <div className="math-block">
                        <Latex math={`p(0) = 0, \\quad p(T) = L, \\quad p'(0) = 0, \\quad p'(T) = 0`} displayMode />
                    </div>
                    <p>
                        {lang === 'es'
                            ? 'Los coeficientes a₂ y a₃ se derivan automáticamente:'
                            : 'Coefficients a₂ and a₃ are derived automatically:'}
                    </p>
                    <div className="math-block">
                        <Latex math={`a_2 = \\frac{3L}{T^2} + \\sum_{k=4}^{n} (k - 3)a_k T^{k-2}`} displayMode />
                        <Latex math={`a_3 = -\\frac{2L}{T^3} - \\sum_{k=4}^{n} (k - 2)a_k T^{k-3}`} displayMode />
                    </div>
                </article>
            </section>

            {siteConfig.docs.length > 0 && (
                <section className="docs-section">
                    <h2>PDF Documents</h2>
                    <div className="docs-list">
                        {siteConfig.docs.map((doc, i) => (
                            <a key={i} href={doc.file} target="_blank" rel="noopener noreferrer" className="doc-card">
                                <div className="doc-icon">📄</div>
                                <div className="doc-info">
                                    <h4>{doc.title}</h4>
                                    <p>{doc.description}</p>
                                </div>
                                <span className="doc-action">{t.docs.downloadPdf}</span>
                            </a>
                        ))}
                    </div>
                </section>
            )}
        </div>
    );
}
