import { useState } from "react";
import { Image } from "antd";
const ContentPage = (props) => {
  const { result } = props;

  // const url_images1 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  // const url_images2 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  // const url_images3 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  // const url_images4 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  // const url_images5 = Array.from({ length: 200 }, (_, i) => 'https://storage.cloud.google.com/nidim/keyframe/L01/L01_V001/'+(i + 1).toString().padStart(3, '0')+ ".jpg");
  return (
    <div className="w-2/3 overflow-y-auto">
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
    </div>
  );
};
export default ContentPage;
