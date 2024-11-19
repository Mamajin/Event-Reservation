import React from 'react';
import { FaShareAlt } from 'react-icons/fa';

const ShareButton = ({ eventId }) => {
  const handleShare = async () => {
    const eventUrl = `${window.location.origin}/events/${eventId}`;

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Check out this event!',
          text: 'Take a look at this amazing event:',
          url: eventUrl,
        });
      } catch (error) {
        console.error('Error sharing:', error);
      }
    } else {
      try {
        await navigator.clipboard.writeText(eventUrl);
        alert('Event link copied to clipboard!');
      } catch (error) {
        console.error('Error copying to clipboard:', error);
        alert('Failed to copy link. Please try again.');
      }
    }
  };

  return (
    <button onClick={handleShare} className="cursor-pointer text-gray-500 hover:text-green-500 active:text-green-600">
      <FaShareAlt />
    </button>
  );
};

export default ShareButton;
