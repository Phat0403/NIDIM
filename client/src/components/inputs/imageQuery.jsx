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
  const handlePaste = (event) => {
    const items = event.clipboardData.items;

    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      if (item.type.indexOf("image") !== -1) {
        const file = item.getAsFile();
        setImage(file);
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreview(reader.result);
        };
        reader.readAsDataURL(file);
      }
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
      await axios.post("http://104.214.176.14:3000/api/query/image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const response = await axios.get("http://104.214.176.14:3000/api/query/image", {
        params: {
          type: "text",
          status: "active",
        },
      });

      setResult(response.data.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleClickBtn = async () => {
    await Promise.all([getData(), sleep(1000)]);
    setLoading(false);
  };

  return (
    <div className="w-80 flex flex-col items-center justify-center bg-gray-50 p-4 rounded-lg shadow-lg mt-2 "
    onPaste={handlePaste}>
      <div className="mb-2 w-full">
        {preview ? (
          <img
            src={preview}
            alt="Uploaded"
            className=" object-cover border-2 border-gray-300 shadow-lg rounded-lg"
          />
        ) : (
          <div
            className="h-40 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg"
          >
            <p className="text-gray-500">No image uploaded</p>
          </div>
        )}
      </div>
      <label
        htmlFor="upload"
        className="cursor-pointer bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg mb-2 transition-all duration-300 w-full text-center"
      >
        {preview ? "Change Image" : "Upload Image"}
      </label>
      <input
        id="upload"
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className="hidden"
      />
      <button
        onClick={handleClickBtn}
        className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-2 rounded-lg transition-all duration-300 w-full"
      >
        Search
      </button>
    </div>
  );
};

export default ImageQuery;
