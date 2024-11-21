import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUsers, FaTicketAlt, FaArrowLeft } from 'react-icons/fa';
import { LuBookmark, LuShare2, LuHeart } from "react-icons/lu";
import { ACCESS_TOKEN } from '../../../constants';
import api from '../../../api';
import { useState, useEffect } from 'react';
import { format, set } from 'date-fns';
import { useNavigate } from 'react-router-dom';


export function EventHeader({ event }) {
  const isRegistrationOpen = new Date(event.end_date_register) > new Date();
  const isFreeEvent = event.is_free || event.ticket_price === 0;
  const [showShareMenu, setShowShareMenu] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (event?.user_engaged) {
      setIsLiked(event.user_engaged.is_liked);
      setIsBookmarked(event.user_engaged.is_bookmarked);
    }
  }, [event]);
  
  const handleShare = async (platform) => {
    const shareUrl = window.location.href;
    const shareText = `Check out this event: ${event.event_name}`;
  
    switch (platform) {
      case 'twitter':
        window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`);
        break;
      case 'facebook':
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`);
        break;
      case 'copy':
        try {
          await navigator.clipboard.writeText(shareUrl);
          alert('Link copied to clipboard!');
        } catch (err) {
          console.error('Failed to copy:', err);
        }
        break;
    }
    setShowShareMenu(false);
  };

  const handleLike = async (eventId) => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      await api.put(`/likes/${eventId}/toggle-like`, {}, { headers });
      setIsLiked(!isLiked);
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
      const response = await api.put(`/bookmarks/${eventId}/toggle-bookmark`, {}, { headers });
      setIsBookmarked(!isBookmarked); 
      console.log('Bookmarked:', response.data.message);
    } catch (error) {
      console.error('Error bookmarking event:', error);
    }
  };  

  const handleBackClick = () => {
    navigate(-1);
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

  return (
    <div className="relative h-[40vh] min-h-[400px] w-full pr-5">
      <div className="absolute top-4 left-4 p-2 z-10">
          <button onClick={handleBackClick}>
            <FaArrowLeft className="text-white" />
          </button>
      </div>
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: `url(${event.event_image || 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?q=80&w=2070'})`,
        }}
      >
        <div className="absolute inset-0 bg-black/50" />
        <div className="absolute top-4 right-4 flex items-center gap-2 z-10">
        <button
          onClick={() => handleLike(event.id)}
          className="button p-2 bg-white/10 backdrop-blur-md rounded-full hover:bg-white/20 transition-colors"
          title={isLiked ? 'Remove like' : 'Like event'}
        >
          <LuHeart
            className={`w-5 h-5 ${isLiked ? 'fill-white text-white' : 'text-white'}`}
          />
        </button>

        <button
          onClick={() => handleBookmark(event.id)}
          className="button p-2 bg-white/10 backdrop-blur-md rounded-full hover:bg-white/20 transition-colors"
          title={isBookmarked ? 'Remove bookmark' : 'Bookmark event'}
        >
          <LuBookmark
            className={`w-5 h-5 ${isBookmarked ? 'fill-white text-white' : 'text-white'}`}
          />
        </button>

        
        <div className="relative">
          <button
            onClick={() => setShowShareMenu(!showShareMenu)}
            className="p-2 bg-white/10 backdrop-blur-md rounded-full hover:bg-white/20 transition-colors"
            title="Share event"
          >
            <LuShare2 share2 className="w-5 h-5 text-white" />
          </button>
          {showShareMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50">
              <button
                onClick={() => handleShare('twitter')}
                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100 transition-colors"
              >
                Share on Twitter
              </button>
              <button
                onClick={() => handleShare('facebook')}
                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100 transition-colors"
              >
                Share on Facebook
              </button>
              <hr className="my-2" />
              <button
                onClick={() => handleShare('copy')}
                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100 transition-colors"
              >
                Copy Link
              </button>
            </div>
          )}
        </div>
      </div>
        </div>
      <div className="absolute inset-0 flex items-end">
        <div className="container pb-8">
          <div className="flex flex-col pl-5 gap-4">
            <div className="flex items-center gap-2">
              <div className="badge bg-dark-purple text-sm text-white font-medium badge-lg">{event.category}</div>
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
                <span className="text-lg">
                  {event.max_attendee === null ? "No attendees limit" : `${event.max_attendee} attendees max`}
                </span>

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
