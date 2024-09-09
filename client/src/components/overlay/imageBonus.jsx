const ImageBouns = (props) => {
  const { closeOverlay, video, frame } = props;
  const folder_video = video.substring(0, 3);
  const imageNeighBor = Array.from(
    { length: 54 },
    (_, index) => index - 27
  ).map(
    (num) =>
      `https://storage.cloud.google.com/nidim/keyframe/${folder_video}/${video}/` +
      (num + frame).toString().padStart(3, "0") +
      ".jpg"
  );
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="rounded-md fixed bg-white w-[1280px] h-[600px] overflow-y-auto">
        <header className="w-full h-8 bg-[#6a6f90]">
          <button
            onClick={closeOverlay}
            className="absolute top-0 right-0 bg-red-500 text-white w-12 h-8 rounded-md"
          >
            X
          </button>
        </header>
        <div className="grid grid-cols-6 gap-2">
          {imageNeighBor.map((url, index) => (
            <div>
            <img
              key={index}
              src={url}
              alt=""
              className="cursor-pointer w-[200px] h-[112.5px] object-cover"
            />
          </div>
          ))}
        </div>
      </div>
    </div>
  );
};
export default ImageBouns;
