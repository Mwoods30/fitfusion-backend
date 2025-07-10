import React, { useContext, useState } from 'react';
import { AuthProvider, AuthContext } from './AuthContext';
import RegisterForm from './components/RegisterForm';
import LoginForm from './components/LoginForm';
import WorkoutForm from './components/WorkoutForm';
import History from './components/History';

function Main() {
  const { token, logout } = useContext(AuthContext);
  const [showRegister, setShowRegister] = useState(null); // null = no choice yet

  if (token) {
    return (
      <>
        <button onClick={logout} className="mb-4 px-4 py-2 bg-red-500 text-white rounded">
          Logout
        </button>
        <WorkoutForm />
        <History />
      </>
    );
  }

  if (showRegister === null) {
    return (
      <div className="flex gap-4 justify-center">
        <button
          onClick={() => setShowRegister(true)}
          className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Register
        </button>
        <button
          onClick={() => setShowRegister(false)}
          className="px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Login
        </button>
      </div>
    );
  }

  return (
    <>
      {showRegister ? <RegisterForm /> : <LoginForm />}
      <button
        onClick={() => setShowRegister(null)}
        className="mt-4 px-4 py-2 border rounded hover:bg-gray-100"
      >
        Back
      </button>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <div className="p-6 max-w-lg mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">🏋️‍♀️ FitFusion</h1>
        <Main />
      </div>
    </AuthProvider>
  );
}

export default App;

