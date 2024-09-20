import { useState } from "react";
import logo from "../../assets/spinning-dots.svg";
import { BiSlideshow } from "react-icons/bi";
import { BsCardImage, BsBoxArrowUpRight } from "react-icons/bs";

import ImageNeighBor from "../overlay/imageNeighBour";
import ImageSimilar from "../overlay/imageSimilar";

const ContentPage = (props) => {
  const { result, loading } = props;
  const [selectedNeighbour, setSelectedNeighbour] = useState(null);
  const [selectedSimilar, setSelectedSimilar] = useState(null);

  const handleNeighBourClick = (id_video, id_frame) => {
    setSelectedNeighbour({ video: id_video, frame: id_frame });
  };

  const closeNeighBour = () => {
    setSelectedNeighbour(null);
  };
  const handleSimilarClick = (id_video, id_frame) => {
    setSelectedSimilar({ video: id_video, frame: id_frame });
  };

  const closeSimilar = () => {
    setSelectedSimilar(null);
  };

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
          <div className="grid grid-cols-6 gap-2">
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
                <>
                  <div className="group relative w-[200px] h-[112.5px]">
                    <img
                      className=" h-full w-full object-cover"
                      src={url_img}
                      alt=""
                    />
                    <div className="w-full absolute top-0 left-0 items-center justify-between flex">
                      <p className="p-1 border border-white bg-black opacity-50  text-white text-sm animate-popOut ">
                        {id_video}, {frame_idx}
                      </p>
                    </div>
                    <div className=" absolute top-0 right-0  hidden group-hover:flex">
                      <button
                        onClick={() => {
                          OpenURL(url_video, pts_time);
                        }}
                        className="p-2 border border-white bg-black opacity-50 rounded-sm text-white text-sm animate-popOut"
                      >
                        <BiSlideshow />
                      </button>
                    </div>
                    <div className="w-full absolute bottom-0  items-center justify-between hidden group-hover:flex">
                      <button
                        onClick={() => handleNeighBourClick(id_video, id_frame)}
                        className="p-2 border left-0 border-white bg-black opacity-50 rounded-sm text-white text-sm animate-popOut"
                      >
                        <BsCardImage />
                      </button>
                      <button
                        onClick={() => handleSimilarClick(id_video, id_frame)}
                        className="p-2 border right-0 border-white bg-black opacity-50 rounded-sm text-white text-sm animate-popOut"
                      >
                        <BsBoxArrowUpRight />
                      </button>
                    </div>
                  </div>
                  {selectedNeighbour &&
                    selectedNeighbour.video === id_video &&
                    selectedNeighbour.frame === id_frame && (
                      <ImageNeighBor
                        closeNeighBour={closeNeighBour}
                        video={id_video}
                        frame={id_frame}
                      />
                    )}
                  {selectedSimilar &&
                    selectedSimilar.video === id_video &&
                    selectedSimilar.frame === id_frame && (
                      <ImageSimilar
                        closeSimilar={closeSimilar}
                        video={id_video}
                        frame={id_frame}
                      />
                    )}
                </>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
};
export default ContentPage;
