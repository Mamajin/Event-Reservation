import { useState, useEffect } from 'react';
import axios from 'axios';
import { ACCESS_TOKEN } from '../constants';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function useUserProfile(navigate) {
    const [userId, setUserId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                // console.log("Fetching user profile...");
                const token = localStorage.getItem(ACCESS_TOKEN);

                if (!token) {
                    navigate('/login');
                    return;
                }

                const response = await api.get('/users/profile', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // console.log("API response data:", response.data);

                // Validate the response data structure
                if (!response.data || !response.data.username || !response.data.id) {
                    throw new Error("Invalid user data received");
                }

                setUserId(response.data.id);
                // console.log("User profile response:", response.data);
            } catch (err) {
                console.error("Error fetching user profile:", err);
                setError(err);
            } finally {
                setLoading(false);
                console.log("Finished fetching user profile.");
            }
        };

        if (!userId && loading) {
            fetchUserProfile();
        }
    }, [userId, navigate]);

    return { userId, loading, error };
}

export default useUserProfile;
