# Building-a-Social-Media-Analytics-Tool
## Description
This project centers on developing a robust social media analytics tool aimed at
delivering in-depth insights into various performance metrics, audience engagement,
and brand sentiment across multiple social media platforms. Utilizing a blend of
advanced data analytics, machine learning algorithms, and natural language processing
(NLP), the tool is designed to capture and assess key performance indicators (KPIs) in
real-time, including metrics such as reach, impressions, likes, shares, and follower
growth. By focusing on these KPIs, the tool enables businesses and marketers to gain
a holistic view of content effectiveness, helping them adapt strategies based on actual
audience behavior and interaction.
One of the tool’s primary features is its capability for sentiment analysis and trend
detection. These capabilities help businesses understand public sentiment toward their
brand and content, while also tracking emerging topics in their industry, allowing for
timely adjustments to content strategies. Additionally, the tool includes keyword
tracking and competitive benchmarking, allowing users to monitor specific industryrelated terms, brands, or products and to compare their performance against
competitors. Customizable dashboards enable users to visualize data in ways that meet
their unique needs, making it easier to interpret complex information and derive
actionable insights.
## System Requirements
## Hardware requirements:
CPU: Intel Core i5 AMD Ryzen 5
GPU: NVIDIA GeForce GTX 1660 or AMD Radeon RX 580
RAM: 8 GB or higher
Storage: Solid-state drive (SSD) with at least 256 GB of storage space
## Hardware requirements:
Operating System: Windows 10 or Linux (Ubuntu, CentOS, or similar) IDE: VSCode
,PyCharm ,Eclipse
SDK: MongoDB
Language:Python
## Program:
## Backend (Node.js + Express)
## 1. `backend/.env`
```
Create a `.env` file in the `backend` directory and add your MongoDB URI:
MONGO_URI=your_mongo_connection_string
PORT=5000
```

### 2. `backend/server.js`
```
---javascript
// server.js
const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const cors = require('cors');
const analyticsRoutes = require('./routes/analytics');
dotenv.config();
const app = express();
app.use(express.json());
app.use(cors());
// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, {
 useNewUrlParser: true,
 useUnifiedTopology: true
})
 .then(() => console.log("MongoDB connected"))
 .catch((error) => console.error("MongoDB connection error:", error));
app.use('/api/analytics', analyticsRoutes);
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```
## 3. `backend/models/AnalyticsData.js`
```
---javascript
// models/AnalyticsData.js
const mongoose = require('mongoose');
const AnalyticsDataSchema = new mongoose.Schema({
 platform: String,
 date: Date,
 followers: Number,
 engagement: Number
});
module.exports = mongoose.model('AnalyticsData', AnalyticsDataSchema);
```
## 4. `backend/routes/analytics.js`
```
---javascript
// routes/analytics.js
const express = require('express');
const router = express.Router();
const AnalyticsData = require('../models/AnalyticsData');
// Get all analytics data
router.get('/', async (req, res) => {
 try {
 const data = await AnalyticsData.find();
 res.json(data);
 } catch (error) {
 res.status(500).json({ message: error.message });
 }
});
// Add new analytics data
router.post('/', async (req, res) => {
 const newData = new AnalyticsData(req.body);
 try {
 const savedData = await newData.save();
 res.json(savedData);
 } catch (error) {
 res.status(400).json({ message: error.message });
 }
});
module.exports = router;
```
 ## Install Backend Dependencies
In the `backend` folder, run:
```bash
npm install express mongoose dotenv cors axios
```
## Start the Backend Server
```bash
node server.js
```
## Frontend (React.js)
## Initialize React App
Create the React app in the `frontend` folder and install Axios:
```bash
npx create-react-app frontend
cd frontend
npm install axios
```
## 1. `frontend/src/App.js`
```javascript
// src/App.js
import React from 'react';
import Analytics from './components/Analytics';
function App() {
 return (
 <div className="App">
 <h1>Social Media Analytics</h1>
 <Analytics />
 </div>
 );
}
export default App;
```
## 2. `frontend/src/components/Analytics.js`
```javascript
// src/components/Analytics.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
function Analytics() {
 const [analyticsData, setAnalyticsData] = useState([]);
 useEffect(() => {
 const fetchData = async () => {
try {
 const response = await axios.get('http://localhost:5000/api/analytics');
 setAnalyticsData(response.data);
 } catch (error) {
 console.error('Error fetching data:', error);
 }
 };
 fetchData();
 }, []);
 return (
 <div>
 <h2>Analytics Data</h2>
 {analyticsData.length > 0 ? (
 <table>
 <thead>
 <tr>
 <th>Platform</th>
 <th>Date</th>
 <th>Followers</th>
<th>Engagement</th>
 </tr>
 </thead>
 <tbody>
 {analyticsData.map((data) => (
 <tr key={data._id}>
 <td>{data.platform}</td>
 <td>{new Date(data.date).toLocaleDateString()}</td>
 <td>{data.followers}</td>
<td>{data.engagement}</td>
 </tr>
 ))}
 </tbody>
 </table>
 ) : (
 <p>No data available</p>
 )}
 </div>
 );
}
export default Analytics;
```
## Start the React App
In the `frontend` folder, run:
```bash
npm start
```
## Output

## Backend

![image](https://github.com/user-attachments/assets/2d0312af-6376-4d00-b832-b391785d919d)

![image](https://github.com/user-attachments/assets/725d7da4-24a2-455c-9839-226bc8181207)

## Frontend

![image](https://github.com/user-attachments/assets/836aff4e-154c-4dfd-a40f-aedc0f6f87ab)

![image](https://github.com/user-attachments/assets/bfb4ce4e-196b-40a6-88b9-e3456b5ad8f9)


