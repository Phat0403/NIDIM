import React, { useState } from "react";
import axios from "axios";

const ImageQuery = (props) => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const { setResult, setLoading } = props;

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImage(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  const sleep = (ms) => {
    return new Promise((resolve) => setTimeout(resolve, ms));
  };
  const getData = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("image", image);
      const postImage = await axios.post(
        "http://localhost:8080/api/query/image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      const response = await axios.get(
        "http://localhost:8080/api/query/image",
        {
          params: {
            type: "text",
            status: "active",
          },
        }
      );
      setResult(response.data.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleClickBtn = async () => {
    await Promise.all([
      getData(), // Hàm async cần chạy
      sleep(1000), // Hàm sleep chạy song song
    ]);
    setLoading(false);
  };
  return (
    <div className="flex-row h-40 mt-10 items-center justify-center bg-gray-100 ">
      <div className="border ">
      {preview && (
        <img
          src={preview}
          alt="Uploaded"
          className="w-40 h-40 object-cover border-2 border-gray-300 shadow-lg rounded-lg"
        />
      )}
      {!preview && <p className="text-gray-500 border">No image uploaded</p>}
      </div>
      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className=""
      />
      <button onClick={handleClickBtn} className="border-2">
        Search
      </button>
    </div>
  );
};

export default ImageQuery;
