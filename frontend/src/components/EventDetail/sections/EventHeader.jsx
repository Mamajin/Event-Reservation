import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUsers, FaTicketAlt } from 'react-icons/fa';
import { format } from 'date-fns';


export function EventHeader({ event }) {
  const isRegistrationOpen = new Date(event.end_date_register) > new Date();
  const isFreeEvent = event.is_free || event.ticket_price === 0;
  
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
  
  return (
    <div className="relative h-[40vh] min-h-[400px] w-full pr-5">
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{ 
          backgroundImage: `url(${event.event_image || 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?q=80&w=2070'})`,
        }}
      >
        <div className="absolute inset-0 bg-black/50" />
      </div>
      <div className="absolute inset-0 flex items-end">
        <div className="container pb-8">
          <div className="flex flex-col pl-5 gap-4">
            <div className="flex items-center gap-2">
             <div className="badge bg-dark-purple text-sm text-black font-medium badge-lg">{event.category}</div>
              {event.is_online && (
                <div className="badge badge-outline badge-lg">Online Event</div>
              )}
            </div>
            <h1 className="text-4xl font-bold text-white">
              {event.event_name}
            </h1>
            <div className="flex flex-wrap gap-6 text-white/90">
              <div className="flex items-center gap-2">
                <FaCalendarAlt className="h-5 w-5" />
                <span className="text-lg">
                  {format(new Date(event.start_date_event), 'MMM d, yyyy')}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <FaClock className="h-5 w-5" />
                <span className="text-lg">
                  {format(new Date(event.start_date_event), 'h:mm a')}
                </span>
              </div>
              {!event.is_online && (
                <div className="flex items-center gap-2">
                  <FaMapMarkerAlt className="h-5 w-5" />
                  <p
                    className="text-lg cursor-pointer"
                    onClick={handleLocation}
                  >
                     {event.address ? (event.address.length > 50 ? event.address.slice(0, 50) + "..." : event.address) : "View Location"}
                  </p>

                </div>
              )}
              <div className="flex items-center gap-2">
                <FaUsers className="h-5 w-5" />
                <span className="text-lg">{event.max_attendee} attendees max</span>
              </div>
              <div className="flex items-center gap-2">
                <FaTicketAlt className="h-5 w-5" />
                <span className="text-lg">{isFreeEvent ? 'Free' : `$${event.ticket_price}`}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
