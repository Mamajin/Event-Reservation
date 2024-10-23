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
    return <div>Loading...</div>;
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
      <h2 className="text-2xl font-bold mb-4">Account Information</h2>
      <div className="info">
        <p><strong>Username:</strong> {userData.username || 'Unknown'}</p>
        <p><strong>Email:</strong> {userData.email || 'Unknown'}</p>
        <p><strong>First Name:</strong> {userData.firstname || 'Unknown'}</p>
        <p><strong>Last Name:</strong> {userData.lastname || 'Unknown'}</p>
        <p><strong>Phone Number:</strong> {userData.phonenumber || 'Unknown'}</p>
        <p><strong>Status:</strong> {userData.status || 'Unknown'}</p>
      </div>
    </PageLayout>
  );
}

export default AccountInfo;
