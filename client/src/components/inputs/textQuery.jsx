import { useState } from "react";
import { Button } from "antd/es/radio";
import { CiSearch } from "react-icons/ci";
import axios from "axios"
const TextQuery = ()=>{
    const [valueQuery, setValueQuery] = useState("")
    const handleClickBtn = async ()=>{
        try {
            const response = await axios.get('http://localhost:8080/api/users', {
                params: {
                    textQuery: valueQuery,
                    status: 'active'
            }
        });
        console.log(response)
    }
    catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    return (
        <div>
            <label form="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your message</label>
            <span className="flex  ">
            <textarea onChange={(e)=>{setValueQuery(e.target.value)}} id="message" rows="4" className="mr-10 block p-2.5 w-3/4 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your thoughts here..."></textarea>
            <button onClick={handleClickBtn} className="mt-11 w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"><CiSearch/></button>
            </span>
            <h1>{valueQuery}</h1>
        </div>
    )
}
export default TextQuery;