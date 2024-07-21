// src/pages/Login.js
import React, { useState } from "react";
import { Container, TextField, Button, Typography, Box } from "@mui/material";
import { Link } from "react-router-dom";

const Login = () => {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission, e.g., send data to backend
    console.log("Email/Username:", identifier);
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
          Login
        </Typography>
        <TextField
          label="Email or Username"
          variant="outlined"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
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
          Login
        </Button>
        <Button
          component={Link}
          to="/register"
          variant="outlined"
          color="secondary"
          fullWidth
        >
          Don't have an account? Register
        </Button>
      </Box>
    </Container>
  );
};

export default Login;
