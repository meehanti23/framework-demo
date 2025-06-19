const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Name analysis endpoint
app.post('/api/analyze-name', async (req, res) => {
  try {
    const { name } = req.body;
    
    if (!name) {
      return res.status(400).json({ error: 'Name is required' });
    }

    // Make parallel API calls
    const [ageResponse, genderResponse, nationalityResponse] = await Promise.all([
      axios.get(`https://api.agify.io?name=${name}`),
      axios.get(`https://api.genderize.io?name=${name}`),
      axios.get(`https://api.nationalize.io?name=${name}`)
    ]);

    const result = {
      name: name,
      age: ageResponse.data.age,
      gender: genderResponse.data.gender,
      probability: genderResponse.data.probability,
      countries: nationalityResponse.data.country || []
    };

    res.json(result);
  } catch (error) {
    console.error('Error analyzing name:', error);
    res.status(500).json({ error: 'Failed to analyze name' });
  }
});

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