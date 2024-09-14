import { useState } from "react";
import logo from "../../assets/spinning-dots.svg";
import ImageBouns from "../overlay/imageBonus";
import { Image, Space } from "antd";
import {
  ExportOutlined,
  RotateLeftOutlined,
  RotateRightOutlined,
  SwapOutlined,
  UndoOutlined,
  ZoomInOutlined,
  ZoomOutOutlined,
} from "@ant-design/icons";

const ContentPage = (props) => {
  const { result, loading } = props;
  const OpenURL = (url, time) => {
    window.open(url + "&t=" + Math.floor(+time), "_blank");
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
              const url_video = item.url;
              const pts_time = item.pts_time;
              const frame_idx = item.frame_idx;
              const url_img =
                `https://storage.cloud.google.com/nidim/keyframe/${folder_video}/${id_video}/` +
                id_frame.toString().padStart(3, "0") +
                ".jpg";
              return (
                <figure>
                  <Image
                    width={200}
                    src={url_img}
                    key={frame_idx}
                    preview={{
                      toolbarRender: (
                        _,
                        {
                          image: { url_img },
                          transform: { scale },
                          actions: {
                            onFlipY,
                            onFlipX,
                            onRotateLeft,
                            onRotateRight,
                            onZoomOut,
                            onZoomIn,
                            onReset,
                          },
                        }
                      ) => (
                        <Space size={12} className="toolbar-wrapper">
                          <ExportOutlined
                            onClick={() => OpenURL(url_video, pts_time)}
                          />
                          <SwapOutlined rotate={90} onClick={onFlipY} />
                          <SwapOutlined onClick={onFlipX} />
                          <RotateLeftOutlined onClick={onRotateLeft} />
                          <RotateRightOutlined onClick={onRotateRight} />
                          <ZoomOutOutlined
                            disabled={scale === 1}
                            onClick={onZoomOut}
                          />
                          <ZoomInOutlined
                            disabled={scale === 50}
                            onClick={onZoomIn}
                          />
                          <UndoOutlined onClick={onReset} />
                        </Space>
                      ),
                    }}
                  />
                  <figcaption>
                    {id_video}, {id_frame}
                  </figcaption>
                </figure>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
};
export default ContentPage;
