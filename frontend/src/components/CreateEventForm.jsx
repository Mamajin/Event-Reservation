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
}

export default CreateEventForm;