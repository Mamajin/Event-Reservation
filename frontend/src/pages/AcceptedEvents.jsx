import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';

function AcceptedEvents() {
  const [acceptedEvents, setAcceptedEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAcceptedEvents = async () => {
      try {
        // Call the API to fetch accepted events
        const response = await axios.get('http://localhost:8000/mock_api/event/');
        // Please consult me before merging we might need more stub data
        // Filter events to include only those that are accepted (assuming we created a way to mark them as accepted)
        const accepted = response.data.filter((event) => event.is_accepted);
        setAcceptedEvents(accepted);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAcceptedEvents();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching accepted events: {error.message}</div>;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1">
          <div className="bg-white min-h-screen p-6">
            <h2 className="text-2xl font-bold mb-4">Accepted Events</h2>
            {acceptedEvents.length === 0 ? (
              <p>No accepted events.</p>
            ) : (
              <ul>
                {acceptedEvents.map((event) => (
                  <li key={event.event_name}>
                    <strong>{event.event_name}</strong> - {new Date(event.start_date_event).toLocaleDateString()}
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

export default AcceptedEvents;
