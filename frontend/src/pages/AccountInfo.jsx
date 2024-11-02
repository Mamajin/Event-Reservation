import React, { useEffect, useState } from 'react';
import axios from 'axios';
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

        const response = await axios.get("/users/profile", {
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
            <div>
              <label className="block text-sm font-medium text-gray-700">ID</label>
              <p className="mt-0 text-gray-900">{userData.id || 'N/A'}</p>
            </div>
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
            {/* Additional fields can be added here */}
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default AccountInfo;