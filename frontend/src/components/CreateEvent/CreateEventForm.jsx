import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import BasicDetails from './sections/BasicDetails';
import LocationDetails from './sections/LocationDetails';
import DateTimeDetails from './sections/DateTimeDetails';
import TicketingDetails from './sections/TicketDetails'
import ContactDetails from './sections/ContactDetails';
import SocialMedia from './sections/SocialMedia';
import { CiCircleInfo } from 'react-icons/ci';

const EventForm = () => {
  const [activeTab, setActiveTab] = useState('basic');
  const form = useForm({
    defaultValues: {
      is_online: false,
      is_free: true,
      visibility: 'PUBLIC',
      category: 'CONFERENCE',
      dress_code: 'CASUAL',
    },
  });

  const renderTabContent = () => {
    switch (activeTab) {
      case 'basic':
        return <BasicDetails form={form} />;
      case 'location':
        return <LocationDetails form={form} />;
      case 'datetime':
        return <DateTimeDetails form={form} />;
      case 'ticketing':
        return <TicketingDetails form={form} />;
      case 'contact':
        return (
          <div className="grid gap-6">
            <ContactDetails form={form} />
            <SocialMedia form={form} />
          </div>
        );
      default:
        return <BasicDetails form={form} />;
    }
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      <div className="flex space-x-4">
        <button
          type="button"
          className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
            ${activeTab === 'basic' ? 'bg-dark-purple text-white shadow-md ring-2' : 'text-gray-600 hover:text-purple-700'}`}
          onClick={() => setActiveTab('basic')}
        >
          <CiCircleInfo className="mr-2 h-4 w-4" />
          Basic Details
        </button>
        <button
          type="button"
          className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
            ${activeTab === 'location' ? 'bg-dark-purple text-white shadow-md ring-2' : 'text-gray-600 hover:text-purple-700'}`}
          onClick={() => setActiveTab('location')}
        >
          Location
        </button>
        <button
          type="button"
          className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
            ${activeTab === 'datetime' ? 'bg-dark-purple text-white shadow-md ring-2' : 'text-gray-600 hover:text-purple-700'}`}
          onClick={() => setActiveTab('datetime')}
        >
          Date & Time
        </button>
        <button
          type="button"
          className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
            ${activeTab === 'ticketing' ? 'bg-dark-purple text-white shadow-md ring-2' : 'text-gray-600 hover:text-purple-700'}`}
          onClick={() => setActiveTab('ticketing')}
        >
          Ticketing
        </button>
        <button
          type="button"
          className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
            ${activeTab === 'contact' ? 'bg-dark-purple text-white shadow-md ring-2' : 'text-gray-600 hover:text-purple-700'}`}
          onClick={() => setActiveTab('contact')}
        >
          Contact & Social
        </button>
      </div>

      <div className="mt-4">{renderTabContent()}</div>
      <button
        type="submit"
        className="btn btn-primary w-full py-3 mt-6"
      >
        Create Event
      </button>
    </form>
  );
};

export default EventForm;
