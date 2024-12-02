import { LuCalendar, LuMapPin, LuTag, LuUsers } from 'react-icons/lu';
import { useNavigate } from 'react-router-dom';
import React from 'react';
function EventCard({ event }) {
    const navigate = useNavigate();
  
    const handleMoreDetailClick = () => {
      navigate(`/events/${event.id}`);
    };
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
          return 'Date not available';
        }
        return new Intl.DateTimeFormat('en-US', {
          month: 'long',
          day: 'numeric',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        }).format(date);
      };
      const handleLocation = () => {
        const latitude = event.latitude;
        const longitude = event.longitude;
        const address = event.address;
    
        // Check if the address is available and use it, otherwise fall back to coordinates
        const googleMapsLink = address
          ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`
          : `https://www.google.com/maps/search/?api=1&query=${latitude},${longitude}`;
    
        window.open(googleMapsLink, "_blank");
      };

      const truncateAddress = (address, maxLength = 30) => {
        if (address.length > maxLength) {
          return `${address.substring(0, maxLength)}...`;
        }
        return address;
      };
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"onClick={handleMoreDetailClick}>
      <div className="relative h-48">
        <img
          src={event.event_image || 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&q=80'}
          alt={event.event_name}
          className="w-full h-full object-cover"
        />
        {event.is_verified && (
          <div className="absolute top-4 right-4 bg-blue-500 text-white px-2 py-1 rounded-full text-xs">
            Verified
          </div>
        )}
      </div>
      
      <div className="p-6">
        <div className="flex items-center gap-2 mb-2">
          <LuTag className="w-4 h-4 text-blue-500" />
          <span className="text-sm text-blue-500">{event.category}</span>
        </div>
        
        <h3 className="text-xl text-black font-semibold mb-2 cursor-pointer" >{event.event_name}</h3>
        
        <div className="flex items-center gap-2 text-gray-600 mb-2">
          <LuCalendar className="w-4 h-4" />
          <span className="text-sm">{formatDate(event.start_date_event)}</span>
        </div>
        
        <div className={`flex items-center gap-2 text-gray-600 mb-4 line-clamp-1 ${event.is_online ? '' : 'cursor-pointer'}`} onClick={event.is_online ? null : handleLocation}>
            <LuMapPin className="w-4 h-4" />
            <span className="text-sm">{event.is_online ? 'Online Event' : truncateAddress(event.address)}</span>
        </div>


        
        <div className="flex items-center gap-2 text-gray-600">
          <LuUsers className="w-4 h-4" />
          <span className="text-sm">{event.current_attendees}/{event.max_attendee} attendees</span>
        </div>
        
        <div className="mt-4 flex items-center justify-between">
          <div>
            {event.is_free ? (
              <span className="text-green-500 font-semibold">Free</span>
            ) : (
              <span className="text-gray-900 font-semibold">{event.ticket_price} ฿</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default EventCard;
