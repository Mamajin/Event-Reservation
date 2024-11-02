import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from "../constants";

function AccountInfo() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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
          <p className="text-gray-600 mb-6">See your user login details.</p>

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
              <div>
                <label className="block text-sm font-medium text-gray-700">Username</label>
                <p className="mt-0 text-gray-900">{userData.username || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <p className="mt-0 text-gray-900">{userData.status || 'N/A'}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">First Name</label>
                <p className="mt-0 text-gray-900">{userData.first_name || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Last Name</label>
                <p className="mt-0 text-gray-900">{userData.last_name || 'N/A'}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Email</label>
                <p className="mt-0 text-gray-900">{userData.email || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Mobile Phone</label>
                <p className="mt-0 text-gray-900">{userData.phone_number || 'N/A'}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Birth Date</label>
                <p className="mt-0 text-gray-900">{userData.birth_date || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Address</label>
                <p className="mt-0 text-gray-900">{userData.address || 'N/A'}</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Company</label>
              <p className="mt-0 text-gray-900">{userData.company || 'N/A'}</p>
            </div>

            {/* Social and Event Info */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Facebook Profile</label>
                <p className="mt-0 text-gray-900">{userData.facebook_profile || 'N/A'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Instagram Handle</label>
                <p className="mt-0 text-gray-900">{userData.instagram_handle || 'N/A'}</p>
              </div>
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
        </div>
      </div>
    </PageLayout>
  );
}

export default AccountInfo;