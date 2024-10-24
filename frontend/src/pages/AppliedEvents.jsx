import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import EventCard from '../components/EventCard';
import { ACCESS_TOKEN } from "../constants";
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

                const url = `http://localhost:8000/api/tickets/event/${userId}`;
                const response = await axios.get(url, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // Map the ticket response to fetch detailed event info
                const eventsData = await Promise.all(
                    response.data.map(async (ticket) => {
                        const eventResponse = await axios.get(`http://localhost:8000/api/events/${ticket.event}`, {
                            headers: {
                                Authorization: `Bearer ${token}`,
                            },
                        });
                        return { ...ticket, event: eventResponse.data };
                    })
                );

                setEvents(eventsData);
                console.log('Fetched events:', eventsData);
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
        return (
            <PageLayout>
                <div className="flex justify-center items-start min-h-screen p-4">
                    <div className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                        <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Error</h2>
                        <div className="text-center">
                            <div>Error fetching applied events: {error?.message || userError.message}</div>
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
                    <div className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
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
                <div className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                    <h1 className="text-2xl font-bold mb-6 text-center text-dark-purple">Applied Events</h1>
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
