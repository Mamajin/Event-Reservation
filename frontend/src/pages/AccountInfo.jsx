import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import DateInput from '../components/DateInput'; // Import DateTimeInput component
import Map from '../components/Map';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN, USER_STATUS, PROFILE_PICTURE } from "../constants";

function AccountInfo() {
  const { register, setValue, handleSubmit, watch } = useForm();
  const [userData, setUserData] = useState(null);
  const [isOrganizer, setIsOrganizer] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);
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
        setIsOrganizer(response.data[USER_STATUS] === 'Organizer');

        setValue('address', response.data.address);
        setValue('latitude', response.data.latitude);
        setValue('longitude', response.data.longitude);


        if (response.data.profile_picture) {
          setPreviewImage(response.data.profile_picture);
        }
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
        address: watch('address'),
        latitude: watch('latitude'),
        longitude: watch('longitude'),
        updated_at: new Date().toISOString(),
      };

      const response = await api.patch(`users/edit-profile/${userId}/`, updatedData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log("User data updated successfully:", response.data);
      setIsEditing(false);

      window.location.reload();
    } catch (err) {
      console.error("Error saving user data:", err.message);
      alert("Failed to save changes. Please try again.");
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreviewImage(URL.createObjectURL(file)); // Show selected image preview
      uploadProfilePicture(file); // Upload image
    }
  };

  const uploadProfilePicture = async (file) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    const formData = new FormData();
    formData.append("profile_picture", file);

    try {
      const response = await api.post(`/users/${userData.id}/upload/profile-picture/`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      setPreviewImage(`http://127.0.0.1:8000${response.data.file_url}`);
      localStorage.setItem(PROFILE_PICTURE, response.data.file_url)
    } catch (err) {
      console.error("Error uploading profile picture:", err.message);
      alert("Failed to upload profile picture. Please try again.");
    }
  };

  const handleMapClick = (address, latitude, longitude) => {
    // Update form and user data on map click
    setValue('address', address);
    setValue('latitude', latitude);
    setValue('longitude', longitude);
    setUserData((prevData) => ({
      ...prevData,
      address,
      latitude,
      longitude,
    }));
  };

  const goToOrganizerInfo = () => {
    navigate('/organizer-info');
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

          {/* Show Organizer Info Button only if user is an organizer */}
          {isOrganizer && (
            <div className="mt-6">
              <button
                onClick={goToOrganizerInfo}
                className="px-4 py-2 bg-amber-300 text-dark-purple rounded hover:bg-yellow-600 transition duration-200"
              >
                Go to Organizer Profile
              </button>
            </div>
          )}

          <p className="mt-6 text-gray-600 mb-6">View or edit your user login details.</p>

          {/* Profile Image */}
          <div className="flex items-center mb-6">
            <div className="w-24 h-24 rounded-full overflow-hidden flex justify-center items-center bg-gray-200">
              {previewImage ? (
                <img src={previewImage} alt="Profile" className="w-full h-full object-cover" />
              ) : (
                <div className="w-24 h-24 bg-white rounded-full"></div>
              )}
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="ml-4"
            />
          </div>

          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">ID</label>
              <p className="mt-0 text-gray-900">{userData.id.toLocaleString() || 'N/A'}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Status</label>
              <p className="mt-0 text-gray-900">{userData.status.toLocaleString() || 'N/A'}</p>
            </div>

            {/* User Fields */}
            {['username', 'first_name', 'last_name', 'email', 'phone_number'].map((field) => (
              <div key={field} className="grid grid-cols-2 gap-4">
                <label className="block text-sm font-medium text-gray-700 capitalize">{field.replace('_', ' ')}</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={userData[field] || ''}
                    onChange={(e) => handleInputChange(field, e.target.value)}
                    className="mt-1 p-2 text-gray-600 bg-gray-100 border border-gray-300 rounded w-full"
                  />
                ) : (
                  <p className="mt-0 text-gray-900">{userData[field] || 'N/A'}</p>
                )}
              </div>
            ))}

            {/*User Birthdate Field*/}
              <div className="grid grid-cols-2 gap-4">
                <label className="block text-sm font-medium text-gray-700">Birth Date</label>
                {isEditing ? (
                  <DateInput
                    name="birth_date"
                    value={userData.birth_date || ''}
                    onChange={(e) => handleInputChange('birth_date', e.target.value)}
                    required
                    type="date"
                  />
                ) : (
                  <p className="mt-0 text-gray-900">
                    {userData.birth_date ? new Date(userData.birth_date).toLocaleDateString() : 'N/A'}
                  </p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Address</label>
              {isEditing ? (
                <input
                  id="address-input"
                  type="text"
                  placeholder="Enter venue address"
                  className="input input-bordered bg-white"
                  {...register('address')}
                />
              ) : (
                <p className="mt-0 text-gray-900">{userData.address || 'N/A'}</p>
              )}
            </div>

            {isEditing && (
              <Map onMapClick={handleMapClick} setError={setError} />
            )}

            {error && <div className="text-red-500">{error}</div>}


            {/* User Fields */}
            {['nationality', 'facebook_profile', 'instagram_handle'].map((field) => (
              <div key={field} className="grid grid-cols-2 gap-4">
                <label className="block text-sm font-medium text-gray-700 capitalize">{field.replace('_', ' ')}</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={userData[field] || ''}
                    onChange={(e) => handleInputChange(field, e.target.value)}
                    className="mt-1 p-2 text-gray-600 bg-gray-100 border border-gray-300 rounded w-full"
                  />
                ) : (
                  <p className="mt-0 text-gray-900">{userData[field] || 'N/A'}</p>
                )}
              </div>
            ))}

            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Attended Events</label>
              <p className="mt-0 text-gray-900">{userData.attended_events_count.toLocaleString() || 'N/A'}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <label className="block text-sm font-medium text-gray-700">Cancelled Events</label>
              <p className="mt-0 text-gray-900">{userData.cancelled_events_count.toLocaleString() || 'N/A'}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
            <label className="block text-sm font-medium text-gray-700">Account Created</label>
            <p className="mt-0 text-gray-900">
              {userData.created_at ? 
                new Date(userData.created_at).toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' }) + 
                " " + 
                new Date(userData.created_at).toLocaleTimeString("en-US", { hour: '2-digit', minute: '2-digit' }) 
                : 'N/A'}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <label className="block text-sm font-medium text-gray-700">Account Updated</label>
            <p className="mt-0 text-gray-900">
              {userData.updated_at ? 
                new Date(userData.updated_at).toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' }) + 
                " " + 
                new Date(userData.updated_at).toLocaleTimeString("en-US", { hour: '2-digit', minute: '2-digit' }) 
                : 'N/A'}
            </p>
          </div>


            {/* Edit and Save/Cancel Buttons */}
            {isEditing ? (
              <div className="flex mt-6 space-x-4">
                <button onClick={handleSaveChanges} className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition duration-200">
                  Save Changes
                </button>
                <button onClick={handleEditToggle} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition duration-200">
                  Cancel
                </button>
              </div>
            ) : (
              <button onClick={handleEditToggle} className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition duration-200">
                Edit Profile
              </button>
            )}
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default AccountInfo;
