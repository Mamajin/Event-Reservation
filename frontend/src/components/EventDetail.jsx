import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { FaRegBookmark, FaRegHeart, FaShareAlt, FaArrowLeft } from 'react-icons/fa';

function EventDetail() {
  const { eventId } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [applyError, setApplyError] = useState(null);
  const [applySuccess, setApplySuccess] = useState(false);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await api.get(`/events/${eventId}`);
        setEvent(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [eventId]);

  const handleBackClick = () => {
    navigate(-1);
  };
  
  const handleApplyEvent = async () => {
    setLoading(true);
    setApplyError(null);
    setApplySuccess(false);

    try {
      const response = await api.post(`/tickets/event/${event.id}/reserve`);
      if (response.status === 200 || response.status === 201) {
        setApplySuccess(true);
      } else {
        setApplyError("An unexpected error occurred.");
      }
    } catch (err) {
      setApplyError(err.response?.data?.message || "Failed to apply for the event.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center mt-8">Loading...</div>;
  }

  if (error) {
    return (
      <div className="text-center mt-8 text-red-500">
        Error fetching event details: {error.message}
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-8 relative">
      <button className="absolute top-4 left-4 p-2" onClick={handleBackClick}>
        <FaArrowLeft className="text-gray-500" />
      </button>
      <div className="flex items-center mt-4">
        <FaRegHeart className="text-gray-500 mr-4 cursor-pointer ml-auto" />
        <FaRegBookmark className="text-gray-500 mr-4 cursor-pointer ml-3" />
        <FaShareAlt className="text-gray-500 cursor-pointer ml-3" />
      </div>
      <h1 className="text-5xl text-dark-purple mb-5 font-bold break-words max-w-full">{event?.event_name}</h1>
      <div className="flex items-center space-x-3 mb-6">
        <div className="avatar placeholder">
          <div className="bg-gradient-to-r from-slate-300 to-amber-500 w-10 h-10 flex items-center justify-center rounded-full">
            <span className="text-2xl text-dark-purple font-bold">
              {event.organizer.organizer_name.charAt(0)}
            </span>
          </div>
        </div>
        <div>
          <p className="text-dark-purple text-lg font-medium">{event.organizer.organizer_name}</p>
          <p className="text-sm text-gray-600">{event.organizer.email}</p>
        </div>
      </div>
      <img
        className="w-full h-64 object-cover rounded-lg mb-6"
        src="https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"
        alt="Event"
      />
      <div className="mb-6">
        <p className="text-lg">
          <span className="font-semibold text-dark-purple mr-2">Event Dates:</span>
          {new Date(event.start_date_event).toLocaleDateString()} - {new Date(event.end_date_event).toLocaleDateString()}
        </p>
        <p className="text-lg">
          <span className="font-semibold text-dark-purple mr-2">Registration Period:</span>
          {new Date(event.start_date_register).toLocaleDateString()} - {new Date(event.end_date_register).toLocaleDateString()}
        </p>
      </div>
      <div className="mb-6">
        <p className="text-lg">
          <span className="font-semibold text-dark-purple mr-2">Max Attendees:</span>
          {event.max_attendee}
        </p>
      </div>
      <div className="mb-6">
        <p className="text-lg">
          <span className="font-semibold text-dark-purple">Event Description:</span>
        </p>
        <p className="mt-2 text-gray-700 break-words max-w-full">{event.description}</p>
      </div>
      {applyError && <div className="text-red-500 mb-2">{applyError}</div>}
      <button
        className="btn bg-amber-300 text-dark-purple"
        onClick={handleApplyEvent}
        disabled={loading}
      >
        {loading ? "Applying..." : "Apply Event"}
      </button>
      {applySuccess && <div className="text-green-500">Successfully applied for the event!</div>}
    </div>
  );
}

export default EventDetail;