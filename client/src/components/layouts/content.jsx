import { useState } from "react";
import logo from "../../assets/spinning-dots.svg";
import ImageBouns from "../overlay/imageBonus";

const ContentPage = (props) => {
  const { result, loading } = props;
  const [clickedImage, setClickedImage] = useState(null);
  const [video, setVideo] = useState(null);
  const [frame, setFrame] = useState(null);

  const handleImageClick = (index, video, frame) => {
    setClickedImage(index);
    setVideo(video);
    setFrame(frame);
  };
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
              return (
                <div>
                  <img
                    key={index}
                    src={url}
                    alt=""
                    className="cursor-pointer w-[200px] h-[112.5px] object-cover"
                    onClick={() => handleImageClick(index, id_video, id_frame)}
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
      {clickedImage !== null && (
        <ImageBouns closeOverlay={closeOverlay} video={video} frame={frame} />
      )}
    </>
  );
};
export default ContentPage;
