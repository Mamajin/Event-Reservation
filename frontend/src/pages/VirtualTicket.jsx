import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { FaArrowLeft } from 'react-icons/fa';
import PageLayout from '../components/PageLayout';

function VirtualTicket() {
  const { ticketId } = useParams();
  const navigate = useNavigate();
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
        const eventId = ticketResponse.data.event_id; // Ensure the event_id exists in the ticket response
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

  const handleBackClick = () => {
    navigate(-1); // Navigate back to the previous page
  };

  if (loading) {
    return (
      <PageLayout>
        <div className="text-center mt-8">Loading ticket details...</div>
      </PageLayout>
    );
  }

  if (error) {
    return (
      <PageLayout>
        <div className="text-center mt-8 text-red-500">{error}</div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-8 relative">
        <button className="absolute top-4 left-4 p-2" onClick={handleBackClick}>
          <FaArrowLeft className="text-gray-500" />
        </button>
        <div className="text-center">
          <h1 className="text-4xl text-dark-purple mb-5 font-bold">Virtual Ticket</h1>
        </div>
        
        {/* Ticket Container */}
        <div className="relative w-full max-w-3xl bg-gradient-to-r from-yellow-200 via-amber-200 to-yellow-400 border-4 border-dashed border-dark-purple rounded-lg p-6 shadow-xl overflow-hidden">

          {/* Watermark */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-gray-500 opacity-30 text-6xl rotate-45 font-bold">
            EventEase
          </div>

          {/* Cut-out Effect on Left & Right */}
          <div className="absolute left-0 top-0 w-8 h-full bg-white transform -translate-x-3 rounded-tr-lg rounded-br-lg z-10"></div>
          <div className="absolute right-0 top-0 w-8 h-full bg-white transform translate-x-3 rounded-tl-lg rounded-bl-lg z-10"></div>

          {/* Event Image */}
          <div className="w-full mb-4">
            <img
              src={event?.event_image || '/path/to/default-image.jpg'}
              alt="Event"
              className="w-full h-56 object-cover rounded-md"
            />
          </div>

          {/* Ticket Details */}
          <div className="text-center text-dark-purple">
            <p className="text-lg font-semibold">
              <span className="text-lg font-bold text-dark-purple">Ticket Number:</span> {ticket.ticket_number}
            </p>
            <p className="text-lg mt-2">
              <span className="text-lg font-bold text-dark-purple">Event Name:</span> {event?.event_name || 'N/A'}
            </p>
            <p className="text-lg mt-2">
              <span className="font-bold text-dark-purple">Registrant Name:</span> {ticket.fullname}
            </p>
            <p className="text-lg mt-2">
              <span className="font-bold text-dark-purple">Register Date:</span>{' '}
              {new Date(ticket.register_date).toLocaleDateString()}
            </p>
            <p className="text-lg mt-2">
              <span className="font-bold text-dark-purple">Status:</span> {ticket.status || 'Active'}
            </p>
            <p className="text-lg mt-2">
              <span className="font-bold text-dark-purple">Registered At:</span>{' '}
              {new Date(ticket.created_at).toLocaleDateString()}
            </p>
          </div>

          <div className="mt-6 text-center">
            <button
              className="btn bg-amber-300 text-dark-purple py-2 px-6 rounded-lg"
              onClick={() => alert('This ticket is valid for the event.')}
            >
              Validate Ticket
            </button>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default VirtualTicket;
