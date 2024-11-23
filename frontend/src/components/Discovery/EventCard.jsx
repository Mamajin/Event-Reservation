import React from 'react';
import { motion } from 'framer-motion';

const EventCard = ({ event }) => {
  if (!event) return null;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="group bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
    >
      <div className="relative">
        <img
          src={event?.event_image || "https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"}
          alt={event.event_name}
          className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <h3 className="absolute bottom-4 left-4 text-xl font-semibold text-white">
          {event.event_name}
        </h3>
      </div>
    </motion.div>
  );
};

export default EventCard;