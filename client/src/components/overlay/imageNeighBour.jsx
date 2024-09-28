import { useState, useEffect, useRef } from "react";

const ImageNeighBor = (props) => {
  const { closeNeighBour, video, frame } = props;
  const [selectedImage, setSelectedImage] = useState(null); // State để lưu URL của hình ảnh được click
  const imageRefs = useRef([]); // Ref để lưu danh sách các hình ảnh

  const folder_video = video.substring(0, 3);
  const imageNeighBor = Array.from({ length: 201 }, (_, i) => i + frame - 100)
    .filter((num) => num > 0)
    .map((num, index) => {
      return (
        `https://storage.cloud.google.com/nidim/keyframe/${folder_video}/${video}/` +
        num.toString().padStart(4, "0") +
        ".jpg"
      );
    });

  // Sử dụng useEffect để cuộn tới ảnh khớp với frame khi component render
  useEffect(() => {
    const frameString = frame.toString().padStart(4, "0");
    const indexToScroll = imageNeighBor.findIndex((url) => url.includes(frameString));

    if (indexToScroll !== -1 && imageRefs.current[indexToScroll]) {
      const timeoutId = setTimeout(() => {
        imageRefs.current[indexToScroll].scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }, 3000); // Cuộn sau 3 giây
      return () => clearTimeout(timeoutId);
    }
  }, [frame, imageNeighBor]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 animate-popOut">
      <div className="rounded-md fixed flex flex-row bg-white w-[1280px] h-[600px] ">
        <header className="fixed w-[1280px] h-10 bg-[#6a6f90]">
          <div className="container mx-auto flex items-center justify-center">
            <h1 className="text-3xl font-bold text-[#EDE8F5]">NEIGHBOUR</h1>
          </div>
          <button
            onClick={closeNeighBour}
            className="absolute top-0 right-0 bg-red-500 text-white w-12 h-10 rounded-md"
          >
            X
          </button>
        </header>
        <div className="flex overflow-y-auto justify-center">
          <div className="mt-10 grid grid-cols-6 gap-1">
            {imageNeighBor.map((url, index) => (
              <div
                key={index}
                ref={(el) => (imageRefs.current[index] = el)} // Gán ref cho từng ảnh
              >
                <img
                  src={url}
                  alt={`${video}, ${frame}`}
                  className={`cursor-pointer w-full h-full object-cover ${
                    url.includes(frame.toString().padStart(4, "0")) ? "border-8 border-yellow-500" : ""
                  }`}
                  onClick={() => setSelectedImage(url)} // Khi click, lưu URL của hình ảnh được chọn
                />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Modal hiển thị ảnh phóng to */}
      {selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex justify-center items-center z-60">
          <div className="relative">
            <img
              src={selectedImage}
              alt="Selected"
              className="w-auto h-auto max-w-full max-h-full"
            />
            <button
              className="absolute top-0 right-0 bg-red-500 text-white w-8 h-8 rounded-full"
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

export default ImageNeighBor;