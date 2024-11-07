import React from 'react';
import { MdOutlineFileUpload, MdCloudUpload, MdDelete } from "react-icons/md";

function FileInput({ label, name, onChange, accept, preview }) {
  const handleRemoveImage = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const input = document.getElementById(name);
    if (input) {
      input.value = '';
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  };

  const handleUploadClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById(name).click();
  };

  return (
    <div className="space-y-2" onClick={(e) => e.stopPropagation()}>
      <label htmlFor={name} className="block font-medium text-dark-purple">{label}</label>
      <div className="space-y-4">
        <div className="group relative w-full h-32 px-4 transition bg-white border-2 border-gray-300 border-dashed rounded-lg hover:border-amber-300 hover:bg-gray-50">
          {preview ? (
            <div className="relative w-full h-full">
              <img 
                src={preview} 
                alt="Preview" 
                className="object-contain w-full h-full"
              />
              <div 
                className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity cursor-pointer"
                onClick={handleUploadClick}
              >
                <span className="text-white text-sm">Click to change</span>
              </div>
              <button
                onClick={handleRemoveImage}
                className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                title="Remove image"
              >
                <MdDelete className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <div 
              className="h-full flex flex-col items-center justify-center space-y-2 cursor-pointer"
              onClick={handleUploadClick}
            >
              <MdOutlineFileUpload className="h-12 w-12 text-gray-400 group-hover:text-amber-500" />
              <div className="text-sm text-dark-purple">
                <span className="font-medium text-amber-500 hover:text-amber-600">Click to upload</span> or drag and drop
              </div>
              <p className="text-xs text-dark-purple">PNG, JPG up to 5MB</p>
            </div>
          )}
          <input
            type="file"
            id={name}
            name={name}
            onChange={onChange}
            accept={accept}
            className="hidden"
          />
        </div>
        
        <button
          type="button"
          onClick={handleUploadClick}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors"
        >
          <MdCloudUpload className="w-5 h-5" />
          {preview ? 'Change Image' : 'Upload Image'}
        </button>
      </div>
    </div>
  );
}

export default FileInput;