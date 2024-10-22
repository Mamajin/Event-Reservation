import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from '../constants';

function OrganizerForm() {
    const [formData, setFormData] = useState({
        organizer_name: '',
        email: '',
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const token = localStorage.getItem(ACCESS_TOKEN);
            const response = await api.post('/organizers/apply-organizer', formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            alert('Application to become an organizer submitted successfully!');
            navigate('/');
        } catch (error) {
            console.error('Error applying to become an organizer:', error);
            alert('Failed to submit the application. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Organizer Form</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="organizer_name"
                    value={formData.organizer_name}
                    onChange={handleChange}
                    placeholder="Enter organizer name"
                    required
                />
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter email"
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Submitting...' : 'Submit Application'}
                </button>
            </form>
        </div>
    );
}

export default OrganizerForm;