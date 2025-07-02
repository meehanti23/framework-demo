import logo from './logo.svg';
import React, { useState } from 'react';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [result, setResult] = useState(null);

  const fetchNameStats = async (event) => {
    // Prevent default form submission behavior (page refresh)
    event.preventDefault();
    
    // Don't proceed if name is empty or just whitespace
    if (!name.trim()) return;
    
    try {
      // Make POST request to our Express backend
      const response = await fetch('http://localhost:3001/api/analyze-name', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Tell server we're sending JSON
        },
        body: JSON.stringify({ name: name.trim() }), // Convert object to JSON string
      });

      // Check if the response was successful
      if (!response.ok) {
        throw new Error('Failed to analyze name');
      }

      // Parse JSON response and update state
      const data = await response.json();
      setResult(data);
      
    } catch (error) {
      // Handle any errors that occurred during the API call
      console.error('Error:', error);
      alert('Failed to analyze name. Please try again.');
    }
  };


  return (
    <div className="App">
      <header className="App-header">
        <h1>Name Analysis Tool</h1>
        <p>Discover insights about any name</p>
      </header>
      <main className="main-content">
        <div className="form-container">
          <form onSubmit={fetchNameStats} className="name-form">
            <div className="input-group">
              <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placehoder="Enter a name"
              className="name-input"
              />
              <button 
              type="submit"
              className="analyze-btn"
              >
                Analyze Name
              </button>
            </div>
          </form>

          {result && (
            <div className="results-container">
              <h2>Analysis Results for "{result.name}"</h2>
              
              {/* Grid layout for result cards */}
              <div className="results-grid">
                {/* Age prediction card */}
                <div className="result-card">
                  <h3>🎂 Predicted Age</h3>
                  <p className="result-value">
                    {/* Conditional rendering based on whether age data exists */}
                    {result.age ? `${result.age} years old` : 'No prediction available'}
                  </p>
                </div>

                {/* Gender prediction card */}
                <div className="result-card">
                  <h3>👤 Predicted Gender</h3>
                  <p className="result-value">
                    {/* Capitalize first letter of gender if it exists */}
                    {result.gender ? 
                      `${result.gender.charAt(0).toUpperCase() + result.gender.slice(1)}` : 
                      'No prediction available'
                    }
                  </p>
                  {/* Show confidence percentage if available */}
                  {result.probability && (
                    <p className="confidence">
                      Confidence: {(result.probability * 100).toFixed(1)}%
                    </p>
                  )}
                </div>

                {/* Nationality prediction card */}
                <div className="result-card">
                  <h3>🌍 Likely Nationality</h3>
                  <p className="result-value">
                    {/* Show first country if available, otherwise show 'Unknown' */}
                    {result.countries && result.countries.length > 0 
                      ? result.countries[0].country_id 
                      : 'Unknown'
                    }
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
