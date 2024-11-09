import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUsers, FaTicketAlt } from 'react-icons/fa';
import { format } from 'date-fns';

export function EventHeader({ event }) {
  return (
    <div className="relative h-[40vh] min-h-[400px] w-full">
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
          <div className="flex flex-col gap-4">
            <h1 className="text-4xl font-bold text-white">
              {event.event_name}
            </h1>
          </div>
        </div>
      </div>
    </div>
  );
}
