import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { FaArrowLeft } from 'react-icons/fa';
import PageLayout from '../components/PageLayout';
import QRCode from 'react-qr-code';
import { PROFILE_PICTURE } from '../constants';

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

  // Construct data for the QR code
  const qrCodeData = {
    ticket_id: ticket.ticket_id,
    event_name: event.event_name,
    fullname: ticket.fullname,
    profile_picture: PROFILE_PICTURE, // Profile picture URL from constants
    register_date: new Date(ticket.register_date).toLocaleDateString(),
    status: ticket.status,
  };

  return (
    <PageLayout>
      <div className="max-w-lg mx-auto p-6 bg-white shadow-xl rounded-lg mt-8 relative overflow-hidden">
        {/* Watermark */}
        <div className="absolute inset-0 transform rotate-45 flex justify-center items-center text-7xl text-gray-300 font-bold opacity-20 pointer-events-none" style={{ zIndex: 1 }}>
          EventEase
        </div>

        {/* Virtual Ticket Header */}
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-dark-purple">Virtual Ticket</h1>
        </div>

        {/* Back Button */}
        <button className="absolute top-4 left-4 p-2" onClick={handleBackClick}>
          <FaArrowLeft className="text-gray-500" />
        </button>

        {/* Ticket Background */}
        <div className="ticket-container p-6 bg-gradient-to-b from-blue-500 to-indigo-700 text-white rounded-2xl relative">
          {/* Event Image */}
          <div className="event-image mb-4">
            <img
              src={event?.event_image || 'https://via.placeholder.com/400x200'}
              alt={event?.event_name || 'Event'}
              className="w-full h-48 object-cover rounded-lg"
            />
          </div>

          {/* Ticket Information */}
          <div className="text-left">
            <h1 className="text-2xl font-bold mb-2">{event?.event_name || 'Event Name'}</h1>
            <div className="ticket-info">
              <p className="text-lg">
                <span className="font-semibold">Ticket Number:</span> {ticket?.ticket_number}
              </p>
              <p className="text-lg mt-2">
                <span className="font-semibold">Registrant Name:</span> {ticket?.fullname}
              </p>
              <p className="text-lg mt-2">
                <span className="font-semibold">Register Date:</span> {new Date(ticket?.register_date).toLocaleDateString()}
              </p>
              <p className="text-lg mt-2">
                <span className="font-semibold">Status:</span> {ticket?.status || 'Active'}
              </p>
            </div>

            {/* QR Code Section with Larger White Space */}
            <div className="mt-6 flex justify-center items-center p-6 bg-white rounded-lg shadow-lg">
              <QRCode value={JSON.stringify(qrCodeData)} size={200} />
            </div>

            {/* Ticket Footer */}
            <div className="mt-6 border-t-2 border-white pt-4">
              <button
                className="bg-amber-300 text-dark-purple py-2 px-6 rounded-lg font-semibold hover:bg-amber-400 transition-all duration-300"
                onClick={() => alert('This ticket is valid for the event.')}
              >
                Validate Ticket
              </button>
            </div>
          </div>
        </div>

        {/* Ticket Borders for realism */}
        <div className="absolute top-0 left-0 right-0 bottom-0 border-4 border-grey rounded-2xl p-2 pointer-events-none">
          <div className="w-full h-full border-4 border-grey opacity-40 rounded-xl"></div>
        </div>
      </div>
    </PageLayout>
  );
}

export default VirtualTicket;
