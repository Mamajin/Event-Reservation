import React from 'react';
import { EditEventForm } from '../components/CreateEvent/EditEventForm';

function EditEventPage() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-4xl font-bold mb-6">Edit Event</h1>
      <EditEventForm />
    </div>
  );
}

export default EditEventPage;