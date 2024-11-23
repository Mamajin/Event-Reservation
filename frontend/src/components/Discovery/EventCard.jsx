import React from 'react';
import { motion } from 'framer-motion';
import { LuClock, LuCalendar, LuUsers, LuBadgeCheck } from 'react-icons/lu';

const EventCard = ({ event }) => {
  if (!event) return null;

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="group bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
    >
      <div className="relative">
        <img
          src={event?.event_image ||  "https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"} 
          alt={event.event_name}
          className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <h3 className="absolute bottom-4 left-4 text-xl font-semibold text-white">
          {event.event_name}
        </h3>
      </div>
      
      <div className="p-6">
        <div className="flex items-center mb-4">
          <img
            src={event.organizer.logo || 'https://via.placeholder.com/40'}
            alt={event.organizer.organizer_name}
            className="w-8 h-8 rounded-full ring-2 ring-white mr-3"
          />
          <div>
            <span className="text-sm font-medium text-gray-900 flex items-center">
              {event.organizer.organizer_name}
              {event.organizer.is_verified && <LuBadgeCheck className="w-4 h-4 ml-1 text-blue-500" />}
            </span>
            <p className="text-xs text-gray-500">{event.organizer.organization_type}</p>
          </div>
        </div>

        <div className="space-y-3 mb-4">
          <div className="flex items-center text-gray-600">
            <LuCalendar className="h-4 w-4 mr-2 text-indigo-500" />
            <span className="text-sm">{formatDate(event.start_date_event)}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <LuClock className="h-4 w-4 mr-2 text-indigo-500" />
            <span className="text-sm">Registration ends: {formatDate(event.end_date_register)}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <LuUsers className="h-4 w-4 mr-1" />
            <span>{event.max_attendee === null || event.max_attendee === 0 ? "No attendees limit" : `${event.max_attendee} attendees max`}</span>
          </div>
        </div>

        <p className="text-gray-600 mb-6 line-clamp-6 text-sm">{event.description}</p>
      </div>
    </motion.div>
  );
};

export default EventCard;