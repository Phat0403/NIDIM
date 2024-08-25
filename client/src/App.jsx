import { useState } from "react";
import { Image } from 'antd';
function App() {
  const [showImage, setShowImage] = useState(false);
  const handleClick = () => {
    setShowImage(true);
  };
  const url_images1 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  const url_images2 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  const url_images3 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  const url_images4 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  const url_images5 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");

  return (
      <div>
        {showImage === false?
      (<button onClick={handleClick}>Show Image</button>)
      :
        (<div>
          {url_images1.map((url) => (
          <Image
          width={200}
          src= {url}
        />))}
      {url_images2.map((url) => (
        <Image
        width={200}
        src= {url}
      />))}
      {url_images3.map((url) => (
        <Image
        width={200}
        src= {url}
      />))}
      {url_images4.map((url) => (
        <Image
        width={200}
        src= {url}
      />))}
      {url_images5.map((url) => (
        <Image
        width={200}
        src= {url}
      />))}
        </div>)
      }
      </div>
  );
}

export default App;
