import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
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
        if (!token) {
          throw new Error('No access token found'); // Handle missing token
        }

        const response = await axios.get('http://localhost:8000/api/users/applied-events', {
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
    return <div>No applied events available</div>;
  }

  return (
    <PageLayout>
      <h2 className="text-2xl font-bold mb-4">Applied Events</h2>
      <div className="events-list">
        {events.map((event, index) => (
          <div key={index} className="event-item">
            <h3>{event.name}</h3>
            <p><strong>Date:</strong> {event.date}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p><strong>Status:</strong> {event.status}</p>
          </div>
        ))}
      </div>
    </PageLayout>
  );
}

export default AppliedEvents;
