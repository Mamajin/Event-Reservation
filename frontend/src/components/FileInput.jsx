import React from 'react';
import { MdOutlineFileUpload } from "react-icons/md";

function FileInput({ label, name, onChange, accept }) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-dark-purple">{label}</label>
      <div className="relative">
        <label className="group flex items-center justify-center w-full h-32 px-4 transition bg-white border-2 border-gray-300 border-dashed rounded-lg hover:border-amber-300 hover:bg-gray-50 cursor-pointer">
          <div className="space-y-2 text-center">
            <MdOutlineFileUpload className="mx-auto h-12 w-12 text-gray-400 group-hover:text-amber-500" />
            <div className="text-sm text-dark-purple">
              <span className="font-medium text-amber-500 hover:text-amber-600">Click to upload</span> or drag and drop
            </div>
            <p className="text-xs text-dark-purple">PNG, JPG, PDF up to 10MB</p>
          </div>
          <input
            type="file"
            name={name}
            onChange={onChange}
            accept={accept}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
        </label>
      </div>
    </div>
  );
}

export default FileInput;