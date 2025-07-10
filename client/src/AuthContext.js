// src/AuthContext.js
import { createContext, useState } from 'react';
import { setAuthToken } from './api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  const login = (newToken) => {
    localStorage.setItem('token', newToken);
    setAuthToken(newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuthToken(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

