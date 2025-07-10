// src/components/RegisterForm.js
import React, { useState } from 'react';
import api from '../api';

export default function RegisterForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/api/register', { email, password });
      setMsg(res.data.msg);
    } catch (err) {
      setMsg(err.response?.data?.msg || 'Error');
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <h3>Register</h3>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button>Register</button>
      <p>{msg}</p>
    </form>
  );
}

