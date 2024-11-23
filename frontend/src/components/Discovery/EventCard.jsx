import React from 'react';

const EventCard = ({ event }) => {
  if (!event) return null;
  
  return (
    <div className="bg-white rounded-xl shadow-sm">
      <div className="relative">
        <img
          src={event?.event_image ||  "https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"}
          alt={event.event_name}
          className="w-full h-48 object-cover"
        />
        <h3 className="text-xl font-semibold p-4">{event.event_name}</h3>
      </div>
    </div>
  );
};

export default EventCard;