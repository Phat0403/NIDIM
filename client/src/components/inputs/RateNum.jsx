import React, { useState, useEffect } from 'react';

const RateNum = (props) => {
    const { setRateNum } = props; 
    const [value, setValue] = useState(4);

    const handleChange = (e) => {
        const newValue = e.target.value;
        setValue(newValue);
        setRateNum(newValue); 
    };

    return (
        <div className="w-80 flex flex-col items-center bg-gray-50 p-4 rounded-lg shadow-lg mt-2">
            <label className="mb-2 text-gray-700 font-semibold">Span:</label>
            <input
                type="number"
                value={value}
                onChange={handleChange}
                className="text-center text-lg w-full mb-2 border border-gray-300 rounded"
            />
        </div>
    );
};

export default RateNum;
