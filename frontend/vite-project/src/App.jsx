import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Register from "./pages/register";
import Login from "./pages/login";
import theme from "./services/app";

const App = () => (
  <ThemeProvider theme={theme}>
    <Router>
      <CssBaseline />
      <Routes>
        {/* Can use the theme provider here */}
        {/* <Route path="/" element={<Home />} /> */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        {/* <Route path="/profile" element={<Profile />} /> */}
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
      </Routes>
    </Router>
  </ThemeProvider>
);

export default App;
