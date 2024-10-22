import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';

function AccountInfo( {user} ) {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/profile');
        const organizer = response.data[0]?.organizer;
        if (organizer?.user) {
          setUserData(organizer.user);
        } else {
          setUserData({
            username: 'Unknown',
            email: 'Unknown',
          });
        }
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching user data: {error.message}</div>;
  }

  if (!userData) {
    return <div>No user data available</div>;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1">
          <div className="bg-white min-h-screen p-6">
            <h2 className="text-2xl font-bold mb-4">Account Information</h2>
            <div className="info">
              <p><strong>Username:</strong> {user.username || 'Unknown'}</p>
              <p><strong>Email:</strong> {user.email || 'Unknown'}</p>
              <p><strong>First Name:</strong> {user.firstname || 'Unknown'}</p>
              <p><strong>Last Name:</strong> {user.lastname || 'Unknown'}</p>
              <p><strong>Phone Number:</strong> {user.phonenumber || 'Unknown'}</p>
              <p><strong>Status:</strong> {user.status || 'Unknown'}</p>
            </div>
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
}

export default AccountInfo;
