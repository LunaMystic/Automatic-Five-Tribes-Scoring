import './App.css';
import PlayerDetail from './PlayerDetail';
import ScoreSheet from './ScoreSheet';
import React, { useState, useEffect, useRef } from 'react';
import { Button, Space } from 'antd';
import PublicBoard from './PublicBoard';
 
export default function App() {
  const [playerDetailData, setPlayerDetailData] = useState([]);

  return (
    <div>
      <PublicBoard />
      <PlayerDetail updater={(newVal) => {setPlayerDetailData([...playerDetailData, newVal])}}/>
      <ScoreSheet merc_score_arr={playerDetailData}/>
    </div>
  );
}
