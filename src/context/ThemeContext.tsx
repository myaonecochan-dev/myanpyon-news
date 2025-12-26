import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
    theme: Theme;
    setTheme: (theme: Theme) => void;
    resolvedTheme: 'light' | 'dark'; // The actual active theme
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [theme, setTheme] = useState<Theme>(() => {
        // Restore preference from localStorage
        const saved = localStorage.getItem('theme-preference');
        return (saved as Theme) || 'system';
    });

    const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

    useEffect(() => {
        // Logic to determine actual theme
        const root = window.document.documentElement;
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)');

        const applyTheme = () => {
            let activeTheme: 'light' | 'dark' = 'light';

            if (theme === 'system') {
                activeTheme = systemDark.matches ? 'dark' : 'light';
            } else {
                activeTheme = theme;
            }

            setResolvedTheme(activeTheme);

            if (activeTheme === 'dark') {
                root.setAttribute('data-theme', 'dark');
            } else {
                root.removeAttribute('data-theme');
            }
        };

        applyTheme();

        // Listen for system changes if mode is 'system'
        systemDark.addEventListener('change', applyTheme);
        return () => systemDark.removeEventListener('change', applyTheme);
    }, [theme]);

    const handleSetTheme = (newTheme: Theme) => {
        setTheme(newTheme);
        localStorage.setItem('theme-preference', newTheme);
    };

    return (
        <ThemeContext.Provider value={{ theme, setTheme: handleSetTheme, resolvedTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};
