// src/components/Verify.js
import React, { useState } from 'react';
import axios from 'axios';

const Verify = () => {
  const [token, setToken] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const handleVerify = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.get(`http://127.0.0.1:8000/users/verify/${token}`);
      console.log(response.data); // Handle the verification success message
      setSuccessMessage('Email verification successful! You can now log in.');
      setError(null);
    } catch (error) {
      setError("Verification failed. Please check the token.");
    }
  };

  return (
    <div>
      <h2>Verify Email</h2>
      <form onSubmit={handleVerify}>
        <div>
          <label>Verification Token:</label>
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
        <button type="submit">Verify</button>
      </form>
    </div>
  );
};

export default Verify;
