import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

function EventDetail() {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching event details: {error.message}</div>;
  }

  return (
    <div className="p-4">
        <h1 className="text-7xl text-dark-purple mb-5 font-bold">{event.event_name}</h1>
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
        <img
        className="mt-10 object-cover rounded-lg"
        src="https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"
        alt="Event"
        />
         <p className="mt-2">Organizer: {event.organizer.organizer_name}</p>
         <p>Email: {event.organizer.email}</p>
         <p className="mt-4">{event.description}</p>
         <p>Date: {new Date(event.start_date_event).toLocaleDateString()} - {new Date(event.end_date_event).toLocaleDateString()}
          </p>
        <p>Max Attendees: {event.max_attendee}</p>
    </div>
  );
}

export default EventDetail;