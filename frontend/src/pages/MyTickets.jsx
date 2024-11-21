import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaTicketAlt } from 'react-icons/fa';
import api from '../api';
import PageLayout from '../components/PageLayout';

function MyTickets() {
  const [tickets, setTickets] = useState([]);
  const [events, setEvents] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTicketsAndEvents = async () => {
      try {
        const userId = localStorage.getItem("id");
        const token = localStorage.getItem("access_token");

        if (!userId || !token) {
          throw new Error("User not logged in or missing credentials.");
        }

        const ticketResponse = await api.get(`/tickets/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const ticketsData = ticketResponse.data;
        setTickets(ticketsData);

        const uniqueEventIds = [...new Set(ticketsData.map((ticket) => ticket.event_id))];

        const eventResponses = await Promise.all(
          uniqueEventIds.map((eventId) =>
            api.get(`/events/${eventId}`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })
          )
        );

        // Create a map of event_id to event data
        const eventMap = {};
        eventResponses.forEach((response) => {
          const event = response.data;
          eventMap[event.id] = event;
        });

        setEvents(eventMap);
      } catch (err) {
        console.error("Error fetching tickets or events:", err);
        setError(err.message || "Failed to fetch tickets or events.");
      } finally {
        setLoading(false);
      }
    };

    fetchTicketsAndEvents();
  }, []);

  const handleViewTicket = (ticketId) => {
    navigate(`/virtual-ticket/${ticketId}`);
  };

  if (loading) {
    return (
      <PageLayout>
        <div className="text-center mt-8">Loading your tickets...</div>
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

  if (tickets.length === 0) {
    return (
      <PageLayout>
        <div className="flex justify-center items-start min-h-screen p-4">
          <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
            <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">My Tickets</h2>
            <div className="grid grid-cols-1 gap-4">
              <div>You don't have any tickets at the moment.</div>
            </div>
          </div>
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="max-w-4xl max-w-[1400px] mx-auto p-6 bg-white shadow-lg rounded-lg mt-8">
        <h1 className="text-2xl text-dark-purple mb-5 font-bold text-center">My Tickets</h1>
        <div className="grid gap-6">
          {tickets.map((ticket) => {
            const event = events[ticket.event_id] || {};
            return (
              <div
                key={ticket.id}
                className="flex border-2 border-solid border-gray-400 rounded-lg p-4 hover:bg-gray-100 cursor-pointer transition duration-300"
                onClick={() => handleViewTicket(ticket.id)}
              >
                {/* Event Image */}
                <div className="flex-shrink-0 w-30 h-32 mr-4">
                  <img
                    src={event.event_image || 'https://via.placeholder.com/400x200'}
                    alt={event.event_name || 'Event'}
                    className="w-full h-full object-cover rounded-lg"
                  />
                </div>

                {/* Ticket Details */}
                <div className="flex-grow">
                  <p className="text-lg">
                    <span className="font-semibold text-dark-purple">Event:</span> {event.event_name || 'Fetching...'}
                  </p>
                  <p className="text-lg mt-2">
                    <span className="font-semibold text-dark-purple">Ticket Number:</span> {ticket.ticket_number}
                  </p>
                  <p className="text-lg mt-2">
                    <span className="font-semibold text-dark-purple">Registration date:</span> {new Date(ticket.register_date).toLocaleDateString()}
                  </p>
                  <p className="text-lg mt-2">
                    <span className="font-semibold text-dark-purple">Status:</span> {ticket.status || "Active"}
                  </p>
                </div>

                {/* Ticket Icon */}
                <div className="flex-shrink-0 ml-4 flex items-center">
                  <FaTicketAlt className="text-yellow-500 hover:text-dark-purple" size={55} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </PageLayout>
  );
}

export default MyTickets;
