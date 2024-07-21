// For making APIs to interact with backend
import axios from "axios";

// Frontend themography
import { createTheme } from "@mui/material";


const api = axios.create({
  baseURL: "http://localhost:5173/api",
});

export const registerUser = (userData) => api.post("/users/", userData);
export const loginUser = (credentials) => api.post("/auth/login/", credentials);
export const getUserActivities = (userId) => api.get(`/users/${userId}/activities`);
export const createUserActivity = (userId, activityData) => api.post(`/users/${userId}/activities`, activityData);
export const getUserReports = (userId) => api.get(`/users/${userId}/reports`);
export const createUserGoal = (userId, goalData) => api.post(`/users/${userId}/goals`, goalData);
export const getUserTips = (userId) => api.get(`/users/${userId}/tips`);
export const getUserAchievements = (userId) => api.get(`/users/${userId}/achievements`);



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
