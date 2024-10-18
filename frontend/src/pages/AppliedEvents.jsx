import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';

function AppliedEvents() {
  const [appliedEvents, setAppliedEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAppliedEvents = async () => {
      try {
        // Call the Ninja API to fetch events
        const response = await axios.get('http://localhost:8000/mock_api/event/');
        setAppliedEvents(response.data); // Assuming data is an array of events
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAppliedEvents();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching applied events: {error.message}</div>;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1">
          <div className="bg-white min-h-screen p-6">
            <h2 className="text-2xl font-bold mb-4">Applied Events</h2>
            {appliedEvents.length === 0 ? (
              <p>No events applied for.</p>
            ) : (
              <ul>
                {appliedEvents.map((event) => (
                  <li key={event.event_name}>
                    <strong>{event.event_name}</strong> - {event.start_date_event}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
}

export default AppliedEvents;
