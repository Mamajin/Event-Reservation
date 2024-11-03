import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from "../constants";

function AccountInfo() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
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
  }, [navigate]);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleInputChange = (field, value) => {
    setUserData(prevData => ({ ...prevData, [field]: value }));
  };

  const handleSaveChanges = async () => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const userId = userData.id;

      const updatedData = {
        ...userData,
        updated_at: new Date().toISOString(),
      };

      const response = await api.put(`users/edit-profile/${userId}/`, updatedData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log("User data updated successfully:", response.data);
      setIsEditing(false);
    } catch (err) {
      console.error("Error saving user data:", err.message);
      alert("Failed to save changes. Please try again.");
    }
  };

  if (loading) {
    return (
      <PageLayout>
        <div>Loading...</div>
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

  return (
    <PageLayout>
      <div className="flex-1 p-6 bg-white rounded-lg shadow-lg w-full max-w-screen-lg mx-auto">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-2xl font-bold mb-6 text-dark-purple">Account Details</h1>
          <p className="text-gray-600 mb-6">View or edit your user login details.</p>

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

          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">ID</label>
              <p className="mt-0 text-gray-900">{userData.id.toLocaleString() || 'N/A'}</p>
            </div>


            {/* User Fields */}
            {['username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'address', 'facebook_profile', 'instagram_handle', 'nationality'].map((field) => (
              <div key={field} className="grid grid-cols-2 gap-4">
                <label className="block text-sm font-medium text-gray-700 capitalize">{field.replace('_', ' ')}</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={userData[field] || ''}
                    onChange={(e) => handleInputChange(field, e.target.value)}
                    className="mt-1 p-2 border border-gray-300 rounded w-full"
                  />
                ) : (
                  <p className="mt-0 text-gray-900">{userData[field] || 'N/A'}</p>
                )}
              </div>
            ))}

            {/* Non-editable fields */}
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Attended Events</label>
              <p className="mt-0 text-gray-900">{userData.attended_events_count || 0}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Cancelled Events</label>
              <p className="mt-0 text-gray-900">{userData.cancelled_events_count || 0}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Created At</label>
              <p className="mt-0 text-gray-900">{new Date(userData.created_at).toLocaleString() || 'N/A'}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Updated At</label>
              <p className="mt-0 text-gray-900">{new Date(userData.updated_at).toLocaleString() || 'N/A'}</p>
            </div>

            {/* Edit and Save/Cancel Buttons */}
            {isEditing ? (
              <div className="flex mt-6 space-x-4">
                <button onClick={handleSaveChanges} className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition duration-200">
                  Confirm
                </button>
                <button onClick={handleEditToggle} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition duration-200">
                  Cancel
                </button>
              </div>
            ) : (
              <button onClick={handleEditToggle} className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition duration-200">
                Edit
              </button>
            )}
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default AccountInfo;
