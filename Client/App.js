import React, { useState, useEffect, useRef } from 'react';
import { Text, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera';
import Toast, { DURATION } from 'react-native-easy-toast';

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [isSecond, setIsSecond] = useState(false);
  const camera = useRef(null);
  const toast = useRef(null);
  const photos = useRef([]);
  const url = 'http://density-calculator.herokuapp.com/api/detect_mitsu';
  // const url = 'http://192.168.11.13:5000/api/save_picture';
  // const url = 'http://192.168.11.13:5000/api/detect_mitsu';

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  getFileData = (photo) => {
    const localUri = photo.uri;
    const filename = localUri.split('/').pop();
    const match = /\.(\w+)$/.exec(filename);
    const type = match ? `image/${match[1]}` : `image`;
    return { uri: localUri, name: filename, type };
  }

  uploadFiles = async () => {
    toast.current.show('判定中です...', DURATION.FOREVER);

    const data = new FormData();
    data.append('pic1', getFileData(photos.current[0]));
    data.append('pic2', getFileData(photos.current[1]));
    data.append('move', '10');
    data.append('cmos', '4.8');

    const response = await fetch(url, {
      method: 'POST',
      body: data,
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    const responseJson = await response.json();
    if (responseJson.error) {
      toast.current.show(responseJson.error, 5000);
    } else if (responseJson.mitsu) {
      toast.current.show('密です！', 5000);
    } else {
      toast.current.show('密ではありません', 5000);
    }
    console.log(responseJson);
    photos.current = [];
  }

  snap = async () => {
    if (!camera.current) {
      return
    }
    const photo = await camera.current.takePictureAsync({
      quality: 0.1,
      exif: true
    });
    photos.current.push(photo);

    if (isSecond) {
      uploadFiles();
    }
    setIsSecond(!isSecond);
  };

  getMessage = () => isSecond ? '右へ10cmずらしてタップしてください' : 'タップして1枚目を撮影';

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }
  return (
    <View style={{ flex: 1 }}>
      <Camera style={{ flex: 1 }} ref={camera}
        autoFocus={Camera.Constants.AutoFocus.on}>
        <View
          style={{
            flex: 1,
            backgroundColor: 'transparent',
            flexDirection: 'row',
          }}>
          <TouchableOpacity
            style={{
              flex: 1,
              alignSelf: 'center',
              alignItems: 'center',
            }}
            onPress={snap}>
            <Text style={{ fontSize: 20, marginBottom: 10, color: 'white' }}>{getMessage()}</Text>
          </TouchableOpacity>
        </View>
      </Camera>
      <Toast ref={toast}
        position='top'
        textStyle={{ fontSize:20, color:'white' }}
      />
    </View>
  );
}