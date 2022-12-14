import './App.css';
 
import React, { useState, useEffect, useRef } from 'react';
import { Button, Space } from 'antd';
 
export default function App() {
  const canvasRef = useRef();
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
 
  const drawRectangle = () => {
    const context = canvasRef.current.getContext("2d");
    context.strokeStyle = "white";
    context.lineWidth = 2;
    context.strokeRect(50, 30, 110, 90);
    context.strokeRect(170, 65, 100, 80);
  };
  
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
        <input type="file" name="file" onChange={(e) => {setSelectedFile(e.target.files[0]); drawRectangle();}}/>
        <button onClick={() => fetchPlayerScoreResponse()}> SB </button>
        <Button type="primary" onClick={() => fetchPlayerScoreResponse()}>Primary Button</Button>
      </div>
      <h1>{data==null ? null : data.score}</h1>
      <div>
        <canvas
          ref={canvasRef}
          style={{
            width: "600px",
            height: "400px",
            background: selectedFile,
          }}
      />
      </div>
    </div>
  );
}
