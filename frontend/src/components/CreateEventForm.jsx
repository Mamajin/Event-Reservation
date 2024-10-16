import React, { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import qs from 'qs';

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
            
            const formDataString = qs.stringify(payload); // Convert payload to URL-encoded string

            const res = await api.post("/api/events/create-event", formDataString, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
            });
            alert("Event created successfully!");
            navigate("/");
        } catch (error) {
            console.error("Error creating event:", error);
            let errorMessage = "Failed to create event. Please try again.";
            if (error.response) {
                errorMessage = error.response.data?.message || error.response.statusText || errorMessage;
            }
            alert(errorMessage);
        } finally {
            setLoading(false);
        }
    };
}


export default CreateEventForm;