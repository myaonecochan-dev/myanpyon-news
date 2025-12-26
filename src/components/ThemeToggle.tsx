import { useTheme } from '../context/ThemeContext';
import './ThemeToggle.css';

export const ThemeToggle = () => {
    const { theme, setTheme, resolvedTheme } = useTheme();

    // Toggle logic: System -> Light -> Dark -> System (Loop) or just Light <-> Dark?
    // User requested "System match & Toggle button". 
    // Let's make it a simple toggle: If currently Dark (system or manual) -> Light. If Light -> Dark.
    // But we need to handle "System" state nicely.
    // Simple approach: Click toggles between Light and Dark manually.
    // Long press or special UI to reset to system? 
    // Let's keep it simple: Icon shows current state. Click flips state to opposite of current resolved.

    const toggleTheme = () => {
        const next = resolvedTheme === 'dark' ? 'light' : 'dark';
        setTheme(next);
    };

    return (
        <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Current theme is ${resolvedTheme}. Click to switch to ${resolvedTheme === 'dark' ? 'light' : 'dark'}.`}
            title={`Theme: ${theme === 'system' ? 'System (Auto)' : theme}`}
        >
            {resolvedTheme === 'dark' ? '🌙' : '☀️'}
        </button>
    );
};
