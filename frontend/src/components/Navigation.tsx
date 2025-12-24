import { useLang, useTheme } from '../contexts';
import { getTranslation } from '../translations';

interface NavigationProps {
    currentPage: string;
    onNavigate: (page: string) => void;
}

export function Navigation({ currentPage, onNavigate }: NavigationProps) {
    const { theme, toggleTheme } = useTheme();
    const { lang, toggleLang } = useLang();
    const t = getTranslation(lang);

    const navItems = [
        { id: 'home', label: t.nav.home },
        { id: 'docs', label: t.nav.docs },
        { id: 'analysis', label: t.nav.analysis },
        { id: 'video', label: t.nav.video },
    ];

    return (
        <nav className="navigation">
            <div className="nav-brand" onClick={() => onNavigate('home')}>
                <img src="/img/logo.png" alt="Rowing Dynamics Logo" className="nav-logo-img" />
                <span className="nav-title">RowLab</span>
            </div>

            <input type="checkbox" id="nav-toggle" className="nav-toggle" />
            <label htmlFor="nav-toggle" className="nav-toggle-label">
                <span></span>
                <span></span>
                <span></span>
            </label>

            <div className="nav-menu">
                <ul className="nav-links">
                    {navItems.map((item) => (
                        <li key={item.id}>
                            <a
                                href={`#/${item.id === 'home' ? '' : item.id}`}
                                className={currentPage === item.id ? 'active' : ''}
                                onClick={(e) => {
                                    e.preventDefault();
                                    onNavigate(item.id);
                                }}
                            >
                                {item.label}
                            </a>
                        </li>
                    ))}
                </ul>

                <div className="nav-controls">
                    <button
                        className="nav-btn"
                        onClick={toggleTheme}
                        title={t.nav.theme}
                        aria-label={t.nav.theme}
                    >
                        {theme === 'dark' ? '☀️' : '🌙'}
                    </button>
                    <button
                        className="nav-btn"
                        onClick={toggleLang}
                        title={t.nav.language}
                        aria-label={t.nav.language}
                    >
                        {lang.toUpperCase()}
                    </button>
                </div>
            </div>
        </nav>
    );
}
