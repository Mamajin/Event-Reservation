import React from 'react';
import { useNavigate } from 'react-router-dom';

function EventCard({ event }) {
  const navigate = useNavigate();

  const handleMoreDetailClick = () => {
    navigate(`/events/${event.id}`);
  };

  return (
    <div className="card lg:card-side bg-gray-200 shadow-xl mb-4">
      <figure>
        <img
          src="https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"
          alt="Event" />
      </figure>
      <div className="card-body">
        <h2 className="card-title">{event.event_name}</h2>
        <p className="text-sm text-gray-600">Organizer: {event.organizer.organizer_name}</p>
        <p className="text-sm text-gray-600">Email: {event.organizer.email}</p>
        <p className="mt-2">{event.description}</p>
        <p className="text-sm text-gray-500">
          Date: {new Date(event.start_date_event).toLocaleDateString()} - {new Date(event.end_date_event).toLocaleDateString()}
        </p>
        <p className="text-sm text-gray-500">Max Attendees: {event.max_attendee}</p>
        <div className="card-actions justify-end">
          <button className="btn bg-amber-300 text-dark-purple" onClick={handleMoreDetailClick}>More Detail</button>
        </div>
      </div>
    </div>
  );
}

export default EventCard;