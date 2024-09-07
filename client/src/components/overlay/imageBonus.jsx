const ImageBouns = (props) => {
  const { closeOverlay, video, frame } = props;
  const imageNeighBor = []
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="rounded-md fixed bg-white w-[1280px] h-[600px] ">
        <header className="w-full h-8 bg-[#6a6f90]">
        <button
          onClick={closeOverlay}
          className="absolute top-0 right-0 bg-red-500 text-white w-12 h-8 rounded-md"
        >
          X
        </button>
        </header>
        <p>This is the overlay content!</p>
        <h1>
          {video}, {frame}
        </h1>
      </div>
    </div>
  );
};
export default ImageBouns;
