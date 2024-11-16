import React, { useState, useEffect } from 'react';
import { FaBookmark, FaRegBookmark } from 'react-icons/fa';
import api from '../../api';
import { ACCESS_TOKEN } from '../../constants';

const BookmarkButton = ({ eventId }) => {
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    const fetchInitialBookmarkState = async () => {
      try {
        const response = await api.get(`/events/${eventId}/user-engagement`, {
          headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
        });

        const isBookmarked = response.data?.is_bookmarked ?? false;
        setBookmarked(isBookmarked);
      } catch (error) {
        console.error("Failed to fetch bookmark state:", error);
      }
    };

    fetchInitialBookmarkState();
  }, [eventId]);

  const handleToggleBookmark = async () => {
    setLoading(true);
    setErrorMessage(null);

    try {
      const newBookmarkState = !bookmarked;
      setBookmarked(newBookmarkState);

      await api.put(`/bookmarks/${eventId}/toggle-bookmark`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
      });
    } catch (error) {
      setBookmarked(!bookmarked);

      setErrorMessage(
        error.response?.data?.message || "An error occurred. Please try again."
      );
      console.error("Error toggling bookmark:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div onClick={handleToggleBookmark} className="cursor-pointer">
      {bookmarked ? (
        <FaBookmark
          className={`text-blue-500 ${loading ? 'opacity-50 pointer-events-none' : ''}`}
        />
      ) : (
        <FaRegBookmark
          className={`text-gray-500 hover:text-blue-500 ${loading ? 'opacity-50 pointer-events-none' : ''}`}
        />
      )}
      {errorMessage && (
        <p className="text-red-500 text-xs mt-1">{errorMessage}</p>
      )}
    </div>
  );
};

export default BookmarkButton;
