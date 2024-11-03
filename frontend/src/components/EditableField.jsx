import React, { useState } from 'react';

const EditableField = ({ label, value, isEditing, onSave, fieldName }) => {
  const [inputValue, setInputValue] = useState(value);

  const handleSave = () => {
    onSave({ [fieldName]: inputValue });
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      {isEditing ? (
        <div className="flex items-center mt-1">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button onClick={handleSave} className="ml-2 bg-green-500 text-white px-4 py-1 rounded hover:bg-green-600">
            Save
          </button>
        </div>
      ) : (
        <p className="mt-0 text-gray-900">{value || 'N/A'}</p>
      )}
    </div>
  );
};

export default EditableField;
