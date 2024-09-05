import { useState } from "react";
import { CiSearch } from "react-icons/ci";
import axios from "axios";
const TextQuery = (props) => {
  const [valueQuery, setValueQuery] = useState("");
  const { setResult, setLoading } = props;
  const sleep = (ms) => {
    return new Promise((resolve) => setTimeout(resolve, ms));
  };
  const getData = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:8080/api/query/text", {
        params: {
          query: valueQuery,
          status: "active",
        },
      });
      setResult(response.data.data);
      console.log(response.data.data);
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
    <div className="w-80 flex flex-col items-center justify-center bg-gray-50 p-4 rounded-lg shadow-lg mt-2 ">
      <textarea
        onChange={(e) => {
          setValueQuery(e.target.value);
        }}
        id="message"
        rows="4"
        className="w-full block p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Write your thoughts here..."
      ></textarea>
      <button
        onClick={handleClickBtn}
        className="mt-2 w-full rounded-lg h-10 bg-blue-500 text-white  items-center justify-center hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Search
      </button>
    </div>
  );
};
export default TextQuery;
