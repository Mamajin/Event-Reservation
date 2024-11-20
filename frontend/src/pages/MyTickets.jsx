import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
        const userId = localStorage.getItem("id"); // Get the user ID from local storage
        const token = localStorage.getItem("access_token");

        if (!userId || !token) {
          throw new Error("User not logged in or missing credentials.");
        }

        // Fetch tickets for the logged-in user
        const ticketResponse = await api.get(`/tickets/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const ticketsData = ticketResponse.data;
        setTickets(ticketsData);

        // Extract unique event IDs
        const uniqueEventIds = [...new Set(ticketsData.map((ticket) => ticket.event_id))];

        // Fetch all events in one batch
        const eventResponses = await Promise.all(
          uniqueEventIds.map((eventId) =>
            api.get(`/events/${eventId}`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })
          )
        );

        // Create a map of event_id to event_name
        const eventMap = {};
        eventResponses.forEach((response) => {
          const event = response.data;
          eventMap[event.id] = event.event_name;
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
        <div className="text-center mt-8 text-gray-500">You have no tickets yet.</div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-8">
        <h1 className="text-2xl text-dark-purple mb-5 font-bold text-center">My Tickets</h1>
        <div className="grid gap-6">
          {tickets.map((ticket) => (
            <div
              key={ticket.ticket_id}
              className="border-2 border-dashed border-gray-400 rounded-lg p-4 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleViewTicket(ticket.id)}
            >
              <p className="text-lg">
                <span className="font-semibold text-dark-purple">Event:</span> {events[ticket.event_id] || 'Fetching...'}
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
          ))}
        </div>
      </div>
    </PageLayout>
  );
}

export default MyTickets;
