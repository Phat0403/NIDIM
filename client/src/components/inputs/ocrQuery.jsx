import { useState } from "react";
import { CiSearch } from "react-icons/ci";
import axios from "axios";
import qs from "qs";
const OcrQuery = (props) => {
  const { setResult, setLoading } = props;
  const [queries, setQueries] = useState([{ id: 1, value: "" }]);

  const handleAddQuery = () => {
    setQueries([...queries, { id: queries.length + 1, value: "" }]);
  };

  const handleQueryChange = (id, newValue) => {
    setQueries(
      queries.map((query) =>
        query.id === id ? { ...query, value: newValue } : query
      )
    );
  };

  const handleDeleteQuery = () => {
    if (queries.length > 1) {
      const highestId = Math.max(...queries.map((query) => query.id));
      setQueries(queries.filter((query) => query.id !== highestId));
    }
  };

  const sleep = (ms) => {
    return new Promise((resolve) => setTimeout(resolve, ms));
  };
  const getData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        "http://104.214.176.14:3000/api/query/ocr",
        {
          //34.124.251.210:5000
          params: { queries },
          paramsSerializer: (params) => {
            return qs.stringify(params, { arrayFormat: "repeat" });
          },
        }
      );
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
      {queries.map((query) => (
        <textarea
          key={query.id}
          onChange={(e) => handleQueryChange(query.id, e.target.value)}
          value={query.value}
          id={`message-${query.id}`}
          rows="4"
          className="w-full block p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-2"
          placeholder={`Ocr query... (${query.id})`}
        ></textarea>
      ))}
      <button
        onClick={handleAddQuery}
        className="mt-2 w-full rounded-lg h-10 bg-blue-500 text-white  items-center justify-center hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Add query
      </button>
      <button
        onClick={handleDeleteQuery}
        className="mt-2 w-full rounded-lg h-10 bg-red-500 text-white items-center justify-center hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
      >
        Delete query
      </button>
      <button
        onClick={handleClickBtn}
        className="mt-2 w-full rounded-lg h-10 bg-green-500 text-white  items-center justify-center hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Search
      </button>
    </div>
  );
};
export default OcrQuery;
