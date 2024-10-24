import React, { useEffect, useState } from 'react';
import api from '../api';
import EventCard from '../components/EventCard';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import PageLayout from '../components/PageLayout';

function Home() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await api.get('/events/events');
        setEvents(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }

  return (
    <PageLayout>
        <div className="card lg:card-side bg-base-100 shadow-xl">
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
          </div>
    </PageLayout>
  );
}

export default Home;
