import { useState, useEffect } from 'react';
import api from '../api';
import { ACCESS_TOKEN } from '../constants';
import { useNavigate } from 'react-router-dom';

function useUserProfile() {
    const [userId, setUserId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const token = localStorage.getItem(ACCESS_TOKEN);
                if (!token) {
                    throw new Error("No access token found");
                }

                const response = await api.get('/users/profile', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // Validate response content-type to ensure it's JSON
                if (!response.headers['content-type'].includes('application/json')) {
                    throw new Error("Expected JSON but received HTML response");
                }

                // Validate the response data structure
                if (!response.data || !response.data.username || !response.data.id) {
                    throw new Error("Invalid user data received");
                }

                setUserId(response.data.id);
            } catch (err) {
                console.error("Error fetching user profile:", err.message);

                if (err.message.includes("No access token found") || err.response?.status === 401) {
                    alert("You are not logged in. Redirecting to login page...");
                    navigate("/login");
                } else {
                    setError(err);
                }
            } finally {
                setLoading(false);
            }
        };

        if (loading) {
            fetchUserProfile();
        }
    }, [loading, navigate]);


    return { userId, loading, error };
}

export default useUserProfile;
