import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { Language } from './translations';

// Theme context
type Theme = 'light' | 'dark';

interface ThemeContextType {
    theme: Theme;
    toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
    const [theme, setTheme] = useState<Theme>(() => {
        const saved = localStorage.getItem('theme');
        return (saved as Theme) || 'dark';
    });

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'));

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

export function useTheme() {
    const context = useContext(ThemeContext);
    if (!context) throw new Error('useTheme must be used within ThemeProvider');
    return context;
}

// Language context
interface LanguageContextType {
    lang: Language;
    toggleLang: () => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [lang, setLang] = useState<Language>(() => {
        const saved = localStorage.getItem('lang');
        return (saved as Language) || 'es';
    });

    useEffect(() => {
        document.documentElement.lang = lang;
        localStorage.setItem('lang', lang);
    }, [lang]);

    const toggleLang = () => setLang((l) => (l === 'es' ? 'en' : 'es'));

    return (
        <LanguageContext.Provider value={{ lang, toggleLang }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLang() {
    const context = useContext(LanguageContext);
    if (!context) throw new Error('useLang must be used within LanguageProvider');
    return context;
}
