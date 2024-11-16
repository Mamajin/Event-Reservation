import React, { useState, useEffect } from 'react';
import { FaBookmark, FaRegBookmark } from 'react-icons/fa';
import api from '../../api';
import { ACCESS_TOKEN } from '../../constants';

const BookmarkButton = ({ eventId }) => {
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Fetch the initial bookmark state from the server on mount
  useEffect(() => {
    const fetchInitialBookmarkState = async () => {
      try {
        const response = await api.get(`/events/${eventId}/user-engagement`, {
          headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
        });

        const isBookmarked = response.data?.is_bookmarked ?? false;
        setBookmarked(isBookmarked);

        // Persist the initial bookmark state to localStorage
        localStorage.setItem(`bookmarked-${eventId}`, JSON.stringify(isBookmarked));
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
      // Optimistically update UI
      const newBookmarkState = !bookmarked;
      setBookmarked(newBookmarkState);

      // Persist the new state locally
      localStorage.setItem(`bookmarked-${eventId}`, JSON.stringify(newBookmarkState));

      // Send toggle request to the server
      await api.put(`/bookmarks/${eventId}/toggle-bookmark`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
      });
    } catch (error) {
      // Revert UI state on error
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
