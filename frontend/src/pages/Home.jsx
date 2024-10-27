
import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';
import { Link } from 'react-router-dom';

function Home() {
  const [latestEvents, setLatestEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  return (
    <PageLayout>
      <div className="hero h-screen bg-cover bg-center" style={{ backgroundImage: `url('https://i.pinimg.com/564x/92/57/6b/92576be9601f00886b03e58363369647.jpg')` }}>
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
    </PageLayout>
  );
}

export default Home;