// src/components/WorkoutForm.js
import React, { useState } from 'react';
import api from '../api';

export default function WorkoutForm() {
  const [time, setTime] = useState('');
  const [goal, setGoal] = useState('');
  const [equipment, setEquipment] = useState('');
  const [plan, setPlan] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await api.post('/api/generate', { time, goal, equipment });
    setPlan(res.data.workout);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Generate Workout</h3>
      <input placeholder="Time (minutes)" value={time} onChange={e => setTime(e.target.value)} />
      <input placeholder="Goal (e.g. cardio)" value={goal} onChange={e => setGoal(e.target.value)} />
      <input placeholder="Equipment" value={equipment} onChange={e => setEquipment(e.target.value)} />
      <button>Generate</button>
      {plan && <p><strong>Plan:</strong> {plan}</p>}
    </form>
  );
}
