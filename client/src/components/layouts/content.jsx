import { useState } from "react";
import logo from "../../assets/spinning-dots.svg";
import ImageBouns from "../overlay/imageBonus";

import { Image, Space } from 'antd';
import {
  ExportOutlined,
  RotateLeftOutlined,
  RotateRightOutlined,
  SwapOutlined,
  UndoOutlined,
  ZoomInOutlined,
  ZoomOutOutlined,
} from '@ant-design/icons';

const ContentPage = (props) => {
  const { result, loading } = props;
  const [clickedImage, setClickedImage] = useState(null);
  const [video, setVideo] = useState(null);
  const [frame, setFrame] = useState(null);

  const [names, setNames] = useState({});


  const getName = async (url, id_frame) => {
    try {
      const response = await fetch('http://127.0.0.1:8080/getname', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: url }),
      });
      const data = await response.json();
      setNames((prevNames) => ({
        ...prevNames,
        [id_frame]: data['data'], // Lưu tên theo id_frame
      }));
    } catch (error) {
      console.error('Error fetching name:', error);
    }
  };

  const OpenURL = (url) => {
    fetch('http://127.0.0.1:8080/getlink', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: url})  
    })
    .then(response => response.json())
    .then(data => {
          window.open(data['data'], '_blank');
    });
}// 
  const closeOverlay = () => {
    setClickedImage(null);
  };
  return (
    <>
      <div className="flex border  bg-[#EDE8F5] mt-1 ml-1 rounded-lg w-[calc(100%-300px)] overflow-y-auto justify-center">
        {loading === true ? (
          <div className="flex">
            <img className="scale-[0.2] ml-40 mb-20" src={logo} alt="" />
          </div>
        ) : (
          <div className="grid grid-cols-5 gap-4">
            {result.map((item, index) => {
              const id_video = item.video;
              const id_frame = item.id;
              const folder_video = id_video.substring(0, 3);
              const url =
                `https://storage.cloud.google.com/nidim/keyframe/${folder_video}/${id_video}/` +
                id_frame.toString().padStart(3, "0") +
                ".jpg";
                if (!names[id_frame]) {
              getName(url, id_frame);
            }
            const name = names[id_frame] || "Loading...";
            return  <figure>
              <Image width={200} src={url} 
            preview={{
              toolbarRender: (
                _,
                {
                  image: { url },
                  transform: { scale },
                  actions: { onFlipY, onFlipX, onRotateLeft, onRotateRight, onZoomOut, onZoomIn, onReset },
                },
              ) => (
                <Space size={12} className="toolbar-wrapper">
                  <ExportOutlined onClick={()=>OpenURL(url)} />
                  <SwapOutlined rotate={90} onClick={onFlipY} />
                  <SwapOutlined onClick={onFlipX} />
                  <RotateLeftOutlined onClick={onRotateLeft} />
                  <RotateRightOutlined onClick={onRotateRight} />
                  <ZoomOutOutlined disabled={scale === 1} onClick={onZoomOut} />
                  <ZoomInOutlined disabled={scale === 50} onClick={onZoomIn} />
                  <UndoOutlined onClick={onReset} />
                </Space>
              ),
            }}
            />
            <figcaption>{name}</figcaption>
          </figure> 
            })}
          </div>
        )}
      </div>
    </>
  );
};
export default ContentPage;
