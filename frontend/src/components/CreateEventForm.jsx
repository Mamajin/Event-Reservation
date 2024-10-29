import React, { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";

function CreateEventForm() {

    const [formData, setFormData] = useState({
        event_name: "",
        start_date_register: "",
        end_date_register: "",
        start_date_event: "",
        end_date_event: "",
        description: "",
        max_attendee: "",
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    
    const formatDateTime = (dateTime) => {
        const date = new Date(dateTime);
        return date.toISOString(); // Formats to "YYYY-MM-DDTHH:MM:SS.sssZ"
    };
    const handleChange = (e) => {
        const { name, value } = e.target; // Destructure name and value from input
        setFormData({ ...formData, [name]: value }); // Update corresponding field in state
    };
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent default form submission behavior
        setLoading(true); // Show loading state
        try {
            const payload = {
                ...formData,
                start_date_register: formatDateTime(formData.start_date_register),
                end_date_register: formatDateTime(formData.end_date_register),
                start_date_event: formatDateTime(formData.start_date_event),
                end_date_event: formatDateTime(formData.end_date_event),
                max_attendee: parseInt(formData.max_attendee, 10), // Convert max attendees to integer
            };
    
            console.log("Payload being sent to API:", payload); // Log payload for debugging
            console.log("Payload being sent to API:", JSON.stringify(payload, null, 2));
            const token = localStorage.getItem(ACCESS_TOKEN);
            const response = await api.post('/events/create-event', payload, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            alert("Event created successfully!");
            navigate("/");
        } catch (error) {
            console.error("Error creating event:", error);
            let errorMessage = "Failed to create event. Please try again.";

            if (error.response) {
                errorMessage = error.response.data?.error || errorMessage;
            }

            alert(errorMessage);
        } finally {
            setLoading(false);
        }
    };
    return (
        <div className="flex justify-center items-center min-h-screen bg-white-100">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4"
            >
                <h1 className="text-2xl font-bold mb-4 text-center text-dark-purple">Create Event</h1>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Event Name</span>
                    </label>
                    <input
                        type="text"
                        name="event_name"
                        value={formData.event_name}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        placeholder="Enter event name"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Start Date for Registration</span>
                    </label>
                    <input
                        type="datetime-local"
                        name="start_date_register"
                        value={formData.start_date_register}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">End Date for Registration</span>
                    </label>
                    <input
                        type="datetime-local"
                        name="end_date_register"
                        value={formData.end_date_register}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Start Date of Event</span>
                    </label>
                    <input
                        type="datetime-local"
                        name="start_date_event"
                        value={formData.start_date_event}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">End Date of Event</span>
                    </label>
                    <input
                        type="datetime-local"
                        name="end_date_event"
                        value={formData.end_date_event}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Maximum Attendees</span>
                    </label>
                    <input
                        type="number"
                        name="max_attendee"
                        value={formData.max_attendee}
                        onChange={handleChange}
                        className="input bg-white input-bordered w-full"
                        placeholder="Maximum number of attendees"
                        min="1"
                        required
                    />
                </div>
                <div className="form-control w-full">
                    <label className="label">
                        <span className="label-text text-dark-purple">Description</span>
                    </label>
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        className="textarea bg-white textarea-bordered w-full"
                        placeholder="Enter event description"
                        required
                    ></textarea>
                </div>
                <button
                    type="submit"
                    className={`btn bg-amber-300 text-dark-purple w-full mt-4 ${loading ? "loading" : ""}`}
                    disabled={loading}
                >
                    {loading ? "Creating..." : "Create Event"}
                </button>
            </form>
        </div>
    );
}

export default CreateEventForm;