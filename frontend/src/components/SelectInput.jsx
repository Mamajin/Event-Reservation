import React from 'react';

function SelectInput({ label, name, value, onChange, options }) {
  return (
    <div>
      <label className="block text-sm font-medium text-dark-purple pb-3">{label}</label>
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="select bg-white"
        required
      >
        <option value="" disabled>Select an option</option>
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default SelectInput;