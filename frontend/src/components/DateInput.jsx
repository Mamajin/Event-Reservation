import React from "react";
import "../style/index.css";

function DateInput({ name, value, onChange, required, type = "datetime-local" }) {
    return (
        <div className="form-control w-full">
            <input
                type={type}
                name={name}
                value={value}
                onChange={onChange}
                className="input text-gray-600 bg-gray-100 input-bordered w-full"
                required={required}
            />
        </div>
    );
}

export default DateInput;
