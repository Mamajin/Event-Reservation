
import { FaGlobe, FaFacebook, FaTwitter, FaInstagram, FaClock } from 'react-icons/fa';
import { CiMail } from "react-icons/ci";
import { FiPhone } from "react-icons/fi";
import { LuCalendarDays } from "react-icons/lu";
import { format } from 'date-fns';
  
  export function EventInfo({ event }) {
    const socialLinks = [
      { icon: FaGlobe, url: event.website_url, label: 'Website' },
      { icon: FaFacebook, url: event.facebook_url, label: 'Facebook' },
      { icon: FaTwitter, url: event.twitter_url, label: 'Twitter' },
      { icon: FaInstagram, url: event.instagram_url, label: 'Instagram' },
    ].filter(link => link.url);
  
    return (
      <div className="container bg-white py-8 min-h-screen">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-full">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8 flex flex-col">
            <div className="card bg-white flex-grow">
              <div className="card-body">
                <h2 className="card-title text-2xl mb-4 text-dark-purple">About the Event</h2>
                <p className="whitespace-pre-wrap text-base-content/80 leading-relaxed">
                  {event.detailed_description || event.description}
                </p>
              </div>
            </div>
    
            <div className="card bg-white flex-grow">
              <div className="card-body">
                <h2 className="card-title text-2xl mb-4 text-dark-purple">Terms & Conditions</h2>
                <p className="whitespace-pre-wrap text-base-content/80 leading-relaxed">
                  {event.terms_and_conditions}
                </p>
              </div>
            </div>
          </div>
    
          {/* Sidebar */}
          <div className="space-y-6 flex flex-col">
            {/* Date & Time */}
            <div className="card bg-base flex-grow">
              <div className="card-body">
                <h3 className="font-semibold text-lg mb-4 text-dark-purple">Date & Time</h3>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <LuCalendarDays className="h-5 w-5 mt-1 text-dark-purple" />
                    <div>
                      <p className="font-medium text-dark-purple">Start</p>
                      <p className="text-sm text-base-content/70">
                        {format(new Date(event.start_date_event), 'PPP')}
                      </p>
                      <p className="text-sm text-base-content/70">
                        {format(new Date(event.start_date_event), 'p')}
                      </p>
                    </div>
                  </div>
                  <div className="divider my-2"></div>
                  <div className="flex items-start gap-3">
                    <FaClock className="h-5 w-5 mt-1 text-dark-purple" />
                    <div>
                      <p className="font-medium text-dark-purple">End</p>
                      <p className="text-sm text-base-content/70">
                        {format(new Date(event.end_date_event), 'PPP')}
                      </p>
                      <p className="text-sm text-base-content/70">
                        {format(new Date(event.end_date_event), 'p')}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
    
            {/* Contact Information */}
            <div className="card bg-white flex-grow">
              <div className="card-body">
                <h3 className="font-semibold text-dark-purple text-lg mb-4">Contact Information</h3>
                <div className="space-y-4">
                  {event.contact_email && (
                    <div className="flex items-center gap-3">
                      <CiMail className="h-5 w-5 text-dark-purple" />
                      <a href={`mailto:${event.contact_email}`} className="link link-primary">
                        {event.contact_email}
                      </a>
                    </div>
                  )}
                  {event.contact_phone && (
                    <div className="flex items-center gap-3">
                      <FiPhone className="h-5 w-5 text-primary" />
                      <a href={`tel:${event.contact_phone}`} className="link link-primary">
                        {event.contact_phone}
                      </a>
                    </div>
                  )}
                </div>
              </div>
            </div>
    
            {/* Social Links */}
            {socialLinks.length > 0 && (
              <div className="card bg-base-100 flex-grow">
                <div className="card-body">
                  <h3 className="font-semibold text-lg mb-4">Social Media</h3>
                  <div className="flex flex-wrap gap-4">
                    {socialLinks.map(({ icon: Icon, url, label }) => (
                      <a
                        key={label}
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-circle btn-ghost"
                      >
                        <Icon className="h-5 w-5" />
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