import React, { useState } from 'react';

function OrganizerForm() {
    const [formData, setFormData] = useState({
        organizer_name: '',
        email: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    return (
        <div>
            <h1>Organizer Form</h1>
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
        </div>
    );
}

export default OrganizerForm;