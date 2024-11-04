import React, { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";
import DateTimeInput from "./DateTimeInput";
import FileInput from "./FileInput";
import Map from "./Map";

function CreateEventForm() {

    const [formData, setFormData] = useState({
        event_name: "",
        start_date_register: "",
        end_date_register: "",
        start_date_event: "",
        end_date_event: "",
        description: "",
        max_attendee: "",
        address: '',
        latitude: 0,
        longitude: 0,
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    
    const formatDateTime = (dateTime) => {
        const date = new Date(dateTime);
        return date.toISOString(); // Formats to "YYYY-MM-DDTHH:MM:SS.sssZ"
    };

    const handleFileChange = (e) => {}

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
        <div className="flex justify-center items-center min-h-screen pt-9 bg-white-100 px-4">
            <div className="w-full lg:max-w-4xl mx-auto px-4">
                <form
                    onSubmit={handleSubmit}
                    className="w-full max-w bg-white rounded shadow p-6 space-y-4 mx-auto"
                >
                    <h1 className="text-4xl font-bold mb-4 text-center p-6 text-dark-purple">Create Your Event</h1>
                    <div className="form-control w-full">
                        <label className="label">
                            <span className="label-text font-medium text-dark-purple">Event Name</span>
                        </label>
                        <input
                            type="text"
                            name="event_name"
                            value={formData.event_name}
                            onChange={handleChange}
                            className="input bg-gray-100 input-bordered w-full"
                            placeholder="Enter event name"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                        <DateTimeInput
                            label="Start Date for Registration"
                            name="start_date_register"
                            value={formData.start_date_register}
                            onChange={handleChange}
                            required
                        />
                        <DateTimeInput
                            label="End Date for Registration"
                            name="end_date_register"
                            value={formData.end_date_register}
                            onChange={handleChange}
                            required
                        />
                        <DateTimeInput
                            label="Start Date of Event"
                            name="start_date_event"
                            value={formData.start_date_event}
                            onChange={handleChange}
                            required
                        />
                        <DateTimeInput
                            label="End Date of Event"
                            name="end_date_event"
                            value={formData.end_date_event}
                            onChange={handleChange}
                            required
                        />
  
                    </div>
                    <div className="mt-6 w-full">
                        <FileInput
                            label="Event Banner"
                            name="event_file"
                            onChange={handleFileChange}
                            accept=".jpg,.jpeg,.png,.pdf"
                        />
                    </div>
                    <div className="form-control w-full ">
                        <label className="label">
                            <span className="label-text font-medium text-dark-purple">Maximum Attendees</span>
                        </label>
                        <input
                            type="number"
                            name="max_attendee"
                            value={formData.max_attendee}
                            onChange={handleChange}
                            className="input bg-gray-100 input-bordered w-full"
                            placeholder="Maximum number of attendees"
                            min="1"
                            required
                        />
                    </div>
                    <div className="mt-6">
                        <label className="label">
                            <span className="label-text font-medium text-dark-purple">Location</span>
                        </label>
                        <Map formData={formData} setFormData={setFormData} setError={setError} />
                    </div>
                    <div className="form-control w-full">
                        <label className="label">
                            <span className="label-text font-medium text-dark-purple">Description</span>
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
        </div>
    );
}

export default CreateEventForm;