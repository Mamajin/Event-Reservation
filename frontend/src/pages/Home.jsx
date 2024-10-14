import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EventCard from '../components/EventCard'; // Import the new component

function Home() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axios.get('http://localhost:8000/stub_api/mock_api/event_actual/');
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
    <div className="bg-white min-h-screen p-6">
      <div className="card lg:card-side bg-base-100 shadow-xl">
        {events.map((event) => (
          <EventCard key={event.organizer.user.id} event={event} /> // Use the EventCard component
        ))}
      </div>
    </div>
  );
}

export default Home;
