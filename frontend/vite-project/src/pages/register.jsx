// src/pages/Register.js
import React, { useState } from "react";
import { Container, TextField, Button, Typography, Box } from "@mui/material";
import { Link } from "react-router-dom";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission, e.g., send data to backend
    console.log("Username:", username);
    console.log("Email:", email);
    console.log("Password:", password);
  };

  return (
    <Container maxWidth="sm">
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ mt: 8, display: "flex", flexDirection: "column", gap: 2 }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Register
        </Typography>
        <TextField
          label="Username"
          variant="outlined"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          fullWidth
        />
        <TextField
          label="Email"
          variant="outlined"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          fullWidth
        />
        <TextField
          label="Password"
          variant="outlined"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          fullWidth
        />
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Register
        </Button>
        <Button
          component={Link}
          to="/login"
          variant="outlined"
          color="secondary"
          fullWidth
        >
          Already have an account? Login
        </Button>
      </Box>
    </Container>
  );
};

export default Register;
