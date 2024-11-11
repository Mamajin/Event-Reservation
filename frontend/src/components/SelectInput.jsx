import React from 'react';

function SelectInput({ label, name, value, onChange, options }) {
  return (
    <div className='form-control'>
      <label className="label font-medium text-dark-purple">{label}</label>
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="select select-bordered bg-white text-dark-purple"
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