
import { FaGlobe, FaFacebook, FaTwitter, FaInstagram, FaClock } from 'react-icons/fa';
import { CiMail } from "react-icons/ci";
import { FiPhone } from "react-icons/fi";
import { LuCalendarDays, LuUsers } from "react-icons/lu";
import { format } from 'date-fns';
import { CommentSection } from './Comment';
import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import api from '../../../api';
import { IoVideocam } from "react-icons/io5";


export function EventInfo({ event }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [applyError, setApplyError] = useState(null);
    const [applySuccess, setApplySuccess] = useState(false);
    const [isApplied, setIsApplied] = useState(false);
    const navigate = Navigate

    const socialLinks = [
      { icon: FaGlobe, url: event.website_url, label: 'Website' },
      { icon: FaFacebook, url: event.facebook_url, label: 'Facebook' },
      { icon: FaTwitter, url: event.twitter_url, label: 'Twitter' },
      { icon: FaInstagram, url: event.instagram_url, label: 'Instagram' },
    ].filter(link => link.url);

    const handleApplyEvent = async () => {
      setLoading(true);
      setApplyError(null);
      setApplySuccess(false);
  
      try {
        const response = await api.post(`/tickets/event/${event.id}/register`);
        alert("Event apply successfully!");
        setIsApplied(true);
        navigate("/applied-events");
      } catch (error) {
        console.error("Error apply event:", error);
        let errorMessage = "Failed to apply for the event.";
        if (error.response) {
            errorMessage = error.response.data?.error || errorMessage;
        }
        alert(errorMessage);
        navigate("/discover");
      } finally {
        setLoading(false);
      }
    };
    return (
      <div className="container bg-gray-50 py-8 min-h-screen ">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-full">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8 flex flex-col">
          <div className="space-y-8">
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h2 className="text-2xl font-semibold mb-4 text-dark-purple">About the Event</h2>
              <p className="text-gray-600 leading-relaxed break-words">
                {event.detailed_description || event.description}
              </p>
            </div>
          </div>

            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h2 className="text-2xl font-semibold mb-4 text-dark-purple">Terms & Conditions</h2>
              <p className="text-gray-600 leading-relaxed whitespace-pre-wrap break-words">
                {event.terms_and_conditions}
              </p>
            </div>

            <CommentSection event={event}/>
          </div>
    
          {/* Sidebar */}
          <div className="space-y-6 flex flex-col">
            {/* Date & Time */}
            <div className="card bg-white">
              <div className="card-body">
                <h3 className="font-semibold text-lg mb-4 text-dark-purple">Date & Time</h3>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <LuCalendarDays className="h-5 w-5 mt-1 text-dark-purple" />
                    <div>
                      <p className="font-medium text-dark-purple">Start</p>
                      <p className="text-sm text-gray-600">
                        {format(new Date(event.start_date_event), 'PPP')}
                      </p>
                      <p className="text-sm text-gray-600">
                        {format(new Date(event.start_date_event), 'p')}
                      </p>
                    </div>
                  </div>
                  <div className="divider my-2"></div>
                  <div className="flex items-start gap-3">
                    <FaClock className="h-5 w-5 mt-1 text-dark-purple" />
                    <div>
                      <p className="font-medium text-dark-purple">End</p>
                      <p className="text-sm text-gray-600">
                        {format(new Date(event.end_date_event), 'PPP')}
                      </p>
                      <p className="text-sm text-gray-600">
                        {format(new Date(event.end_date_event), 'p')}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          {/* Registration */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-xl font-semibold mb-4 text-dark-purple">Registration Details</h3>
        <div className="space-y-4 mb-6">
          <p className="flex items-center gap-2 text-gray-600">
            <LuUsers className="w-5 h-5 text-dark-purple" />
            {event.max_attendee === 0 ? "No attendees limit" : `Limited to ${event.max_attendee} attendees attendees max`}
          </p>
          <p className="flex items-center gap-2 text-gray-600">
            <LuCalendarDays className="w-5 h-5 text-dark-purple" />
            Registration closes {new Date(event.end_date_register).toLocaleDateString()}
          </p>
        </div>
        <button
          onClick={handleApplyEvent}
          disabled={isApplied}
          className={`w-full py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors ${
            isApplied
              ? 'bg-green-600 text-white cursor-not-allowed'
              : 'bg-dark-purple hover:bg-green-600 text-white'
          }`}
        >
          {isApplied ? (
            <>
              <CheckCircle className="w-5 h-5" />
              Applied Successfully
            </>
          ) : (
            'Apply Now'
          )}
        </button>
        {isApplied && (
          <p className="text-center text-sm text-gray-600 mt-2">
            We'll contact you with further details
          </p>
        )}
      </div>
            {/* Contact Information */}
            <div className="card bg-white">
              <div className="card-body">
                <h3 className="font-semibold text-dark-purple text-lg mb-4">Contact Information</h3>
                <div className="space-y-4">
                  {event.contact_email && (
                    <div className="flex items-center gap-3">
                      <CiMail className="h-5 w-5 text-dark-purple" />
                      <a href={`mailto:${event.contact_email}`} className="link link-dark-purple">
                        {event.contact_email}
                      </a>
                    </div>
                  )}
                  {event.contact_phone && (
                    <div className="flex items-center gap-3">
                      <FiPhone className="h-5 w-5 text-dark-purple" />
                      <a href={`tel:${event.contact_phone}`} className="link link-dark-purple">
                        {event.contact_phone}
                      </a>
                    </div>
                  )}
                </div>
              </div>
            </div>
    
            {/* Social Links */}
            {socialLinks.length > 0 && (
              <div className="card bg-white">
                <div className="card-body">
                  <h3 className="font-semibold text-dark-purple text-lg mb-4">Social Media</h3>
                  <div className="flex flex-wrap gap-4">
                    {socialLinks.map(({ icon: Icon, url, label }) => (
                      <a
                        key={label}
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-circle btn-ghost"
                      >
                        <Icon className="h-5 w-5 text-dark-purple" />
                      </a>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }