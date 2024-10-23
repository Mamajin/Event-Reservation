import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { ACCESS_TOKEN } from "../constants";

function AccountInfo() {
  const [userData, setUserData] = useState(null); // Initially null
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate here

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
          throw new Error('No access token found'); // Handle missing token
        }

        const response = await axios.get('http://localhost:8000/api/users/profile', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log('API response:', response.data); // Log the API response

        // Assuming response.data is a single user object, update the state
        setUserData(response.data);

      } catch (err) {
        if (err.message === 'No access token found') {
          alert('You are not logged in. Redirecting to login page...');
          navigate('/login'); // Redirect to login if token is missing
        } else {
          setError(err); // Handle other errors
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [navigate]); // Add 'navigate' as a dependency

  if (loading) {
    return (
      <PageLayout>
        <h2 className="text-2xl font-bold mb-4">Applied Events</h2>
          <div className="grid grid-cols-1 gap-4">
            <div>Loading...</div>
          </div>
      </PageLayout>
  );
  }

  if (error) {
    return <div>Error fetching user data: {error.message}</div>;
  }

  // Ensure userData is available before rendering its properties
  if (!userData) {
    return <div>No user data available</div>;
  }

  return (
    <PageLayout>
        <div className="flex justify-end items-start min-h-screen bg-white-100 p-4">
            <div className="w-full max-w-xs bg-white rounded-lg shadow-lg p-6 space-y-4">
                <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Account Information</h2>
                <div className="info space-y-2">
                    <p className="text-lg"><strong>ID:</strong> {userData.id || 'Unknown'}</p>
                    <p className="text-lg"><strong>Username:</strong> {userData.username || 'Unknown'}</p>
                    <p className="text-lg"><strong>Email:</strong> {userData.email || 'Unknown'}</p>
                    <p className="text-lg"><strong>First Name:</strong> {userData.firstname || 'Unknown'}</p>
                    <p className="text-lg"><strong>Last Name:</strong> {userData.lastname || 'Unknown'}</p>
                    <p className="text-lg"><strong>Phone Number:</strong> {userData.phonenumber || 'Unknown'}</p>
                    <p className="text-lg"><strong>Status:</strong> {userData.status || 'Unknown'}</p>
                </div>
            </div>
        </div>
    </PageLayout>
  );
}

export default AccountInfo;
