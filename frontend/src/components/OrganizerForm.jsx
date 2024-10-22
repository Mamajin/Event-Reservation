import React, { useState } from 'react';

function OrganizerForm() {
    const [formData, setFormData] = useState({
        organizer_name: '',
        email: '',
    });

    return (
        <div>
            <h1>Organizer Form</h1>
        </div>
    );
}

export default OrganizerForm;