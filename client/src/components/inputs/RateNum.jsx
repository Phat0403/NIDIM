import React, { useState } from 'react';

const RateNum = (props) => {
    const {rateNum}=props;
    const [value, setValue] = useState(0);
    const handleChange = (e) => {
        setValue(e.target.value);
    };

    return (
        <div className="w-80 flex flex-col items-center bg-gray-50 p-4 rounded-lg shadow-lg mt-2">
            <label className="mb-2 text-gray-700 font-semibold">Threshold:</label>
            <input
                type="number"
                value={value}
                min="0"
                max="1"
                step="0.05"
                onChange={handleChange}
                className="text-center text-lg w-full mb-2 border border-gray-300 rounded"
            />
        </div>
    );
};

export default RateNum;
