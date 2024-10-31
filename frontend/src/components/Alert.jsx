import React from "react";

function Alert({ type, message, onClose }) {
  const alertTypeClasses = {
    success: "alert-success",
    error: "alert-error",
    warning: "alert-warning",
    info: "alert-info",
  };

  return (
    <div className={`alert ${alertTypeClasses[type]} shadow-lg`}>
      <div>
        <span>{message}</span>
      </div>
      {onClose && (
        <button onClick={onClose} className="btn btn-xs btn-circle btn-ghost">
          ✕
        </button>
      )}
    </div>
  );
}

export default Alert;
