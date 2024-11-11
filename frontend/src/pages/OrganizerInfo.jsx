import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from "../constants";

function OrganizerInfo() {
  const [organizerData, setOrganizerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [previewLogo, setPreviewLogo] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrganizerData = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
          throw new Error("No access token found");
        }

        const response = await api.get('/organizers/view-organizer', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.headers["content-type"].includes("text/html")) {
          throw new Error("Expected JSON but received HTML response");
        }

        setOrganizerData(response.data);
        if (response.data.logo) {
          setPreviewLogo(response.data.logo);
        }
      } catch (err) {
        console.error("Error fetching organizer data:", err.message);
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

    fetchOrganizerData();
  }, [navigate]);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleInputChange = (field, value) => {
    setOrganizerData(prevData => ({ ...prevData, [field]: value }));
  };

  const handleSaveChanges = async () => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
  
      // Create an object that will store the fields that have been edited
      const updatedData = {};
  
      // Add only the changed fields to updatedData
      Object.keys(organizerData).forEach((field) => {
        if (organizerData[field] !== undefined && organizerData[field] !== null) {
          updatedData[field] = organizerData[field];
        }
      });
  
      // Check if there are any changes, if not, alert the user
      if (Object.keys(updatedData).length === 0) {
        alert("No changes were made.");
        return;
      }
  
      // Make the PUT request to save the changes
      const response = await api.put('/organizers/update-organizer', updatedData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      console.log("Organizer data updated successfully:", response.data);
      setIsEditing(false);  // Turn off the editing mode after saving
    } catch (err) {
      console.error("Error saving organizer data:", err.message);
      alert("Failed to save changes. Please try again.");
    }
  };
  
  

  const handleLogoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreviewLogo(URL.createObjectURL(file)); // Show selected logo preview
      uploadLogo(file); // Upload logo
    }
  };

  const uploadLogo = async (file) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    const formData = new FormData();
    formData.append("logo", file);

    try {
      const response = await api.post(`/organizers/${organizerData.id}/upload/logo/`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      setPreviewLogo(response.data.file_url);
    } catch (err) {
      console.error("Error uploading logo:", err.message);
      alert("Failed to upload logo. Please try again.");
    }
  };

  const goToAccountInfo = () => {
    navigate('/account-info');
  };

  const organizerTypes = [
    'INDIVIDUAL', 'COMPANY', 'NONPROFIT', 'EDUCATIONAL', 'GOVERNMENT'
  ];

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
        <div className="text-red-500">Error fetching organizer data: {error.message}</div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="flex-1 p-6 bg-white rounded-lg shadow-lg w-full max-w-screen-lg mx-auto">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-2xl font-bold mb-6 text-dark-purple">Organizer Profile</h1>

            {/* Navigate to Organizer Info Button */}
            <div className="mt-6">
              <button
                onClick={goToAccountInfo}
                className="px-4 py-2 bg-amber-300 text-dark-purple rounded hover:bg-yellow-600 transition duration-200"
              >
                Back to Account Info
              </button>
            </div>

          <p className="mt-6 text-gray-600 mb-6">View or edit your organizer profile details.</p>

          {/* Organizer Logo */}
          <div className="flex items-center mb-6">
            <div className="w-24 h-24 rounded-full overflow-hidden flex justify-center items-center bg-gray-200">
              {previewLogo ? (
                <img src={previewLogo} alt="Organizer Logo" className="w-full h-full object-cover" />
              ) : (
                <div className="w-24 h-24 bg-white rounded-full"></div>
              )}
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleLogoChange}
              className="ml-4"
            />
          </div>

          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">ID</label>
              <p className="mt-0 text-gray-900">{organizerData.id.toLocaleString() || 'N/A'}</p>
            </div>

            {/* Organizer Fields */}
            {['organizer_name', 'email'].map((field) => (
              <div key={field} className="grid grid-cols-2 gap-4">
                <label className="block text-sm font-medium text-gray-700 capitalize">{field.replace('_', ' ')}</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={organizerData[field] || ''}
                    onChange={(e) => handleInputChange(field, e.target.value)}
                    className="mt-1 p-2 border border-gray-300 rounded w-full"
                  />
                ) : (
                  <p className="mt-0 text-gray-900">{organizerData[field] || 'N/A'}</p>
                )}
              </div>
            ))}

            {/* Organization Type Dropdown */}
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Organization Type</label>
              {isEditing ? (
                <select
                  value={organizerData.organization_type || ''}
                  onChange={(e) => handleInputChange('organization_type', e.target.value)}
                  className="mt-1 p-2 border border-gray-300 rounded w-full"
                >
                  <option value="">Select an organization type</option>
                  {organizerTypes.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              ) : (
                <p className="mt-0 text-gray-900">{organizerData.organization_type || 'N/A'}</p>
              )}
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

export default OrganizerInfo;
