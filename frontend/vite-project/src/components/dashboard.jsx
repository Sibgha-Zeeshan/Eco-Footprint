import React, { useEffect, useState } from "react";
import {
  getUserActivities,
  getUserReports,
  getUserGoals,
  getUserTips,
  getUserAchievements,
} from "../services/api";

const Dashboard = () => {
  const [activities, setActivities] = useState([]);
  const [reports, setReports] = useState([]);
  const [goals, setGoals] = useState([]);
  const [tips, setTips] = useState([]);
  const [achievements, setAchievements] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const userId = 1; // replace with actual user ID
      const activitiesData = await getUserActivities(userId);
      const reportsData = await getUserReports(userId);
      const goalsData = await getUserGoals(userId);
      const tipsData = await getUserTips(userId);
      const achievementsData = await getUserAchievements(userId);

      setActivities(activitiesData.data);
      setReports(reportsData.data);
      setGoals(goalsData.data);
      setTips(tipsData.data);
      setAchievements(achievementsData.data);
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <div>
        <h2>Activities</h2>
        {activities.map((activity) => (
          <div key={activity.id}>
            {activity.activity_type}: {activity.activity_value}
          </div>
        ))}
      </div>
      <div>
        <h2>Reports</h2>
        {reports.map((report) => (
          <div key={report.id}>{report.report_data}</div>
        ))}
      </div>
      <div>
        <h2>Goals</h2>
        {goals.map((goal) => (
          <div key={goal.id}>
            {goal.target_reduction} by {goal.deadline}
          </div>
        ))}
      </div>
      <div>
        <h2>Tips</h2>
        {tips.map((tip) => (
          <div key={tip.id}>{tip.tip_text}</div>
        ))}
      </div>
      <div>
        <h2>Achievements</h2>
        {achievements.map((achievement) => (
          <div key={achievement.id}>
            {achievement.achievement_type} on {achievement.date_awarded}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
