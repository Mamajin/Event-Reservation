import React from "react";
import "../style/index.css";

function DateTimeInput({ label, name, value, onChange, required }) {
    return (
        <div className="form-control w-full">
            <label className="label">
                <span className="label-text font-medium text-dark-purple">{label}</span>
            </label>
            <input
                type="datetime-local"
                name={name}
                value={value}
                onChange={onChange}
                className="input bg-gray-100 input-bordered w-full"
                required={required}
            />
        </div>
    );
}

export default DateTimeInput;