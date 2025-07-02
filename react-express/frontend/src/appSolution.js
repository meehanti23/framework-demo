import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [dogImage, setDogImage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch a random dog image
  const fetchRandomDog = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:3001/api/random-dog');
      
      if (!response.ok) {
        throw new Error('Failed to fetch dog image');
      }
      
      const data = await response.json();
      setDogImage(data.imageUrl);
    } catch (err) {
      setError('Error: ' + err.message);
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch a dog image when component mounts
  useEffect(() => {
    fetchRandomDog();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Random Dog Generator</h1>
        
        <div style={{ margin: '20px 0' }}>
          <button 
            onClick={fetchRandomDog} 
            disabled={loading}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Loading...' : 'Get New Dog!'}
          </button>
        </div>

        {error && (
          <div style={{ color: 'red', margin: '10px 0' }}>
            {error}
          </div>
        )}

        {dogImage && !loading && (
          <div style={{ margin: '20px 0' }}>
            <img 
              src={dogImage} 
              alt="Random dog" 
              style={{
                maxWidth: '400px',
                maxHeight: '400px',
                borderRadius: '10px',
                boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
              }}
            />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;