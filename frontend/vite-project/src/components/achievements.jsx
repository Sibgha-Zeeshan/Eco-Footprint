import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Container,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Typography,
} from "@mui/material";
import { Delete, Edit } from "@mui/icons-material";

const Achievement = () => {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [achievement, setAchievement] = useState({
    achievement_type: "",
    date_awarded: "",
  });
  const [currentAchievementId, setCurrentAchievementId] = useState(null);

  const fetchAchievements = async () => {
    try {
      const response = await axios.get("/api/achievements");
      setAchievements(response.data.achievements || []);
    } catch (error) {
      console.error("Error fetching achievements:", error);
      setError("Failed to fetch achievements");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setAchievement({ ...achievement, [e.target.name]: e.target.value });
  };

  const handleCreate = async () => {
    try {
      await axios.post("/api/achievements", achievement);
      fetchAchievements();
      setAchievement({ achievement_type: "", date_awarded: "" });
      setOpen(false);
    } catch (error) {
      console.error("Error creating achievement:", error);
      setError("Failed to create achievement");
    }
  };

  const handleUpdate = async () => {
    try {
      await axios.put(`/api/achievements/${currentAchievementId}`, achievement);
      fetchAchievements();
      setAchievement({ achievement_type: "", date_awarded: "" });
      setEditOpen(false);
    } catch (error) {
      console.error("Error updating achievement:", error);
      setError("Failed to update achievement");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/achievements/${id}`);
      fetchAchievements();
    } catch (error) {
      console.error("Error deleting achievement:", error);
      setError("Failed to delete achievement");
    }
  };

  useEffect(() => {
    fetchAchievements();
  }, []);

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Achievements
      </Typography>
      <Button variant="contained" color="primary" onClick={() => setOpen(true)}>
        Add Achievement
      </Button>
      <List>
        {achievements.length > 0 ? (
          achievements.map((ach) => (
            <ListItem key={ach.achievement_id}>
              <ListItemText
                primary={ach.achievement_type}
                secondary={new Date(ach.date_awarded).toLocaleDateString()}
              />
              <IconButton
                edge="end"
                onClick={() => {
                  setCurrentAchievementId(ach.achievement_id);
                  setAchievement({
                    achievement_type: ach.achievement_type,
                    date_awarded: ach.date_awarded,
                  });
                  setEditOpen(true);
                }}
              >
                <Edit />
              </IconButton>
              <IconButton
                edge="end"
                onClick={() => handleDelete(ach.achievement_id)}
              >
                <Delete />
              </IconButton>
            </ListItem>
          ))
        ) : (
          <Typography variant="body1">No achievements found.</Typography>
        )}
      </List>

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Add Achievement</DialogTitle>
        <DialogContent>
          <DialogContentText>
            To add a new achievement, please enter the achievement type and date
            awarded here.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="add_achievement_type"
            name="achievement_type"
            label="Achievement Type"
            type="text"
            fullWidth
            value={achievement.achievement_type}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            id="add_date_awarded"
            name="date_awarded"
            label="Date Awarded"
            type="datetime-local"
            fullWidth
            value={achievement.date_awarded}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleCreate} color="primary">
            Add
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={editOpen} onClose={() => setEditOpen(false)}>
        <DialogTitle>Edit Achievement</DialogTitle>
        <DialogContent>
          <DialogContentText>
            To edit the achievement, please update the achievement type and date
            awarded here.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="edit_achievement_type"
            name="achievement_type"
            label="Achievement Type"
            type="text"
            fullWidth
            value={achievement.achievement_type}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            id="edit_date_awarded"
            name="date_awarded"
            label="Date Awarded"
            type="datetime-local"
            fullWidth
            value={achievement.date_awarded}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditOpen(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleUpdate} color="primary">
            Update
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Achievement;
