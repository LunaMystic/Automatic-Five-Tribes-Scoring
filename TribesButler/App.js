import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Button, Text, View } from 'react-native';

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
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
      <StatusBar style="auto" />
      <div>
        <input type="file" name="file" onChange={(e) => setSelectedFile(e.target.files[0])}/>
        <Button
          title="SUBMIT"
          color="#f194ff"
          onPress={() => fetchPlayerScoreResponse()}
        />
      </div>
      <Text>{data==null ? null : data.score}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
