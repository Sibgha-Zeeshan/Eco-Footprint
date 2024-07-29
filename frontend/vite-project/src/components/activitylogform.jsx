// import React, { useState } from "react";
// import {
//   TextField,
//   Button,
//   MenuItem,
//   Container,
//   Typography,
// } from "@mui/material";
// import axios from "axios";

// const ActivityLogForm = () => {
//   const [activityType, setActivityType] = useState("");
//   const [activityValue, setActivityValue] = useState("");
//   const [date, setDate] = useState("");

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     const newActivityLog = {
//       activity_type: activityType,
//       activity_value: parseFloat(activityValue),
//       date: new Date(date).toISOString(), // Ensure date is in ISO 8601 format
//     };

//     try {
//       const response = await axios.post(
//         "http://localhost:8000/api/activity-logs/",
//         newActivityLog
//       );
//       console.log("Activity log created:", response.data);
//       // Clear the form
//       setActivityType("");
//       setActivityValue("");
//       setDate("");
//     } catch (error) {
//       console.error("Error creating activity log:", error);
//     }
//   };

//   return (
//     <Container component="main" maxWidth="xs">
//       <Typography component="h1" variant="h5">
//         Log Activity
//       </Typography>
//       <form onSubmit={handleSubmit} noValidate>
//         <TextField
//           variant="outlined"
//           margin="normal"
//           required
//           fullWidth
//           id="activityType"
//           label="Activity Type"
//           name="activityType"
//           select
//           value={activityType}
//           onChange={(e) => setActivityType(e.target.value)}
//         >
//           <MenuItem value="car_travel">Car Travel</MenuItem>
//           <MenuItem value="public_transport">Public Transport</MenuItem>
//           <MenuItem value="electricity_usage">Electricity Usage</MenuItem>
//           <MenuItem value="natural_gas_usage">Natural Gas Usage</MenuItem>
//           <MenuItem value="waste_generation">Waste Generation</MenuItem>
//           <MenuItem value="water_usage">Water Usage</MenuItem>
//           <MenuItem value="air_travel">Air Travel</MenuItem>
//           <MenuItem value="food_consumption_meat">
//             Food Consumption (Meat)
//           </MenuItem>
//           <MenuItem value="food_consumption_vegetables">
//             Food Consumption (Vegetables)
//           </MenuItem>
//           <MenuItem value="clothing_purchases">Clothing Purchases</MenuItem>
//         </TextField>
//         <TextField
//           variant="outlined"
//           margin="normal"
//           required
//           fullWidth
//           name="activityValue"
//           label="Activity Value"
//           type="number"
//           id="activityValue"
//           value={activityValue}
//           onChange={(e) => setActivityValue(e.target.value)}
//         />
//         <TextField
//           variant="outlined"
//           margin="normal"
//           required
//           fullWidth
//           name="date"
//           label="Date"
//           type="datetime-local"
//           id="date"
//           value={date}
//           onChange={(e) => setDate(e.target.value)}
//           InputLabelProps={{
//             shrink: true,
//           }}
//         />
//         <Button type="submit" fullWidth variant="contained" color="primary">
//           Log Activity
//         </Button>
//       </form>
//     </Container>
//   );
// };

// export default ActivityLogForm;
import React, { useState } from "react";
import {
  TextField,
  Button,
  MenuItem,
  Container,
  Typography,
} from "@mui/material";
import axios from "axios";

const ActivityLogForm = () => {
  const [activityType, setActivityType] = useState("");
  const [activityValue, setActivityValue] = useState("");
  const [date, setDate] = useState("");
  const [userId, setUserId] = useState(""); // Add this state to store user ID

  const handleSubmit = async (event) => {
    event.preventDefault();
    const newActivityLog = {
      user_id: parseInt(userId), // Include user ID
      activity_type: activityType,
      activity_value: parseFloat(activityValue),
      date: date,
    };

    try {
      const response = await axios.post(
        "http://localhost:8000/api/activity-logs/",
        newActivityLog
      );
      console.log("Activity log created:", response.data);
      // Clear the form
      setActivityType("");
      setActivityValue("");
      setDate("");
      setUserId(""); // Clear user ID field
    } catch (error) {
      console.error("Error creating activity log:", error);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Typography component="h1" variant="h5">
        Log Activity
      </Typography>
      <form onSubmit={handleSubmit} noValidate>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="userId"
          label="User ID"
          name="userId"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="activityType"
          label="Activity Type"
          name="activityType"
          select
          value={activityType}
          onChange={(e) => setActivityType(e.target.value)}
        >
          <MenuItem value="car_travel">Car Travel</MenuItem>
          <MenuItem value="public_transport">Public Transport</MenuItem>
          <MenuItem value="electricity_usage">Electricity Usage</MenuItem>
          <MenuItem value="natural_gas_usage">Natural Gas Usage</MenuItem>
          <MenuItem value="waste_generation">Waste Generation</MenuItem>
          <MenuItem value="water_usage">Water Usage</MenuItem>
          <MenuItem value="air_travel">Air Travel</MenuItem>
          <MenuItem value="food_consumption_meat">
            Food Consumption (Meat)
          </MenuItem>
          <MenuItem value="food_consumption_vegetables">
            Food Consumption (Vegetables)
          </MenuItem>
          <MenuItem value="clothing_purchases">Clothing Purchases</MenuItem>
        </TextField>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          name="activityValue"
          label="Activity Value"
          type="number"
          id="activityValue"
          value={activityValue}
          onChange={(e) => setActivityValue(e.target.value)}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          name="date"
          label="Date"
          type="datetime-local"
          id="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          InputLabelProps={{
            shrink: true,
          }}
        />
        <Button type="submit" fullWidth variant="contained" color="primary">
          Log Activity
        </Button>
      </form>
    </Container>
  );
};

export default ActivityLogForm;

