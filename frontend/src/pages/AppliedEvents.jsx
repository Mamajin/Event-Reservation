import React, { useEffect, useState } from 'react';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import EventCard from '../components/EventCard';
import { ACCESS_TOKEN } from "../constants";
import api from '../api';
import useUserProfile from '../hooks/useUserProfile';

function AppliedEvents() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { userId, loading: userLoading, error: userError } = useUserProfile(navigate);

    useEffect(() => {
        const fetchAppliedEvents = async () => {
            try {
                console.log('Fetching applied events...');
                const token = localStorage.getItem(ACCESS_TOKEN);
                if (!token || !userId) {
                    throw new Error('No access token or user ID found');
                }

                // Fetch all events from the API
                const eventsResponse = await api.get(`/events/events`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // Fetch tickets for the user
                const ticketsResponse = await api.get(`/tickets/user/${userId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // Extract event IDs from tickets
                const eventIds = ticketsResponse.data.map(ticket => ticket.event_id);

                // Filter events based on applied event IDs
                const appliedEvents = eventsResponse.data.filter(event => eventIds.includes(event.id));

                setEvents(appliedEvents);
                console.log('Fetched applied events:', appliedEvents);
            } catch (err) {
                console.error('Error fetching applied events:', err);
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        if (!userLoading && userId) {
            fetchAppliedEvents();
        } else if (userLoading) {
            console.log('Waiting for user profile to load...');
        }
    }, [navigate, userId, userLoading]);

    if (loading || userLoading) {
        return (
            <PageLayout>
                <div className="flex justify-center items-start min-h-screen p-4">
                    <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
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
        return (
            <PageLayout>
                <div className="flex justify-center items-start min-h-screen p-4">
                    <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                        <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Error</h2>
                        <div className="text-center">
                            <div>Error fetching applied events: {error?.message || userError?.message}</div>
                        </div>
                    </div>
                </div>
            </PageLayout>
        );
    }

    if (events.length === 0) {
        return (
            <PageLayout>
                <div className="flex justify-center items-start min-h-screen p-4">
                    <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                        <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Applied Events</h2>
                        <div className="grid grid-cols-1 gap-4">
                            <div>No applied events available</div>
                        </div>
                    </div>
                </div>
            </PageLayout>
        );
    }

    return (
        <PageLayout>
            <div className="flex justify-center items-start min-h-screen p-4">
                <div className="w-full max-w-[1400px] bg-white rounded-lg shadow-lg p-6 space-y-4">
                    <h1 className="text-2xl font-bold mb-6 text-center text-dark-purple">Applied Events</h1>
                    <div className="grid grid-cols-1 gap-4"> {/* Stacks EventCard components vertically with spacing */}
                        {events.map((event) => (
                            <EventCard 
                            key={event.id}
                            event={event}/>
                        ))}
                    </div>
                </div>
            </div>
        </PageLayout>
    );
}

export default AppliedEvents;
