import React, { useEffect, useState } from 'react';
import api from '../api';
import EventCard from '../components/EventCard';
import PageLayout from '../components/PageLayout';
import { useNavigate,Link } from 'react-router-dom';
import {USER_STATUS} from '../constants'

export default function Home() {
  const [latestEvents, setLatestEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const isOrganizer = localStorage.getItem(USER_STATUS) === "Organizer";
  const navigate = useNavigate(); 


  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await api.get('/events/events');
        const sortedEvents = response.data.slice().sort((a, b) => new Date(b.start_date_event) - new Date(a.start_date_event));
        setLatestEvents(sortedEvents.slice(0, 3));
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);
  const handleCreateEventClick = () => {
    if (isOrganizer) {
      navigate('/create-event');
    } else {
      navigate('/become-organizer');
    }
  };
  return (
    <PageLayout>
      <div className='pr-6 pt-4'>
      <div className="hero h-screen bg-cover bg-center " style={{ backgroundImage: `url('https://i.pinimg.com/564x/92/57/6b/92576be9601f00886b03e58363369647.jpg')` }}>
        <div className="hero-overlay bg-opacity-60 bg-black"></div>
        <div className="hero-content text-center text-neutral-content">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold text-white mb-4">Welcome to EventEase!</h1>
            <p className="py-4 text-white text-lg">
              Discover amazing events, meet new people, and experience unforgettable moments. 
              Start exploring now and find the events that suit your interests.
            </p>
            <Link to="/discover" className="btn bg-amber-300 text-dark-purple mt-6 px-8 py-3 text-lg">Explore Events</Link>
          </div>
        </div>
      </div>

      <div className="p-10 bg-white">
        <h2 className="text-4xl text-amber-300 font-semibold mb-10 text-center">Latest Events</h2>
        {loading ? (
          <div className="text-center">Loading...</div>
        ) : error ? (
          <div className="text-center text-bold text-red-500">Error fetching events: {error.message}</div>
        ) : latestEvents.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {latestEvents.map(event => (
              <EventCard 
                key={event.id} 
                event={event} 
                className="text-xs"
              />
            ))}
          </div>
        ) : (
          <div className="text-center text-lg font-semibold">No events found</div>
        )}
      </div>

      <div className="bg-white text-primary-content p-10 text-center">
        <h2 className="text-3xl font-semibold mb-4">Want to organize your own event?</h2>
        <p className="mb-6">Become an organizer and start creating events that bring people together.</p>
        <button className="btn text-dark-purple bg-amber-300 px-8 py-3 text-lg" onClick={handleCreateEventClick}>
          Create Event
        </button>
      </div>
      </div>
    </PageLayout>
  );
}
