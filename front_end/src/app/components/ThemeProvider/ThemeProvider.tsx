import React, { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';

type Theme = 'light' | 'dark'; // Add more theme types if needed

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const defaultState: ThemeContextType = {
  theme: 'light',
  setTheme: (theme: Theme) => {
    console.warn('setTheme was called without a ThemeProvider: ', theme);
  },
};

const ThemeContext = createContext<ThemeContextType>(defaultState);

interface ThemeProviderProps {
  children: ReactNode;
}

export const Theme: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(() => {
    try {
      const localTheme = localStorage.getItem('theme') as Theme;
      return localTheme || 'light';
    } catch (error) {
      console.error('Error accessing localStorage:', error);
      return 'light';
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
    } catch (error) {
      console.error('Error storing theme:', error);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook to use the theme context
export const useTheme = () => useContext(ThemeContext);
