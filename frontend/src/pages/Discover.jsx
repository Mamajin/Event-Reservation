import React, { useEffect, useState } from 'react';
import api from '../api';
import EventCard from '../components/EventCard';
import PageLayout from '../components/PageLayout';
import { ACCESS_TOKEN } from '../constants';

function Discover() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const response = await api.get('/events/events', { headers });
        console.log(response.data);
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

  const filteredEvents = events.filter(event =>
    event.event_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <PageLayout>
      <div className="p-2">
        <input
          type="text"
          placeholder="Search events..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input input-bordered w-full bg-gray-200 mb-4"
        />
        {filteredEvents.length > 0 ? (
          filteredEvents.map((event) => (
            <EventCard key={event.id} event={event} />
          ))
        ) : (
          <h2 className="flex items-center font-bold justify-center h-64 text-4xl text-dark-purple">
          No events found
        </h2>
         )}
      </div>
    </PageLayout>
  );
}

export default Discover;