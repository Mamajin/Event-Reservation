import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import { PROFILE_PICTURE } from '../constants';

function TicketDetail() {
  const { ticketId } = useParams();
  const [ticket, setTicket] = useState(null);
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTicketAndEvent = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) throw new Error('Unauthorized: No access token found.');

        // Fetch ticket details
        const ticketResponse = await api.get(`/tickets/${ticketId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTicket(ticketResponse.data);

        // Use event_id from the ticket to fetch event details
        const eventId = ticketResponse.data.event_id;
        const eventResponse = await api.get(`/events/${eventId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setEvent(eventResponse.data);
      } catch (err) {
        console.error('Error fetching ticket or event details:', err);
        setError(err.message || 'Failed to fetch data.');
      } finally {
        setLoading(false);
      }
    };

    fetchTicketAndEvent();
  }, [ticketId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-xl rounded-lg mt-8">
      <div className="event-image mb-4">
        <img
          src={event?.event_image || 'https://via.placeholder.com/400x200'}
          alt={event?.event_name || 'Event'}
          className="w-full h-48 object-cover rounded-lg"
        />
      </div>

      <h1 className="text-2xl font-bold">{event?.event_name || 'Event Name'}</h1>
      <div className="ticket-info">
        <p>Ticket Number: {ticket?.ticket_number}</p>
        <p>Registrant Name: {ticket?.fullname}</p>
        <p>Register Date: {new Date(ticket?.register_date).toLocaleDateString()}</p>
        <p>Status: {ticket?.status || 'Active'}</p>
      </div>

      <div className="profile">
        <img
          src={PROFILE_PICTURE || 'https://via.placeholder.com/100'}
          alt="Profile"
          className="rounded-full"
          width={100}
        />
      </div>
    </div>
  );
}

export default TicketDetail;
