// src/components/History.js
import React, { useEffect, useState } from 'react';
import api from '../api';

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    api.get('/api/history').then(res => {
      setHistory(res.data);
    });
  }, []);

  return (
    <div>
      <h3>Workout History</h3>
      <ul>
        {history.map((w, i) => (
          <li key={i}>{w.time} — {w.workout}</li>
        ))}
      </ul>
    </div>
  );
}

