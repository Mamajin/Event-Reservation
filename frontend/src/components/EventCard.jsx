import React from 'react';
import { useNavigate } from 'react-router-dom';
import LikeButton from './EventCardButton/LikeButton';
import BookmarkButton from './EventCardButton/BookMarkButton';
import ShareButton from './EventCardButton/ShareButton';
import api from '../api';

function EventCard({ event, onEdit, isEditable}) {
  const navigate = useNavigate();
  const maxDescriptionLength = 110;

  const handleMoreDetailClick = () => {
    navigate(`/events/${event.id}`);
  };

  // Destructure engagement and provide default values in case it's null or undefined
  const { user_engaged = {} } = event;
  const hasUserLiked = user_engaged.is_liked ?? false;

  const handleDelete = async (eventId) => {
    try {
      await api.delete(`/organizers/delete-event/${eventId}`);
      window.location.reload();
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  return (
    <div className="flex bg-white shadow-lg p-4 mb-4 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer duration-200">
      <img
        className="w-1/3 h-48 object-cover rounded-lg"
        src={
          event?.event_image ||
          "https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"
        }
        alt="Event"
      />
      <div className="ml-4 flex-grow">
        <div className="flex items-center space-x-3">
          <div className="avatar placeholder">
            <div className="bg-gradient-to-r from-slate-300 to-amber-500 text-neutral-content w-6 h-6 flex items-center justify-center rounded-full">
              <span className="text-md text-dark-purple">
                {event.organizer.organizer_name.charAt(0)}
              </span>
            </div>
          </div>
          <p className="text-sm text-gray-600">{event.organizer.organizer_name}</p>
        </div>
        <h2
          className="text-3xl text-dark-purple font-bold mb-2 cursor-pointer"
          onClick={handleMoreDetailClick}
        >
          {event.event_name}
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          {new Date(event.start_date_event).toLocaleDateString()} -{' '}
          {new Date(event.end_date_event).toLocaleDateString()}
        </p>
        <p className="mt-2 text-gray-700 break-words">
          {event.description.length > maxDescriptionLength
            ? `${event.description.substring(0, maxDescriptionLength)}...`
            : event.description}
        </p>

        {/* Engagement and Share Buttons */}
        <div className="flex items-center mt-4 space-x-4">
          <LikeButton eventId={event.id} eventInfo={event} isInitiallyLiked={hasUserLiked} />
          <BookmarkButton eventId={event.id} eventInfo={event} />
          <ShareButton eventId={event.id} />
        </div>

        {isEditable && (
          <div>
            <button
              onClick={() => onEdit(event.id)}
              className="btn bg-amber-300 text-dark-purple mt-4"
            >
              Edit Event
            </button>
            <button
              onClick={() => handleDelete(event.id)}
              className="btn bg-red-500 text-white mt-4 ml-2"
            >
              Delete Event
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default EventCard;
