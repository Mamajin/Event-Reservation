import { EventHeader } from '../components/EventDetail/sections/EventHeader';
import { EventInfo } from '../components/EventDetail/sections/EventInfo';
import { OrganizerInfo } from '../components/EventDetail/sections/OrganizerInfo';
import PageLayout from "../components/PageLayout";
import { ACCESS_TOKEN } from '../constants';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function EventDetail() {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const response = await api.get(`/events/${eventId}`, { headers });
        console.log(response.data);
        setEvent(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [eventId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading event details.</div>;
  if (!event) return <div>No event found.</div>;

  return (
    <PageLayout>
    <div className="min-h-screen bg-gray-50 w-full relative ">
      <EventHeader event={event} />
      {event.organizer && <OrganizerInfo organizer={event.organizer} />}
      <EventInfo event={event} />
    </div>
    </PageLayout>
  );
}