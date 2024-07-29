// For making APIs to interact with backend
import axios from "axios";

// Frontend themography
import { createTheme } from "@mui/material";

// Base API instance
export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/",
});

// Add JWT token to request headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const registerUser = (userData) => api.post("/auth/register", userData);


// export const loginUser = (credentials) => api.post("/auth/login/", credentials);
export const loginUser = (credentials) => {
  const formData = new URLSearchParams();
  formData.append("username", credentials.username);
  formData.append("password", credentials.password);

  return api.post("/auth/login/", formData, {
    headers: {
      "content-type":
        "multipart/form-data; boundary=ebf9f03029db4c2799ae16b5428b06bd",
    },
  });
};
export const getUserActivities = (userId) =>
  api.get(`/users/${userId}/activities`);
export const createUserActivity = (userId, activityData) =>
  api.post(`/users/${userId}/activities`, activityData);
export const getUserReports = (userId) => api.get(`/users/${userId}/reports`);
export const createUserGoal = (userId, goalData) =>
  api.post(`/users/${userId}/goals`, goalData);
export const getUserTips = (userId) => api.get(`/users/${userId}/tips`);
export const getUserAchievements = (userId) =>
  api.get(`/users/${userId}/achievements`);

export const createActivityLog = (activityData) =>
  api.post("/activity-logs/", activityData);


const theme = createTheme({
  palette: {
    primary: {
      main: "#010101", // black color for primary 
      sec: "#fdfdfd" , // white for on dark colors
    },
    secondary: {
      main: "#afafaf", // silver color for secondary
      sec : "#357960", // amazon color for adding background to components
      third : "#45523e", // cabbage pont
      font : "ad5d50" // Matrix
    },
  },
});
export default theme;
