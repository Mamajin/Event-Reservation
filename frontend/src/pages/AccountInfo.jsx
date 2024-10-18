import { useState, useEffect } from 'react';
import axios from 'axios';

function AccountInfo() {
    const [userData, setUserData] = useState(null); // Store the fetched user data
    const [loading, setLoading] = useState(true);   // Show loading state
    const [error, setError] = useState(null); // Handle errors

    useEffect(() => {
        // Fetch user data from the API
        axios.get('http://localhost:8000/mock_api/event/')
            .then((response) => {
                const organizer = response.data[0]?.organizer;
                if (organizer?.user) {
                    // If user data is present, set it
                    setUserData(organizer.user);
                } else {
                    // Handle missing user data gracefully
                    setUserData({
                        username: 'Unknown',
                        email: 'Unknown',
                    });
                }
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching user data:', error);
                setError(error);
                setLoading(false);
            });
    }, []);

    // If still loading data, show loading state
    if (loading) {
        return <div>Loading...</div>;
    }

    // If error occurred, show error message
    if (error) {
        return <div>Error fetching user data: {error.message}</div>;
    }

    // If no data found, handle it
    if (!userData) {
        return <div>No user data available</div>;
    }

    return (
        <div className="account-info">
            <h2>Account Information</h2>
            <div className="info">
                <p><strong>Username:</strong> {userData.username || 'Unknown'}</p>
                <p><strong>Email:</strong> {userData.email || 'Unknown'}</p>
            </div>
        </div>
    );
}

export default AccountInfo;
