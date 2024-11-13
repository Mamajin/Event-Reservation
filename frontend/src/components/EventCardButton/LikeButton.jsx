import React, { useState, useEffect } from 'react';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import api from '../../api';
import { ACCESS_TOKEN } from '../../constants';

const LikeButton = ({ eventId, isInitiallyLiked }) => {
  const [liked, setLiked] = useState(null); // Initially null until we know the state
  const [loading, setLoading] = useState(false); // Track loading state
  const [errorMessage, setErrorMessage] = useState(null); // Track errors

  // Sync the like state when the component mounts or when the 'isInitiallyLiked' prop changes
  useEffect(() => {
    // Check localStorage to see if this event has been liked
    const storedLiked = localStorage.getItem(`liked-${eventId}`);
    
    // If we have a stored value, use it, otherwise use the initial prop
    if (storedLiked !== null) {
      setLiked(JSON.parse(storedLiked)); // Use stored value from localStorage
    } else {
      setLiked(isInitiallyLiked); // Use prop if no stored value
    }
  }, [eventId, isInitiallyLiked]);

  const handleLike = async () => {
    if (loading) return; // Prevent clicking while loading

    setLoading(true);
    setErrorMessage(null); // Clear any previous error messages
    const token = localStorage.getItem(ACCESS_TOKEN); // Get token for authentication

    try {
      let response;
      if (liked) {
        // Send the unlike request if currently liked
        response = await api.delete(`/likes/unlike/${eventId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        // Send the like request if currently unliked
        response = await api.post(`/likes/like/${eventId}`, {}, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }

      if (response.status === 200) {
        const newLikedState = !liked;
        setLiked(newLikedState); // Toggle the liked state after a successful request

        // Store the new state in localStorage to persist it after page refresh
        localStorage.setItem(`liked-${eventId}`, JSON.stringify(newLikedState));
      }
    } catch (error) {
      // Handle errors, show error message if any
      if (error.response && error.response.data && error.response.data.error) {
        setErrorMessage(error.response.data.error);
      } else {
        console.error("Error toggling like:", error);
      }
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  if (liked === null) {
    // If we haven't received the state yet, return a loading state or a placeholder
    return <div className="animate-pulse">...</div>;
  }

  return (
    <div onClick={handleLike} className="cursor-pointer">
      {liked ? (
        <FaHeart
          className={`text-red-500 ${loading ? 'opacity-50 pointer-events-none' : ''}`}
        />
      ) : (
        <FaRegHeart
          className={`text-gray-500 hover:text-red-500 ${loading ? 'opacity-50 pointer-events-none' : ''}`}
        />
      )}
      {errorMessage && (
        <p className="text-red-500 text-xs mt-1">{errorMessage}</p> // Display error message if any
      )}
    </div>
  );
};

export default LikeButton;
