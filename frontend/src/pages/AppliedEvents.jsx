import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import EventCard from '../components/EventCard';
import { ACCESS_TOKEN } from "../constants";
import useUserProfile from '../hooks/useUserProfile'; // Import the custom hook

function AppliedEvents() {
  const [events, setEvents] = useState([]); // Initially an empty array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate here
  const { userId, loading: userLoading, error: userError } = useUserProfile(navigate); // Use the custom hook

  useEffect(() => {
    const fetchAppliedEvents = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token || !userId) {
          throw new Error('No access token or user ID found'); // Handle missing token or user ID
        }

        const response = await axios.get(`http://localhost:8000/api/tickets/event/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log('API response:', response.data); // Log the API response
        setEvents(response.data); // Set the fetched events data

      } catch (err) {
        if (err.message === 'No access token or user ID found') {
          alert('You are not logged in. Redirecting to login page...');
          navigate('/login'); // Redirect to login if token is missing
        } else {
          setError(err); // Handle other errors
        }
      } finally {
        setLoading(false);
      }
    };

    if (!userLoading && userId) {
      fetchAppliedEvents(); // Fetch applied events only if user ID is available
    }
  }, [navigate, userId, userLoading]); // Add 'userId' and 'userLoading' as dependencies

  if (loading || userLoading) {
    return (
      <PageLayout>
        <div className="flex justify-end items-start min-h-screen bg-white-100 p-4">
            <div className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Applied Events</h2>
                <div className="grid grid-cols-1 gap-4">
                    <div className="text-center">Loading...</div>
                </div>
            </div>
        </div>
      </PageLayout>
  );
  }

  if (error || userError) {
    return <div>Error fetching applied events: {error?.message || userError.message}</div>;
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
        <div className="flex justify-end items-start min-h-screen bg-white-100 p-4">
            <div className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Applied Events</h2>
                <div className="grid grid-cols-1 gap-4">
                    {events.map((ticket, index) => (
                        <EventCard key={index} event={ticket.event} />
                    ))}
                </div>
            </div>
        </div>
    </PageLayout>
  );
}

export default AppliedEvents;
