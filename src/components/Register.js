// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Typography, Container, Snackbar } from '@mui/material';
import { Alert } from '@mui/material';
import { motion } from 'framer-motion'; // Import motion
import './Register.css';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/users/register', {
        email,
        password,
        phone_number: phoneNumber,
      });

      setSuccessMessage('Registration successful! Please verify your email.');
      setSnackbarMessage('Registration successful!');
      setOpenSnackbar(true);
    } catch (error) {
      setError('Registration failed. Please check your details.');
      setSnackbarMessage('Registration failed. Please check your details.');
      setOpenSnackbar(true);
    }
  };

  return (
    <Container className="register-container" maxWidth="sm">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Typography variant="h4" gutterBottom align="center">
          Register
        </Typography>
        <form onSubmit={handleRegister} className="register-form">
          <TextField
            label="Email"
            type="email"
            variant="outlined"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="form-input"
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="form-input"
          />
          <TextField
            label="Phone Number (optional)"
            type="text"
            variant="outlined"
            fullWidth
            margin="normal"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            className="form-input"
          />
          {error && <Alert severity="error" className="error-message">{error}</Alert>}
          {successMessage && <Alert severity="success" className="success-message">{successMessage}</Alert>}
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            className="submit-button"
          >
            Register
          </Button>
        </form>
        <Snackbar
          open={openSnackbar}
          autoHideDuration={6000}
          onClose={() => setOpenSnackbar(false)}
        >
          <Alert onClose={() => setOpenSnackbar(false)} severity={error ? 'error' : 'success'}>
            {snackbarMessage}
          </Alert>
        </Snackbar>
      </motion.div>
    </Container>
  );
};

export default Register;
