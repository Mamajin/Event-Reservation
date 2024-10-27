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
            console.error("Error applying to become an organizer", error);
            let errorMessage = "Failed to submit the application. Please try again.";

            if (error.response) {
                errorMessage = error.response.data?.error || errorMessage;
            }

            alert(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex justify-center items-start min-h-screen bg-white-100 p-0">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4"
                aria-label="Apply to Become Organizer Form"
            >
                <h1 className="text-2xl font-bold mb-4 text-center text-dark-purple">Apply to Become an Organizer</h1>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Organizer Name</span>
                    </label>
                    <input
                        type="text"
                        name="organizer_name"
                        value={formData.organizer_name}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        placeholder="Enter organizer name"
                        aria-label="Organizer Name"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Email</span>
                    </label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        placeholder="Enter email"
                        aria-label="Email"
                        required
                    />
                </div>
                <button
                    type="submit"
                    className={`btn bg-amber-300 text-dark-purple w-full mt-4 ${loading ? 'loading' : ''}`}
                    disabled={loading}
                >
                    {loading ? 'Submitting...' : 'Submit Application'}
                </button>
            </form>
        </div>
    );
}

export default OrganizerForm;