import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { FaArrowLeft } from 'react-icons/fa';

function VirtualTicket() {
  const { ticketId } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTicket = async () => {
      try {
        const response = await api.get(`/tickets/${ticketId}`);
        setTicket(response.data);
      } catch (err) {
        console.error('Error fetching ticket details:', err);
        setError('Failed to fetch ticket details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchTicket();
  }, [ticketId]);

  const handleBackClick = () => {
    navigate(-1);
  };

  if (loading) {
    return <div className="text-center mt-8">Loading ticket details...</div>;
  }

  if (error) {
    return <div className="text-center mt-8 text-red-500">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-8 relative">
      <button className="absolute top-4 left-4 p-2" onClick={handleBackClick}>
        <FaArrowLeft className="text-gray-500" />
      </button>
      <div className="text-center">
        <h1 className="text-4xl text-dark-purple mb-5 font-bold">Virtual Ticket</h1>
      </div>
      <div className="flex flex-col items-center">
        <div className="border-2 border-dashed border-gray-400 rounded-lg p-4 w-full max-w-xl">
          <p className="text-lg">
            <span className="font-semibold text-dark-purple">Ticket Number:</span> {ticket.ticket_number}
          </p>
          <p className="text-lg mt-2">
            <span className="font-semibold text-dark-purple">Event Name:</span> {ticket.event_name}
          </p>
          <p className="text-lg mt-2">
            <span className="font-semibold text-dark-purple">Registrant Name:</span> {ticket.fullname}
          </p>
          <p className="text-lg mt-2">
            <span className="font-semibold text-dark-purple">Register Date:</span>{' '}
            {new Date(ticket.register_date).toLocaleDateString()}
          </p>
          <p className="text-lg mt-2">
            <span className="font-semibold text-dark-purple">Status:</span> {ticket.status || 'Active'}
          </p>
          <p className="text-lg mt-2">
            <span className="font-semibold text-dark-purple">Created At:</span>{' '}
            {new Date(ticket.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="mt-6">
          <button
            className="btn bg-amber-300 text-dark-purple"
            onClick={() => alert('This ticket is valid for the event.')}
          >
            Validate Ticket
          </button>
        </div>
      </div>
    </div>
  );
}

export default VirtualTicket;
