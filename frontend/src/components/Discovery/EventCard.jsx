import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LuClock, LuCalendar, LuUsers, LuBadgeCheck, LuHeart, LuBookmark, LuTag } from 'react-icons/lu';
import { ACCESS_TOKEN } from '../../constants';
import api from '../../api';
import { useNavigate } from 'react-router-dom';

const EventCard = ({ event }) => {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(event?.engagement?.total_likes || 0);
  const [bookmarkCount, setBookmarkCount] = useState(event?.engagement?.total_bookmarks || 0);
  const navigate = useNavigate();
  
  useEffect(() => {
    if (event?.user_engaged) {
      setIsLiked(event.user_engaged.is_liked);
      setIsBookmarked(event.user_engaged.is_bookmarked);
    }
  }, [event]);

  const handleMoreDetailClick = () => {
    navigate(`/events/${event.id}`);
  };

  const handleLike = async (eventId) => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      await api.put(`/likes/${eventId}/toggle-like`, {}, { headers });
      setIsLiked(!isLiked);
      setLikeCount((prev) => (isLiked ? prev - 1 : prev + 1));
    } catch (error) {
      console.error('Error liking event:', error);
      alert('Failed to like the event. Please try again.');
    }
  };
  
  const handleBookmark = async (eventId) => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      await api.put(`/bookmarks/${eventId}/toggle-bookmark`, {}, { headers });
      setIsBookmarked(!isBookmarked);
      setBookmarkCount((prev) => (isBookmarked ? prev - 1 : prev + 1));
    } catch (error) {
      console.error('Error bookmarking event:', error);
    }
  };
  if (!event) return null;

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };
  
  const tags = event.tags ? event.tags.split(',').filter(Boolean) : [];

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
        <h3 className="absolute bottom-4 left-4 text-xl font-semibold text-white cursor-pointer" onClick={handleMoreDetailClick}>
          {event.event_name}
        </h3>
        <div className="absolute top-4 right-4 flex gap-2">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => handleLike(event.id)}
            className={`flex h-8 items-center gap-1 p-2 rounded-full bg-white/90 backdrop-blur-sm shadow-sm transition-colors ${
              isLiked? 'text-red-500' : 'text-gray-600 hover:text-red-500'
            }`}
          >
            <LuHeart className="h-5 w-5" fill={isLiked ? 'currentColor' : 'none'}/>
            <span className="text-sm font-medium">{likeCount}</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => handleBookmark(event.id)}
            className={`flex h-8 items-center gap-1 p-2 rounded-full bg-white/90 backdrop-blur-sm shadow-sm transition-colors ${
              isBookmarked ? 'text-yellow-500' : 'text-gray-600 hover:text-yellow-500'
            }`}
          >
            <LuBookmark
              className="h-5 w-5"
              fill={isBookmarked ? 'currentColor' : 'none'}
            />
            <span className="text-sm font-medium">{bookmarkCount}</span>
          </motion.button>
        </div>
        <div className="absolute top-4 text-white left-4 badge bg-dark-purple">
          {event.status.charAt(0) + event.status.slice(1).toLowerCase()}
        </div>
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
      <div className="space-y-4">
          <div className="flex gap-2 overflow-x-auto scrollbar-hide">
            <span className="badge bg-dark-purple text-white" variant={event.is_free ? 'success' : 'default'}>
              {event.is_free ? 'Free' : 'Paid'}
            </span>
            <span className="badge bg-dark-purple text-white" variant="secondary">
              {event.category.charAt(0) + event.category.slice(1).toLowerCase()}
            </span>
            {tags.map((tag) => (
              <span className="badge bg-dark-purple text-white flex-shrink-0" key={tag} variant="default">
                <LuTag className="h-3 w-3 mr-1" />
                {tag.trim()}
              </span>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default EventCard;