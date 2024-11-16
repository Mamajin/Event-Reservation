import React, { useState, useEffect } from 'react';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import api from '../../api';
import { ACCESS_TOKEN } from '../../constants';

const LikeButton = ({ eventId }) => {
  const [liked, setLiked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Fetch the initial like state from the server on mount
  useEffect(() => {
    const fetchInitialLikeState = async () => {
      try {
        const response = await api.get(`/events/${eventId}/user-engagement`, {
          headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
        });

        const isLiked = response.data?.is_liked ?? false;
        setLiked(isLiked);

        // Persist the initial like state to localStorage
        localStorage.setItem(`liked-${eventId}`, JSON.stringify(isLiked));
      } catch (error) {
        console.error("Failed to fetch like state:", error);
      }
    };

    fetchInitialLikeState();
  }, [eventId]);

  const handleToggleLike = async () => {
    setLoading(true);
    setErrorMessage(null);

    try {
      // Update UI
      const newLikedState = !liked;
      setLiked(newLikedState);

      // Persist the new state locally
      localStorage.setItem(`liked-${eventId}`, JSON.stringify(newLikedState));

      // Send toggle request to the server
      await api.put(`/likes/${eventId}/toggle-like`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
      });
    } catch (error) {
      // Revert UI state on error
      setLiked(!liked);

      setErrorMessage(
        error.response?.data?.message || "An error occurred. Please try again."
      );
      console.error("Error toggling like:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div onClick={handleToggleLike} className="cursor-pointer">
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
        <p className="text-red-500 text-xs mt-1">{errorMessage}</p>
      )}
    </div>
  );
};

export default LikeButton;
