import React from "react";
import "../style/index.css";
function DateTimeInput({ label, name, value, onChange, required }) {

    const currentYear = new Date().getFullYear();
    const maxYear = currentYear + 100;
    const minDate = `${currentYear}-01-01T00:00`;
    const maxDate = `${maxYear}-12-31T23:59`;

    return (
        <div className="form-control w-full">
            <label className="label">
                <span className="label-text font-medium text-dark-purple">{label}</span>
            </label>
            <input
                type="datetime-local"
                name={name}
                value={value || ""}
                onChange={onChange}
                className="input bg-gray-100 input-bordered w-full"
                required={required}
                min={minDate}
                max={maxDate}  
            />
        </div>
    );
}

export default DateTimeInput;