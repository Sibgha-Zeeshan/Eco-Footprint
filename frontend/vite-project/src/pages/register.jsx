import React, { useState } from "react";
import { Container, TextField, Button, Typography, Box } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../services/app";
import GoogleIcon from "@mui/icons-material/Google"; // Optional: Google icon for the button


const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await registerUser({ username, email, password });
      navigate("/login");
    } catch (error) {
      console.error(
        "Registration failed:",
        error.response ? error.response.data : error.message
      );
    }
  };

  const handleGoogleLogin = () => {
    const clientId =
      "140789581112-1mf5v3c4k2gcvv7n61tc9cfr57cfrb5q.apps.googleusercontent.com"; // Ensure this matches the client ID from Google
    const scope = "openid email profile"; // Required scopes
    const redirectUri = "http://localhost:8000/auth/callback"; // Must match the redirect URI registered in Google Console
    const authUri = "https://accounts.google.com/o/oauth2/auth";
    const responseType = "code"; // This should be 'code' for OAuth 2.0
    const state = "RANDOM_STATE_STRING"; // Optional, but recommended
    const nonce = "RANDOM_NONCE_STRING"; // Optional, helps prevent replay attacks
    const accessType = "offline"; // If you need a refresh token

    const googleAuthUrl = `${authUri}?client_id=${clientId}&redirect_uri=${encodeURIComponent(
      redirectUri
    )}&response_type=${responseType}&scope=${encodeURIComponent(
      scope
    )}&state=${state}&nonce=${nonce}&access_type=${accessType}`;

    window.location.href = googleAuthUrl;
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
        <Typography variant="subtitle1" align="center">
          OR
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          fullWidth
          startIcon={<GoogleIcon />} // Optional: Add Google icon
          onClick={handleGoogleLogin}
        >
          Register with Google
        </Button>
      </Box>
    </Container>
  );
};

export default Register;
