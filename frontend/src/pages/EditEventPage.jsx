import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { CiCalendar, CiGlobe, CiCircleInfo } from "react-icons/ci";
import { FiMapPin } from "react-icons/fi";
import { IoTicketOutline } from "react-icons/io5";
import PageLayout from '../components/PageLayout';
import BasicDetails from '../components/CreateEvent/sections/BasicDetails';
import LocationDetails from '../components/CreateEvent/sections/LocationDetails';
import DateTimeDetails from '../components/CreateEvent/sections/DateTimeDetails';
import TicketingDetails from '../components/CreateEvent/sections/TicketDetails';
import ContactDetails from '../components/CreateEvent/sections/ContactDetails';
import SocialMedia from '../components/CreateEvent/sections/SocialMedia';
import { ACCESS_TOKEN } from '../constants';
import api from '../api';
import { useNavigate, useParams } from 'react-router-dom';

export default function EditEvent() {
  const { eventId } = useParams();
  const [activeTab, setActiveTab] = useState('basic');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const navigate = useNavigate();

  const form = useForm({
    defaultValues: {
      is_online: false,
      is_free: true,
      visibility: 'PUBLIC',
      category: 'CONFERENCE',
      dress_code: 'CASUAL',
    },
  });

  useEffect(() => {
    const fetchEventData = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const response = await api.get(`/events/${eventId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        const eventData = response.data;
        // Set form default values to the fetched data
        form.reset(eventData);
      } catch (error) {
        console.error("Error fetching event data:", error);
      } finally {
        setIsFetching(false);
      }
    };

    fetchEventData();
  }, [eventId, form]);

  // Format date/time to the required format
  const formatDateTime = (dateTime) => {
    const date = new Date(dateTime);
    return date.toISOString();
  };

  const onSubmit = async (formValues) => {
    setLoading(true);
    try {
      const formData = new FormData();
      const data = {
        ...formValues,
        start_date_register: formatDateTime(formValues.start_date_register),
        end_date_register: formatDateTime(formValues.end_date_register),
        start_date_event: formatDateTime(formValues.start_date_event),
        end_date_event: formatDateTime(formValues.end_date_event),
        updated_at: formatDateTime(new Date())
      };
      delete data.event_image;
      Object.entries(data).forEach(([key, value]) => {
        formData.append(key, value);
      });
      console.log(formValues.event_image);
      if (formValues.event_image !== undefined && formValues.event_image !== null && formValues.event_image instanceof File) {
        const imageFormData = new FormData();
        imageFormData.append('file', formValues.event_image);
  
        const imageResponse = await api.post(
          `/events/${eventId}/upload/event-image/`,
          imageFormData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        );
  
        console.log('Image uploaded:', imageResponse.data);
      }

      const token = localStorage.getItem(ACCESS_TOKEN);
      const headers = {
        'Content-Type': "application/json",
        'Authorization': `Bearer ${token}`,
      };
      console.log(eventId)
      const response = await api.patch(`/events/${eventId}/edit`, formData, { headers });
      console.log(response);
      alert("Event updated successfully!");
      navigate(`/events/${eventId}`);
    } catch (error) {
      console.error("Error updating event:", error);
      let errorMessage = "Failed to update event. Please try again.";
      if (error.response) {
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

  if (isFetching) {
    return <div>Loading event data...</div>;
  }

  return (
    <PageLayout>
    <div className="container mx-auto py-10">
      <div className="card bg-white shadow-xl">
        <div className="card-body">
          <h2 className="card-title font-bold text-dark-purple text-5xl pb-7">Edit Your Event</h2>

          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="tabs tabs-boxed bg-white">
              <button
                type="button"
                className={`tab ${activeTab === 'basic' ? 'bg-dark-purple text-white shadow-md ring-2' : 'text-gray-600'}`}
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
              <button type="submit" className="btn bg-amber-300 text-dark-purple">
                {loading ? "Updating..." : "Update Event"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    </PageLayout>
  );
}
