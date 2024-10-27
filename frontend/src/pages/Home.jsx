
import React, { useEffect, useState } from 'react';
import api from '../api';
import PageLayout from '../components/PageLayout';

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
      <div>Home Page</div>
    </PageLayout>
  );
}

export default Home;