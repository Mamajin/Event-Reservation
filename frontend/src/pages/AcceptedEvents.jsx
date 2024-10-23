import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { ACCESS_TOKEN } from "../constants";

function AcceptedEvent() {
  const [userData, setUserData] = useState(null); // Initially null
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate here

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        console.log('Token:', token);
        if (!token) {
          throw new Error('No access token found'); // Handle missing token
        }

        const response = await axios.get('http://localhost:8000/api/users/profile', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const organizer = response.data[0]?.organizer;
        if (organizer?.user) {
          setUserData(organizer.user); // Set the fetched user data
        } else {
          setUserData({
            username: 'Unknown',
            email: 'Unknown',
            firstname: 'Unknown',
            lastname: 'Unknown',
            phonenumber: 'Unknown',
            status: 'Unknown',
          });
        }
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
      <h2 className="text-2xl font-bold mb-4">Accepted Events</h2>
      <div className="info">
        <p><strong>Place-holder</strong></p>
      </div>
    </PageLayout>
  );
}

export default AcceptedEvent;
