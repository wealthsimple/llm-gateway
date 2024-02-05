import React from 'react';
import { useTheme } from '../ThemeProvider';

export const ThemeToggleButton: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const ThemeIcon = () => {
    return <span>{theme === 'light' ? '🌞' : '🌜'}</span>;
  };

  return (
    <button onClick={toggleTheme} className="theme-toggle-button">
      <ThemeIcon />
    </button>
  );
};
