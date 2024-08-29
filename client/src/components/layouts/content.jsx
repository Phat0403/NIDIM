import { useState } from "react";
import { Image } from "antd";
import logo from "../../assets/spinning-dots.svg";

const ContentPage = (props) => {
  const { result, loading } = props;
  return (
    <div className="flex w-2/3 overflow-y-auto">
      {loading === true
      ?
      (
        <div className="flex  ">
          <img className="scale-[0.2] ml-40 mb-20" src={logo} alt="" />
        </div>
      )
      :
      (
        <div className="grid grid-cols-5">
        {result.map((item) => {
          const id_video = item.video;
          const id_frame = item.id;
          const folder_video = id_video.substring(0, 3);
          const url =
            `https://storage.cloud.google.com/nidim/keyframe/${folder_video}/${id_video}/` +
            id_frame.toString().padStart(3, "0") +
            ".jpg";
          return <Image width={200} src={url} />;
        })}
      </div>
      )
      }
    </div>
  );
};
export default ContentPage;
