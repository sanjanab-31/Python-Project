const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
const port = 8000;

// Middleware
app.use(express.json());
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: false
}));

// MongoDB connection
const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

// Connect to MongoDB
async function connectDB() {
  try {
    await client.connect();
    console.log('Connected to MongoDB');
    return client.db('rainwater_harvester');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    process.exit(1);
  }
}

// API Routes
app.post('/api/inputs', async (req, res) => {
  try {
    const db = await connectDB();
    const result = await db.collection('user_inputs').insertOne(req.body);
    res.json({ success: true, id: result.insertedId });
  } catch (error) {
    console.error('Error saving inputs:', error);
    res.status(500).json({ error: 'Failed to save inputs' });
  }
});

app.get('/api/results', async (req, res) => {
  try {
    const db = await connectDB();
    const results = await db.collection('results').find({}).toArray();
    res.json(results);
  } catch (error) {
    console.error('Error fetching results:', error);
    res.status(500).json({ error: 'Failed to fetch results' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
