import { EventHeader } from './sections/EventHeader';
import { EventInfo } from './sections/EventInfo';
import { OrganizerInfo } from './sections/OrganizerInfo';
import { CommentSection } from './sections/Comment';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../api';

function EventDetail() {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await api.get(`/events/${eventId}`);
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
    <div className="min-h-screen bg-gray-50 w-full relative ">
      <EventHeader event={event} />
      {event.organizer && <OrganizerInfo organizer={event.organizer} />}
      <EventInfo event={event} />
      <CommentSection event={event}/>
    </div>
  );
}

export default EventDetail;
