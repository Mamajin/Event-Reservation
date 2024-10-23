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
    <PageLayout>
      <h2 className="text-2xl font-bold mb-4">Account Information</h2>
      <div className="info">
        <p><strong>Place Holder</strong></p>
      </div>
    </PageLayout>
  );
}

export default AppliedEvents;
