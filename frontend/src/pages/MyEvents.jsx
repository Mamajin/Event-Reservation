import React, { useEffect, useState } from 'react';
import PageLayout from '../components/PageLayout';
import { useNavigate } from 'react-router-dom';
import EventCard from '../components/EventCard';
import { ACCESS_TOKEN } from "../constants";
import useUserProfile from '../hooks/useUserProfile';
import api from '../api';

function MyEvents() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { userId, loading: userLoading, error: userError } = useUserProfile(navigate);
    
    const handleEdit = (eventId) => {
        navigate(`/events/${eventId}/edit`);
    };

    useEffect(() => {
        const fetchOrganizerEvents = async () => {
            try {
                console.log('Fetching organizer events...');
                const token = localStorage.getItem(ACCESS_TOKEN);
                if (!token || !userId) {
                    throw new Error('No access token or user ID found');
                }

                // Fetch organizer events from the API
                const response = await api.get(`/events/my-events`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                });

                setEvents(response.data);
                console.log('Fetched organizer events:', response.data);
            } catch (err) {
                console.error('Error fetching organizer events:', err);
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        if (!userLoading && userId) {
            fetchOrganizerEvents();
        } else if (userLoading) {
            console.log('Waiting for user profile to load...');
        }
    }, [navigate, userId, userLoading]);

    if (loading || userLoading) {
        return (
            <PageLayout>
                <div className="flex justify-center items-start min-h-screen p-4">
                    <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
                        <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">My Events</h2>
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
                            <div>Error fetching organizer events: {error?.message || userError?.message}</div>
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
                        <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">My Events</h2>
                        <div className="grid grid-cols-1 gap-4">
                            <div>No events available</div>
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
                    <h1 className="text-2xl font-bold mb-6 text-center text-dark-purple">My Events</h1>
                    <div className="grid grid-cols-1 gap-4">
                        {events.map((event) => (
                            <EventCard key={event.id} event={event} onEdit={handleEdit} isEditable={true} />
                        ))}
                    </div>
                </div>
            </div>
        </PageLayout>
    );
}

export default MyEvents;
