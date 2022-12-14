import './App.css';
 
import React, { useState, useEffect, useRef } from 'react';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Space } from 'antd';
import { message, Upload } from 'antd';
 
export default function PlayerDetail({updater, ...rest}) {
  const [progress, setProgress] = useState(0);
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
        updater(json.score)
        setProgress(progress + 1)
      })
      .catch((error) => {
        console.error(error);
    });
  };

  const renderColorText= (param) => {
    switch(param) {
        case 0:
            return 'purple';
        case 1:
            return 'yellow';
        default:
            return 'black';
    }
  }

  return (
    <div>
      <h1>Open up App.js to start working on your app!</h1>
      <div>
        <Upload maxCount={1} beforeUpload={(e) => {
            setSelectedFile(e);
            return false;
        }}>
            <Button icon={<UploadOutlined />}>Please Upload Image For {renderColorText(progress)} </Button>
        </Upload>
        <Button type="primary" onClick={() => fetchPlayerScoreResponse()}>Primary Button</Button>
      </div>
      <h1>{data==null ? null : data.score}</h1>
    </div>
  );
}
