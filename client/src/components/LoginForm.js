// src/components/LoginForm.js
import React, { useState, useContext } from 'react';
import api, { setAuthToken } from '../api';
import { AuthContext } from '../AuthContext';

export default function LoginForm() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const res = await api.post('/api/login', 
      { email, password },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    login(res.data.access_token);
  } catch (err) {
    console.error(err);  // Log the full error
    setMsg('Login failed');
  }
};

  return (
    <form onSubmit={handleLogin}>
      <h3>Login</h3>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button>Login</button>
      <p>{msg}</p>
    </form>
  );
}
	
