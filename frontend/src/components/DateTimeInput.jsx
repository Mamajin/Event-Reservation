import React from "react";
import "../style/index.css";
function DateTimeInput({ label, name, value, onChange, required }) {
    const formatDateForInput = (dateTime) => {
        const date = new Date(dateTime);
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}`;
      };
          
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
                defaultValue={formatDateForInput(value) || ""}
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