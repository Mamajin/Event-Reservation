import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from "../constants";
import HoverPasswordField from '../components/HoverPasswordField'; 
import EditableField from '../components/EditableField'; // New component for editable fields

function AccountInfo() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false); // State to manage edit mode
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
          throw new Error("No access token found");
        }

        const response = await api.get('/users/profile', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.headers["content-type"].includes("text/html")) {
          throw new Error("Expected JSON but received HTML response");
        }

        setUserData(response.data);
      } catch (err) {
        console.error("Error fetching user data:", err.message);
        if (err.message.includes("No access token found")) {
          alert("You are not logged in. Redirecting to login page...");
          navigate("/login");
        } else {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();

    // Cleanup function (if needed)
    return () => {
      // Any cleanup logic can go here
    };
  }, [navigate]);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleSaveChanges = async (updatedData) => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const userId = userData.id; // Assuming userData contains an id field

      console.log(userData.id)

      const response = await api.put(`/edit-profile/${userId}/`, updatedData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setUserData(response.data);
      setIsEditing(false);
    } catch (err) {
      console.error("Error saving user data:", err);
      setError(err);
    }
  };

  if (loading) {
    return (
      <PageLayout>
        <h2 className="text-2xl font-bold mb-4">Applied Events</h2>
        <div className="grid grid-cols-1 gap-4">
          <div className="loader">Loading...</div> {/* Replace with a spinner */}
        </div>
      </PageLayout>
    );
  }

  if (error) {
    return (
      <PageLayout>
        <div className="text-red-500">Error fetching user data: {error.message}</div>
      </PageLayout>
    );
  }

  if (!userData) {
    return (
      <PageLayout>
        <div>No user data available</div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="flex-1 p-6 bg-white rounded-lg shadow-lg w-full max-w-screen-lg mx-auto">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-2xl font-bold mb-6 text-dark-purple">Account Details</h1>
          <p className="text-gray-600 mb-6">See or edit your user login details.</p>

          {/* Profile Image */}
          <div className="flex items-center mb-6">
            <div className="w-24 h-24 bg-gray-200 rounded-full flex justify-center items-center">
              <svg 
                className="w-12 h-12 text-gray-400" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor" 
                aria-label="User Icon"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 12c2.667 0 4.667-2 4.667-4.667S14.667 2.667 12 2.667 7.333 4.667 7.333 7.333 9.333 12 12 12zm0 0v7.333m0 0c-1.567 0-5.333 1-5.333 2.333V21h10.667v-1.334c0-1.333-3.767-2.333-5.333-2.333z" />
              </svg>
            </div>
          </div>

          {/* User Information */}
          <div className="space-y-6">
            {/* Personal Info */}
            <div className="grid grid-cols-2 gap-4">
              <EditableField label="Username" value={userData.username} isEditing={isEditing} onSave={handleSaveChanges} fieldName="username" />

              <div>
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <p className="mt-0 text-gray-900">{userData.status || 'N/A'}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <EditableField label="First Name" value={userData.first_name} isEditing={isEditing} onSave={handleSaveChanges} fieldName="first_name" />
              <EditableField label="Last Name" value={userData.last_name} isEditing={isEditing} onSave={handleSaveChanges} fieldName="last_name" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <EditableField label="Email" value={userData.email} isEditing={isEditing} onSave={handleSaveChanges} fieldName="email" />
              <EditableField label="Mobile Phone" value={userData.phone_number} isEditing={isEditing} onSave={handleSaveChanges} fieldName="phone_number" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <EditableField label="Birth Date" value={userData.birth_date} isEditing={isEditing} onSave={handleSaveChanges} fieldName="birth_date" />
              <EditableField label="Address" value={userData.address} isEditing={isEditing} onSave={handleSaveChanges} fieldName="address" />
            </div>

            {/* Social and Event Info */}
            <div className="grid grid-cols-2 gap-4">
              <EditableField label="Facebook Profile" value={userData.facebook_profile} isEditing={isEditing} onSave={handleSaveChanges} fieldName="facebook_profile" />
              <EditableField label="Instagram Handle" value={userData.instagram_handle} isEditing={isEditing} onSave={handleSaveChanges} fieldName="instagram_handle" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Attended Events</label>
                <p className="mt-0 text-gray-900">{userData.attended_events_count || 0}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Cancelled Events</label>
                <p className="mt-0 text-gray-900">{userData.cancelled_events_count || 0}</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Nationality</label>
              <p className="mt-0 text-gray-900">{userData.nationality || 'N/A'}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Created At</label>
                <p className="mt-0 text-gray-900">{new Date(userData.created_at).toLocaleString() || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Updated At</label>
                <p className="mt-0 text-gray-900">{new Date(userData.updated_at).toLocaleString() || 'N/A'}</p>
              </div>
            </div>

          </div>

          {/* Edit Button */}
          <button onClick={handleEditToggle} className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition duration-200">
            {isEditing ? "Cancel" : "Edit"}
          </button>
        </div>
      </div>
    </PageLayout>
  );
}

export default AccountInfo;
