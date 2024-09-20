import axios from "axios";
import { useState, useEffect } from "react";

const ImageSimilar = (props) => {
  const { closeSimilar, video, frame } = props;
  const [similar, setSimilar] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null); // State để lưu hình ảnh đã được click

  const folder_video = video.substring(0, 3);
  const url_img =
    `C:/Users/tanph/Downloads/${folder_video}/${video}/` +
    frame.toString().padStart(3, "0") +
    ".jpg";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8080/api/query/similar",
          {
            params: { url_img },
          }
        );
        setSimilar(response.data.data);
        console.log(response.data.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [url_img]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 animate-popOut">
      <div className="rounded-md fixed flex flex-row bg-white w-[1280px] h-[600px] ">
        <header className="fixed w-[1280px] h-10 bg-[#6a6f90]">
          <div className="container mx-auto  flex items-center justify-center">
            <h1 className="text-3xl font-bold text-[#EDE8F5]">NEIGHBOUR</h1>
          </div>
          <button
            onClick={() => {
              closeSimilar();
            }}
            className="absolute top-0 right-0 bg-red-500 text-white w-12 h-10 rounded-md"
          >
            X
          </button>
        </header>
        <div className="flex overflow-y-auto justify-center">
          <div className="mt-10 grid grid-cols-6 gap-1">
            {similar.map((item, index) => {
              const id_video = item.video;
              const folder_video = id_video.substring(0, 3);
              const id_frame = item.id;
              const url_img =
                `https://storage.cloud.google.com/nidim/keyframe/${folder_video}/${id_video}/` +
                id_frame.toString().padStart(3, "0") +
                ".jpg";
              return (
                <div className='relative' key={index}>
                  <img
                    src={url_img}
                    alt=""
                    className={`cursor-pointer w-full h-full object-cover ${
                      index === 0 ? "border-8 border-yellow-500" : ""
                    }`}
                    onClick={() => setSelectedImage(url_img)} // Khi click sẽ set hình ảnh đã chọn
                  />
                  <div className=" absolute top-0 left-0 items-center justify-between flex">
                      <p className="p-1 border border-white bg-black opacity-50  text-white text-sm animate-popOut ">
                        {id_video}, {id_frame}
                      </p>
                    </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Hiển thị hình ảnh phóng to nếu có hình ảnh được chọn */}
      {selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center z-60">
          <div className="relative">
            <img
              src={selectedImage}
              alt="Selected"
              className="w-auto h-auto max-w-full max-h-full"
            />
            <button
              className=" absolute top-0 right-0 bg-red-500 text-white w-8 h-8 rounded-full"
              onClick={() => setSelectedImage(null)} // Đóng modal khi nhấn nút
            >
              X
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageSimilar;
