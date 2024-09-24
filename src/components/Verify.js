import React, { useState } from 'react';
import axios from 'axios';
import './Verify.css'; // Import the CSS file

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
    <div className="verify-container">
      <h2>Verify Email</h2>
      <form onSubmit={handleVerify} className="verify-form">
        <div className="form-group">
          <label>Verification Token:</label>
          <input
            type="text"
            className="form-input"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            required
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}
        <button type="submit" className="submit-button">Verify</button>
      </form>
    </div>
  );
};

export default Verify;
