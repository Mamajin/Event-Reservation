// HoverPasswordField.jsx
import React from 'react';

const HoverPasswordField = ({ password }) => {
  return (
    <div className="flex items-center">
      <label className="block text-sm font-medium text-gray-700">Password:  </label>
      <p
        className="mt-0 text-gray-900 bg-gray-100 p-2 rounded cursor-pointer hover:bg-gray-200"
        style={{
          display: 'inline-block',
          width: 'auto',
          overflow: 'hidden',
        }}
        title="Hover to reveal"
      >
        <input
          type="password"
          className="hover-password-field"
          defaultValue={password || '••••••••'}
          readOnly
          style={{
            background: 'transparent',
            border: 'none',
            outline: 'none',
            width: '100%',
            color: '#1f2937',
            fontSize: '1rem',
            padding: 0,
            fontFamily: 'inherit',
          }}
        />
      </p>

      {/* Hover Password CSS */}
      <style>
        {`
          .hover-password-field:hover {
            -webkit-text-security: none; /* Show text on hover */
            text-security: none;
          }
        `}
      </style>
    </div>
  );
};

export default HoverPasswordField;
