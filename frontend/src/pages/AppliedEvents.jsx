import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import EventCard from '../components/EventCard';
import { ACCESS_TOKEN } from "../constants";

function AppliedEvents() {
  const [events, setEvents] = useState([]); // Initially an empty array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate here

  useEffect(() => {
    const fetchAppliedEvents = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const userId = 1; // Replace with the actual user ID as needed or fetch dynamically

        if (!token) {
          throw new Error('No access token found'); // Handle missing token
        }

        const response = await axios.get(`http://localhost:8000/api/tickets/event/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log('API response:', response.data); // Log the API response

        setEvents(response.data); // Set the fetched events data

      } catch (err) {
        if (err.message === 'No access token found') {
          alert('You are not logged in. Redirecting to login page...');
          navigate('/login'); // Redirect to login if token is missing
        } else {
          setError(err); // Handle other errors
        }
      } finally {
        setLoading(false);
      }
    };

    fetchAppliedEvents();
  }, [navigate]); // Add 'navigate' as a dependency

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching applied events: {error.message}</div>;
  }

  if (events.length === 0) {
    return (
      <PageLayout>
      <h2 className="text-2xl font-bold mb-4">Applied Events</h2>
      <div className="grid grid-cols-1 gap-4">
        <div>No applied events available</div>
      </div>
    </PageLayout>
  );
  }

  return (
    <PageLayout>
      <h2 className="text-2xl font-bold mb-4">Applied Events</h2>
      <div className="grid grid-cols-1 gap-4">
        {events.map((ticket, index) => (
          <EventCard key={index} event={ticket.event} />
        ))}
      </div>
    </PageLayout>
  );
}

export default AppliedEvents;
