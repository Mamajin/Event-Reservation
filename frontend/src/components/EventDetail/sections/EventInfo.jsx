
import { FaGlobe, FaFacebook, FaTwitter, FaInstagram, FaClock, FaRegCheckCircle } from 'react-icons/fa';
import { CiMail } from "react-icons/ci";
import { FiPhone } from "react-icons/fi";
import { LuCalendarDays, LuUsers, LuShirt } from "react-icons/lu";
import { format } from 'date-fns';
import { CommentSection } from './Comment';
import { useState, useEffect } from 'react';
import api from '../../../api';
import ApplicantsList from './ApplicantsList';
import { ACCESS_TOKEN, USER_ID } from '../../../constants';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
export function EventInfo({ event }) {
  const [loading, setLoading] = useState(false);
  const [isApplied, setIsApplied] = useState(false);
  const [canceling, setCanceling] = useState(false);
  const [ticketId, setTicketId] = useState(null);
  const [attendees, setAttendees] = useState([]);
  const [showApplicants, setShowApplicants] = useState(false);
  const userId = localStorage.getItem(USER_ID);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      if (event?.user_engaged) {
        setIsApplied(event.user_engaged.is_applied);
        const fetchTicket = async () => {
          try {
            const token = localStorage.getItem(ACCESS_TOKEN);
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const response = await api.get(`/tickets/user/${userId}`, { headers });
            const tickets = response.data;

            const ticket = tickets.find(ticket => ticket.event_id === event.id);
            if (ticket) {
              setTicketId(ticket.id);
            }
          } catch (error) {
            console.error("Error fetching tickets:", error);
          }
        };


        const fetchAttendees = async () => {
          try {
            const token = localStorage.getItem(ACCESS_TOKEN);
            // Only fetch attendees if user is event owner or has applied to the event
            if (event.user_id === userId || isApplied) {
              const headers = token ? { Authorization: `Bearer ${token}` } : {};
              const response = await api.get(`/events/${event.id}/attendee-list`, { headers });
              const attendees = response.data;
              setAttendees(attendees);
            }
          } catch (error) {
            // Check if it's a 403 error and handle accordingly
            if (error.response?.status === 403) {
              console.warn("Not authorized to view attendee list");
            } else {
              console.error("Error fetching attendees:", error);
            }
          }
        };

        fetchTicket();
        fetchAttendees();
      }
    }
  }, [userId, event.id, event.user_id, isApplied]);

  const socialLinks = [
    { icon: FaGlobe, url: event.website_url, label: 'Website' },
    { icon: FaFacebook, url: event.facebook_url, label: 'Facebook' },
    { icon: FaTwitter, url: event.twitter_url, label: 'Twitter' },
    { icon: FaInstagram, url: event.instagram_url, label: 'Instagram' },
  ].filter(link => link.url);

  const handleApplyEvent = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) {
      navigate('/login');
      return;
    }
    setLoading(true);

    try {

      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      await api.post(`/tickets/event/${event.id}/register`, {}, { headers });
      alert("Event applied successfully!");
      setIsApplied(true);
      window.location.reload();
    } catch (error) {
      let errorMessage = "Failed to apply for the event.";
      if (error.response) {
        errorMessage = error.response.data?.error || errorMessage;
      }
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleUnapplyEvent = async () => {
    setCanceling(true);
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      await api.delete(`/tickets/${ticketId}/cancel`, { headers });
      alert("You have successfully unapplied from the event!");
      setIsApplied(false);
      window.location.reload();
    } catch (error) {
      let errorMessage = "Failed to unapply from the event.";
      if (error.response) {
        errorMessage = error.response.data?.error || errorMessage;
      }
      alert(errorMessage);
    } finally {
      setCanceling(false);
    }
  };
  return (
    <div className="container bg-gray-50 py-8 min-h-screen ">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-full">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8 flex flex-col">
<div className="bg-white rounded-xl p-6 shadow-sm w-full">
  <h2 className="text-2xl font-semibold mb-4 text-dark-purple">About the Event</h2>
  <div className="prose text-gray-800 leading-relaxed">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
             
              >
                {event.detailed_description}
              </ReactMarkdown>
            </div>
</div>

{event.terms_and_conditions && (
  <div className="bg-white rounded-xl p-6 shadow-sm mt-6 w-full">
    <h2 className="text-2xl font-semibold mb-4 text-dark-purple">Terms & Conditions</h2>
    <div className="prose text-gray-800 leading-relaxed">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  
                >
                  {event.terms_and_conditions}
                </ReactMarkdown>
              </div>
  </div>
)}


          <CommentSection event={event} />
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

          {/* Dress Code */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4 text-dark-purple">Dress Code</h2>
            <p className="flex items-center gap-2 text-gray-600">
              <LuShirt className="h-5 w-5 text-dark-purple" />
              {event.dress_code.charAt(0) + event.dress_code.slice(1).toLowerCase()}
            </p>
          </div>

          {/* Registration */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold mb-4 text-dark-purple">Registration Details</h3>
            <div className="space-y-4 mb-6">
              <button
                onClick={() => setShowApplicants(true)}
                disabled={attendees.length === 0}
                className={`flex items-center gap-2 text-gray-600 ${attendees.length === 0 ? 'opacity-50' : 'hover:text-blue-600 transition-colors'
                  }`}
              >
                <LuUsers className="w-5 h-5 text-dark-purple" />
                {attendees.length === 0 ? (
                  event.max_attendee === null ? (
                    'No attendee limit'
                  ) : (
                    `Limited to ${event.max_attendee} attendees`
                  )
                ) : (
                  `View ${attendees.length} applicants`
                )} </button>
              <p className="flex items-center gap-2 text-gray-600">
                <LuCalendarDays className="w-5 h-5 text-dark-purple" />
                Registration closes {new Date(event.end_date_register).toLocaleDateString()}
              </p>
            </div>
            <button
              onClick={isApplied ? handleUnapplyEvent : handleApplyEvent}
              disabled={loading || canceling}
              className={`w-full py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors ${(loading || canceling)
                ? 'bg-gray-300 text-gray-700 cursor-not-allowed'
                : isApplied
                  ? 'bg-red-400 hover:bg-red-700 text-white'
                  : 'bg-dark-purple hover:bg-green-600 text-white'
                }`}
            >
              {loading || canceling ? (
                <>
                  <span className="loader"></span>
                  {isApplied ? "Unapplying..." : "Applying..."}
                </>
              ) : isApplied ? (
                <>
                  <FaRegCheckCircle className="w-5 h-5" />
                  Unapply
                </>
              ) : (
                'Apply Now'
              )}
            </button>

            {isApplied && (
              <p className="text-center text-sm text-gray-600 mt-2">
                Cancel your Ticket?
              </p>
            )}
          </div>

          {/* Contact Information */}
          {(event.contact_email || event.contact_phone) && (
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
            </div>)}
          {/* Social Links */}
          {socialLinks.length > 0 || event.other_url && (
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
                  {event.other_url && (
                    <div className="flex flex-wrap gap-4">
                      {event.other_url.split(',').map((url, index) => (
                        <a
                          key={index}
                          href={url.trim()}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn btn-circle btn-ghost"
                        >
                          <FaGlobe className="h-5 w-5 text-dark-purple" />
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      <ApplicantsList
        isOpen={showApplicants}
        onClose={() => setShowApplicants(false)}
        applicants={attendees}
      />
    </div>
  );
}