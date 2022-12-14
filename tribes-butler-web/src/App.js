import './App.css';
 
import React, { useState, useEffect, useRef } from 'react';
import { Button, Space } from 'antd';
 
export default function App() {
  const canvasRef = useRef();
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
 
  const drawRectangle = () => {
    if(selectedFile == null){return}


    const context = canvasRef.current.getContext("2d");

    
    const canvasBG = new Image(600,400);
    canvasBG.src= URL.createObjectURL(selectedFile);
    canvasBG.onload = () => {
      var imgwidth = canvasBG.width;
      var imgheight = canvasBG.height;
      console.log(imgheight, imgwidth)
      context.drawImage(canvasBG, 0, 0, 600, 500);

      context.strokeStyle = "red";
      context.lineWidth = 2;
      context.strokeRect(0, 0, 600, 500);
      for (let i = 0; i < 500; i+=100) {
        context.strokeRect(i, 0, 100, 500);
        context.strokeRect(0, i, 600, 100);
      }
    } 

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

  // useEffect(() => {
  //   // Update the document title using the browser API
  //   canvasBgRef.onload = () => {
  //     console.log("?");
  //     const context = canvasRef.current.getContext("2d");
  //     context.drawImage(canvasBgRef, 0, 0, 600, 400)
  //     drawRectangle();
  //   }
  // });

  useEffect(() => {
    drawRectangle(); // This is be executed when `loading` state changes
  });

  return (
    <div>
      <h1>Open up App.js to start working on your app!</h1>
      <div>
        <canvas
          ref={canvasRef}
          width="600" 
          height="500"
        />
      </div>
      <div>
        <input type="file" name="file" onChange={(e) => {
          setSelectedFile(e.target.files[0]);
        }}/>
        <button onClick={() => fetchPlayerScoreResponse()}> SB </button>
        <Button type="primary" onClick={() => fetchPlayerScoreResponse()}>Primary Button</Button>
      </div>
      <h1>{data==null ? null : data.score}</h1>
    </div>
  );
}
