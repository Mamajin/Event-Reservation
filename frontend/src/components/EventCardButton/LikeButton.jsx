import React, { useState, useEffect } from 'react';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import api from '../../api';
import { ACCESS_TOKEN } from '../../constants';

const LikeButton = ({ eventId, eventInfo }) => {
  const [liked, setLiked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    if (eventInfo) {
      const isLiked = eventInfo.user_engaged?.is_liked ?? false;
      setLiked(isLiked);
    }
  }, [eventInfo]);

  const handleToggleLike = async () => {
    setLoading(true);
    setErrorMessage(null);

    try {
      const newLikedState = !liked;
      setLiked(newLikedState);

      await api.put(`/likes/${eventId}/toggle-like`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
      });
    } catch (error) {
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
