import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { CiCalendar, CiGlobe, CiCircleInfo } from "react-icons/ci";
import { FiMapPin } from "react-icons/fi";
import { IoTicketOutline } from "react-icons/io5";
import BasicDetails from './sections/BasicDetails';
import LocationDetails from './sections/LocationDetails';
import DateTimeDetails from './sections/DateTimeDetails';
import TicketingDetails from './sections/TicketDetails';
import ContactDetails from './sections/ContactDetails';
import SocialMedia from './sections/SocialMedia';
import { ACCESS_TOKEN } from '../../constants';
import api from '../../api';
import { useNavigate } from 'react-router-dom';

export function CreateEventForm() {
  const [activeTab, setActiveTab] = useState('basic');
  const [loading, setLoading] = useState(false);
  const form = useForm({
    defaultValues: {
      is_online: false,
      is_free: true,
      visibility: 'PUBLIC',
      category: 'CONFERENCE',
      dress_code: 'CASUAL',
    },
  });
  const navigate = useNavigate();

  const formatDateTime = (dateTime) => {
    const date = new Date(dateTime);
    return date.toISOString(); // Formats to "YYYY-MM-DDTHH:MM:SS.sssZ"
  };

  const onSubmit = async (formValues) => {
    setLoading(true);
    try {
      const formData = new FormData();
  
      // Append form data fields
      formData.append('event_name', formValues.event_name);
      formData.append('start_date_register', formatDateTime(formValues.start_date_register) || '');
      formData.append('end_date_register', formatDateTime(formValues.end_date_register) || '');
      formData.append('start_date_event', formatDateTime(formValues.start_date_event) || '');
      formData.append('end_date_event', formatDateTime(formValues.end_date_event) || '');
      formData.append('max_attendee', parseInt(formValues.max_attendee, 10) || 0);
      formData.append('description', formValues.description || '');
      formData.append('category', formValues.category || 'CONFERENCE');
      formData.append('dress_code', formValues.dress_code || 'CASUAL');
      formData.append('visibility', formValues.visibility || 'PUBLIC');
      formData.append('is_online', Boolean(formValues.is_online));
      formData.append('is_free', Boolean(formValues.is_free));
      formData.append('ticket_price', formValues.is_free ? 0 : parseFloat(formValues.ticket_price || 0));
      formData.append('expected_price', formValues.is_free ? 0 : parseFloat(formValues.expected_price || 0));
      formData.append('address', formValues.address || '');
      formData.append('latitude', parseFloat(formValues.latitude || 0));
      formData.append('longitude', parseFloat(formValues.longitude || 0));
      formData.append('meeting_link', formValues.is_online ? (formValues.meeting_link || '') : '');
      formData.append('allowed_email_domains', formValues.allowed_email_domains || '');
      formData.append('detailed_description', formValues.detailed_description || '');
      formData.append('contact_email', formValues.contact_email || '');
      formData.append('contact_phone', formValues.contact_phone || '');
      formData.append('website_url', formValues.website_url || '');
      formData.append('facebook_url', formValues.facebook_url || '');
      formData.append('twitter_url', formValues.twitter_url || '');
      formData.append('instagram_url', formValues.instagram_url || '');
      formData.append('min_age_requirement', parseInt(formValues.min_age_requirement || 0, 10));
      formData.append('terms_and_conditions', formValues.terms_and_conditions || '');
      formData.append('tags', formValues.tags || '');
  
      // Optional fields
      formData.append('event_create_date', formatDateTime(new Date()));
      formData.append('engagement', JSON.stringify({}));
      formData.append('organizer', JSON.stringify(formValues.organizer || {}));
      formData.append('status', formValues.status || '');
      formData.append('status_registeration', formValues.status_registeration || '');
  
      // Handle image upload if provided
      if (formValues.image && formValues.image[0]) {
        formData.append('image', formValues.image[0]);
      }
  
      const token = localStorage.getItem(ACCESS_TOKEN);
      const headers = {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`,
      };
  
      const response = await api.post('/events/create-event', formData, { headers });
      alert("Event created successfully!");
      navigate("/"); // Redirect after success
    } catch (error) {
      console.error("Error creating event:", error);
      let errorMessage = "Failed to create event. Please try again.";
      if (error.response) {
        console.error("Error response data:", error.response.data);
        errorMessage = error.response.data?.error || errorMessage;
      }
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };
  

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
    <div className="container mx-auto py-10">
      <div className="card bg-white shadow-xl">
        <div className="card-body">
          <h2 className="card-title font-bold text-dark-purple text-5xl pb-7">Create Your Event</h2>

          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="tabs tabs-boxed bg-white">
              <button
                type="button"
                className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
                  ${activeTab === 'basic' 
                    ? 'bg-dark-purple text-white shadow-md ring-2'
                    : 'text-gray-600 hover:text-purple-700'}`}
                onClick={() => setActiveTab('basic')}
              >
                <CiCircleInfo className="mr-2 h-4 w-4" />
                Basic Details
              </button>
              <button
                type="button"
                className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
                  ${activeTab === 'location' 
                    ? 'bg-dark-purple text-white shadow-md ring-2 '
                    : 'text-gray-600 hover:text-purple-700'}`}
                onClick={() => setActiveTab('location')}
              >
                <FiMapPin className="mr-2 h-4 w-4" />
                Location
              </button>
              <button
                type="button"
                className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
                  ${activeTab === 'datetime' 
                    ? 'bg-dark-purple text-white shadow-md ring-2 '
                    : 'text-gray-600 hover:text-purple-700'}`}
                onClick={() => setActiveTab('datetime')}
              >
                <CiCalendar className="mr-2 h-4 w-4" />
                Date & Time
              </button>
              <button
                type="button"
                className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
                  ${activeTab === 'ticketing' 
                    ? 'bg-dark-purple text-white shadow-md ring-2'
                    : 'text-gray-600 hover:text-purple-700'}`}
                onClick={() => setActiveTab('ticketing')}
              >
                <IoTicketOutline className="mr-2 h-4 w-4" />
                Ticketing
              </button>
              <button
                type="button"
                className={`tab transition-all duration-200 hover:bg-gray-100 hover:text-purple-700 flex items-center
                  ${activeTab === 'contact' 
                    ? 'bg-dark-purple text-white shadow-md ring-2'
                    : 'text-gray-600 hover:text-purple-700'}`}
                onClick={() => setActiveTab('contact')}
              >
                <CiGlobe className="mr-2 h-4 w-4" />
                Contact & Social
              </button>
            </div>
            <div className="min-h-[500px] py-4">
              {renderTabContent()}
            </div>

            <div className="flex justify-end space-x-4 border-t pt-4">
              <button type="button" className="btn btn-outline">
                Save as Draft
              </button>
              <button type="submit" className="btn btn-primary">
                {loading ? "Creating..." : "Create Event"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
