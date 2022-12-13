import './App.css';

import React, { useState, useEffect } from 'react';

export default function App() {
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const fetchPlayerScoreResponse = () => {
    var body = new FormData()
    body.append('color', 'yellow')
    body.append('image', selectedFile)
    console.log(body)
    fetch('http://127.0.0.1:5000/player_detail',{
      method: 'POST',
      body: body
    }).then((response) => response.json())
      .then((json) => {
        console.log(json)
        setData(json)
      })
      .catch((error) => {
        console.error(error);
    });
  };

  return (
    <div>
      <h1>Open up App.js to start working on your app!</h1>
      <div>
        <input type="file" name="file" onChange={(e) => setSelectedFile(e.target.files[0])}/>
        <button onClick={() => fetchPlayerScoreResponse()}> SB </button>
      </div>
      <h1>{data==null ? null : data.score}</h1>
    </div>
  );
}
