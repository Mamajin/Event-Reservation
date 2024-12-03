import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import { useNavigate,Link } from 'react-router-dom';
import {USER_STATUS} from '../constants'
import EventScroller from '../components/Home/EventScroller';
import HeroCarousel from '../components/Home/Hero';
import Loading from '../components/LoadingIndicator';
export default function Home() {
  const [popularEvents, setPopularEvents] = useState([]);
  const [latestEvents, setLatestEvents] = useState([]);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const isOrganizer = localStorage.getItem(USER_STATUS) === "Organizer";
  const navigate = useNavigate(); 


  useEffect(() => {
    const fetchEvents = async () => {
      
      try {
        const response = await api.get('/events/events');
        const sortedEvents = response.data.slice().sort((a, b) => new Date(b.start_date_event) - new Date(a.start_date_event));
        setLatestEvents(sortedEvents.slice(0, 8));

        const sortedByLikes = response.data.sort((a, b) => 
          b.current_attendees - a.current_attendees
        );
        setPopularEvents(sortedByLikes.slice(0, 8));

        const sortedUpcoming = response.data.filter(event => new Date(event.start_date_event) > new Date());
        setUpcomingEvents(sortedUpcoming.sort((a, b) => new Date(a.start_date_event) - new Date(b.start_date_event)).slice(0, 8)); 
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
  if (loading) {
    return (
      <Loading />
    );
  }
  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }
  return (
    <PageLayout>
      <HeroCarousel  slides={popularEvents}/>
      <div className='bg-white pt-6'>
      <div className=''>
      <EventScroller
        title="Popular Events"
        description="Join the most attended events in your area"
        events={popularEvents}
      />
      </div>
      <div className='bg-white'>
      <EventScroller
        title="Upcoming Events"
        description="Don't miss out on the events coming soon!"
        events={upcomingEvents}
      />
      </div>
      <div className='bg-white'>
      <EventScroller
        title="Latest Events"
        description="Discover newly added events"
        events={latestEvents}
      />
      </div>

    <div className="bg-gradient-to-r from-amber-400 to-amber-500 py-16">    
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Ready to Create Your Own Event?
        </h2>
        <p className="text-xl text-gray-800 mb-8 max-w-2xl mx-auto">
          {isOrganizer
            ? "Share your passion with the world. Start planning your next event today!"
            : "Become an organizer and start creating events that bring people together."}
        </p>
        <button
          onClick={handleCreateEventClick}
          className="bg-gray-900 text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-gray-800 transition-colors"
        >
          {isOrganizer ? "Create Event" : "Become an Organizer"}
        </button>
      </div>
    </div>
      </div>
    </PageLayout>
  );
}
