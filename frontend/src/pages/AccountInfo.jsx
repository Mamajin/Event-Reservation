import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import DateInput from '../components/DateInput';
import Map from '../components/Map';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN, USER_STATUS, PROFILE_PICTURE } from "../constants";
import Loading from '../components/LoadingIndicator';
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
        if (!token) throw new Error("No access token found");

        const response = await api.get('/users/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.headers["content-type"].includes("text/html")) {
          throw new Error("Expected JSON but received HTML response");
        }

        const data = response.data;
        setUserData(data);
        setIsOrganizer(data[USER_STATUS] === 'Organizer');
        setValue('address', data.address);
        setValue('latitude', data.latitude);
        setValue('longitude', data.longitude);
        if (data.profile_picture) setPreviewImage(data.profile_picture);
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
  }, [navigate, setValue]);

  const handleEditToggle = () => setIsEditing(!isEditing);

  const handleInputChange = (field, value) => {
    setUserData((prevData) => ({ ...prevData, [field]: value }));
  };

  const handleSaveChanges = async () => {
    if (!validateSocialLinks() || !validatePhoneNumber()) return;
  
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
        headers: { Authorization: `Bearer ${token}` },
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
      setPreviewImage(URL.createObjectURL(file));
      uploadProfilePicture(file);
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
      localStorage.setItem(PROFILE_PICTURE, response.data.file_url);
    } catch (err) {
      console.error("Error uploading profile picture:", err.message);
      alert("Failed to upload profile picture. Please try again.");
    }
  };

  const handleMapClick = (address, latitude, longitude) => {
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

  const validateSocialLinks = () => {
    const facebookPattern = /^https?:\/\/(www\.)?facebook\.com\/.+$/i;
    const instagramPattern = /^https?:\/\/(www\.)?instagram\.com\/.+$/i;
  
    const isFacebookValid = !userData.facebook_profile || facebookPattern.test(userData.facebook_profile);
    const isInstagramValid = !userData.instagram_handle || instagramPattern.test(userData.instagram_handle);
  
    return isFacebookValid && isInstagramValid;
  };

  const validatePhoneNumber = () => {
    const phoneNumberPattern = /^\d{10}$/;
    const isPhoneNumberValid = !userData.phone_number || phoneNumberPattern.test(userData.phone_number);
    return isPhoneNumberValid;
  };
  

  const goToOrganizerInfo = () => navigate('/organizer-info');

  if (loading) {
    return (
      <Loading></Loading>
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
          <div className="relative">
            <div className="absolute top-4 right-4 text-4xl font-bold text-light-purple">
              EventEase
            </div>
          </div>
  
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
  
          {/* Profile picture and user details layout */}
          <div className="flex gap-8">
            {/* Profile Picture Section */}
            <div className="flex flex-col items-center space-y-4">
              <div className="w-36 h-36 rounded-full overflow-hidden bg-gray-200 border-4 border-yellow-500">
                {previewImage ? (
                  <img
                    src={previewImage}
                    alt="Profile"
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full bg-white"></div>
                )}
              </div>
              {isEditing && (
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="text-center"
                />
              )}
            </div>

  
            {/* User Details Section */}
            <div className="ml-10 space-y-6">
              <div className="grid grid-cols-2">
              <div>
                <label className="block text-l font-medium text-gray-700">Status</label>
                <p
                  className={`mt-0 text-gray-900 font-bold ${
                    userData.status === 'Organizer'
                      ? 'text-orange-300' // Dark orange for Organizer
                      : userData.status === 'Attendee'
                      ? 'text-red-700' // Dark red for Attendee
                      : ''
                  }`}
                >
                  {userData.status?.toLocaleString() || 'N/A'}
                </p>
              </div>
              </div>

              <div>
              <div key="username" className="grid grid-cols-2">
                <label className="block text-l font-medium text-gray-700">Username</label>
                <p className="mt-0 text-gray-900">{userData.username || 'N/A'}</p>
              </div>
              </div>
  
              {['first_name', 'last_name', 'email'].map((field) => (
                <div key={field} className="grid grid-cols-2">
                  <label className="block text-l font-medium text-gray-700 capitalize">
                    {field.replace('_', ' ')}
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={userData[field] || ''}
                      onChange={(e) => handleInputChange(field, e.target.value)}
                      className="mt-1 p-2 text-gray-600 bg-gray-100 border border-gray-300 rounded w-full"
                      placeholder={field.replace('_', ' ')}
                    />
                  ) : (
                    <p className="mt-0 text-gray-900">{userData[field] || 'N/A'}</p>
                  )}
                </div>
              ))}

              <div key="phone_number" className="grid grid-cols-2">
                <label className="block text-l font-medium text-gray-700">Phone Number</label>
                {isEditing ? (
                  <>
                    <input
                      type="text"
                      value={userData.phone_number || ''}
                      onChange={(e) => handleInputChange('phone_number', e.target.value)}
                      className={`mt-1 p-2 text-gray-600 bg-gray-100 border ${error?.phone_number ? 'border-red-500' : 'border-gray-300'} rounded w-full`}
                      placeholder="Must only be 10 digits"
                    />
                    {error?.phone_number && (
                      <p className="text-red-500 text-sm mt-1">{error.phone_number}</p>
                    )}
                  </>
                ) : (
                  <p className="mt-0 text-gray-900">{userData.phone_number || 'N/A'}</p>
                )}
              </div>

  
              <div className="grid grid-cols-2">
                <label className="block text-l font-medium text-gray-700">Birth Date</label>
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
                    {userData.birth_date
                      ? new Date(userData.birth_date).toLocaleDateString()
                      : 'N/A'}
                  </p>
                )}
              </div>
  
              {/* Address and Map Section */}
              <div className="grid grid-cols-2">
                <label className="block text-l font-medium text-gray-700">Address</label>
                {isEditing ? (
                  <input
                    id="address-input"
                    type="text"
                    placeholder="Enter venue address"
                    className="input input-bordered text-gray-600 bg-gray-100 border border-gray-300"
                    {...register('address')}
                  />
                ) : (
                  <p className="mt-0 text-gray-900">{userData.address || 'N/A'}</p>
                )}
              </div>
  
              {isEditing && <Map onMapClick={handleMapClick} setError={setError} />}
              {error && <div className="text-red-500">{error}</div>}
  
              {/* Nationality and Social Links */}
              <div className="grid grid-cols-2">
                <label className="block text-l font-medium text-gray-700">Nationality</label>
                {isEditing ? (
                  <input
                    type="text"
                    value={userData.nationality || ''}
                    onChange={(e) => handleInputChange('nationality', e.target.value)}
                    className="mt-1 p-2 text-gray-600 bg-gray-100 border border-gray-300 rounded w-full"
                    placeholder="Nationality"
                  />
                ) : (
                  <p className="mt-0 text-gray-900">{userData.nationality || 'N/A'}</p>
                )}
              </div>

              {['facebook_profile', 'instagram_handle'].map((field) => (
              <div key={field} className="grid grid-cols-2">
                <label className="block text-l font-medium text-gray-700">
                  {field.replace('_', ' ').replace(/\b\w/g, (char) => char.toUpperCase())}
                </label>
                {isEditing ? (
                  <>
                    <input
                      type="text"
                      value={userData[field] || ''}
                      onChange={(e) => handleInputChange(field, e.target.value)}
                      className={`mt-1 p-2 text-gray-600 bg-gray-100 border ${
                        error?.[field] ? 'border-red-500' : 'border-gray-300'
                      } rounded w-full`}
                      placeholder={`Use a valid link or empty`}
                    />
                    {error?.[field] && (
                      <p className="text-red-500 text-sm mt-1">{error[field]}</p>
                    )}
                  </>
                ) : userData[field] ? (
                  <a
                    href={userData[field]}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 underline hover:text-blue-700"
                  >
                    {field === 'facebook_profile' ? 'Facebook' : 'Instagram'}
                  </a>
                ) : (
                  <p className="text-gray-500">N/A</p>
                )}
              </div>
            ))}

            </div>
          </div>
  
          {/* Footer with account information inside the box */}
          <div className="mt-6 text-xs text-right text-gray-500">
            <p>Account created: {new Date(userData.created_at).toLocaleDateString()}</p>
            <p>Last updated: {new Date(userData.updated_at).toLocaleDateString()}</p>
            <p>Attended events: {userData.attended_events || 0}</p>
            <p>Cancelled events: {userData.cancelled_events || 0}</p>
          </div>
  
          {/* Save and Edit buttons */}
          <div className="flex justify-between space-x-4 mt-6">
            {isEditing && (
              <button
                onClick={handleSubmit(handleSaveChanges)}
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition duration-200"
              >
                Save Changes
              </button>
            )}
  
            <button
              onClick={handleEditToggle}
              className={`px-4 py-2 text-white rounded ${
                isEditing
                  ? 'bg-red-500 hover:bg-red-600'
                  : 'bg-blue-500 hover:bg-blue-600'
              } transition duration-200`}
            >
              {isEditing ? 'Cancel' : 'Edit Profile'}
            </button>
          </div>
        </div>
      </div>
    </PageLayout>
  );  
}

export default AccountInfo;
