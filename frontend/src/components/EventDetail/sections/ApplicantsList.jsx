import React from 'react';
import { LuUsers, LuMail, LuPhone, LuBuilding2, LuMapPin, LuFlag, LuCalendar, LuX } from "react-icons/lu";

const ApplicantsList = ({ isOpen, onClose, applicants }) => {
  if (!isOpen) return null;
    console.log(applicants);
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
        <div className="p-6 border-b flex justify-between items-center">
          <div className="flex items-center gap-2">
            <LuUsers className="w-5 h-5 text-blue-600" />
            <h2 className="text-2xl font-semibold text-gray-800">Event Applicants</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <LuX className="w-5 h-5 text-gray-500" />
          </button>
        </div>
        
        <div className="overflow-y-auto max-h-[calc(90vh-88px)]">
          <div className="grid gap-4 p-6">
            {applicants.map((applicant) => (
              <div
                key={applicant.id}
                className="bg-gray-50 rounded-lg p-4 flex gap-4"
              >
                <img
                  src={applicant.profile_picture}
                  alt={`${applicant.username}'s profile picture`}
                  className="w-16 h-16 rounded-full object-cover"
                />
                
                <div className="flex-1 space-y-3">
                  <div>
                    <h3 className="text-lg font-medium text-gray-800">
                      {applicant.first_name} {applicant.last_name}
                    </h3>
                    <p className="text-sm text-gray-500">@{applicant.username}</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                    <div className="flex items-center gap-2 text-gray-600">
                      <LuMail className="w-4 h-4" />
                      {applicant.email}
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <LuPhone className="w-4 h-4" />
                      {applicant.phone_number}
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <LuBuilding2 className="w-4 h-4" />
                      {applicant.company}
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <LuMapPin className="w-4 h-4" />
                      {applicant.address}
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <LuFlag className="w-4 h-4" />
                      {applicant.nationality}
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <LuCalendar className="w-4 h-4" />
                      {new Date(applicant.birth_date).toLocaleDateString()}
                    </div>
                  </div>
                  
                  <div className="flex gap-4 text-sm">
                    <div className="text-green-600">
                      {applicant.attended_events_count} events attended
                    </div>
                    <div className="text-red-600">
                      {applicant.cancelled_events_count} events cancelled
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      applicant.status === 'approved' ? 'bg-green-100 text-green-700' :
                      applicant.status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {applicant.status.charAt(0).toUpperCase() + applicant.status.slice(1)}
                    </span>
                    <span className="text-xs text-gray-500">
                      Applied {new Date(applicant.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApplicantsList;