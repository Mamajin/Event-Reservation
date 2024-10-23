import { useEffect, useState } from 'react';
import axios from 'axios';
import { ACCESS_TOKEN } from "../constants";

const useUserProfile = (navigate) => {
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
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

        console.log('User profile response:', response.data); // Log the user profile response
        setUserId(response.data.id); // Set the user ID from the response

      } catch (err) {
        if (err.message === 'No access token found') {
          alert('You are not logged in. Redirecting to login page...');
          navigate('/login'); // Redirect to login if token is missing
        } else {
          setError(err); // Handle other errors
        }
      } finally {
        setLoading(false); // Set loading to false after fetching
      }
    };

    fetchUserProfile();
  }, [navigate]); // Run the effect when navigate changes

  return { userId, loading, error }; // Return userId, loading, and error
};

export default useUserProfile;
