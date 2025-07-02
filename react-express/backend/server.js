const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Random dog image endpoint
app.get('/api/random-dog', async (req, res) => {
  try {
    const response = await axios.get('https://dog.ceo/api/breeds/image/random');
    res.json({ imageUrl: response.data.message });
  } catch (error) {
    console.error('Error fetching dog image:', error);
    res.status(500).json({ error: 'Failed to fetch dog image' });
  }
});

app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
});