import React, { useEffect, useState } from 'react';
import api from '../api';
import EventCard from '../components/EventCard';
import PageLayout from '../components/PageLayout';
import Sidebar from '../components/Discovery/Sidebar';
import { LuSearch, LuTag  } from "react-icons/lu";
import { ACCESS_TOKEN } from '../constants';

function Discover() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState('');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const response = await api.get('/events/events', { headers });
        console.log(response.data);
        setEvents(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }


  const filteredEvents = events.filter((event) => {
    const matchesSearch = event.event_name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesTags = selectedTags.length === 0 || 
      selectedTags.some((tag) => event.tags.split(',').includes(tag));
    const matchesStatus = !selectedStatus || event.status === selectedStatus;

    return matchesSearch && matchesTags && matchesStatus;
  });

  return (
    <PageLayout>
      <div className="min-h-screen bg-gray-50 w-full relative overflow-hidden">
        <main className="w-full mx-auto px-4 py-8">
        <div className="flex gap-8 max-w-7xl mx-auto">
            {/* Main Content */}
            <div className="flex-1 overflow-y-auto">
              <div className="mb-8 space-y-4">
                <div className="relative">
                  <LuSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <input
                    type="search"
                    placeholder="Search events..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg bg-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                <div className="flex flex-wrap gap-2">
                {["UPCOMING", "ONGOING", "COMPLETED"].map((status) => (
                    <button
                      key={status}
                      onClick={() =>
                        setSelectedStatus((prev) =>
                          prev === status ? "" : status
                        )
                      }
                      className={`flex items-center px-3 py-1 rounded-full text-sm ${
                        selectedStatus === status
                          ? "bg-indigo-600 text-white"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      }`}
                    >
                      {status}
                    </button>
                  ))}
                  {[
                    ...new Set(
                      events
                        .flatMap((event) => (event.tags ? event.tags.split(",") : []))
                    ),
                  ].map((tag) => (
                    <button
                      key={tag}
                      onClick={() =>
                        setSelectedTags((prev) =>
                          prev.includes(tag)
                            ? prev.filter((t) => t !== tag)
                            : [...prev, tag]
                        )
                      }
                      className={`flex items-center px-3 py-1 rounded-full text-sm ${
                        selectedTags.includes(tag)
                          ? "bg-indigo-600 text-white"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      }`}
                    >
                      <LuTag className="h-4 w-4 mr-1" />
                      {tag}
                    </button>
                  ))}
                </div>
                {filteredEvents.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-1 gap-6">
                    {filteredEvents.map((event) => (
                      <EventCard key={event.id} event={event} />
                    ))}
                  </div>
                ) : (
                  <h2 className="flex items-center font-bold justify-center h-64 text-4xl text-dark-purple">
                    No events found
                  </h2>
                )}
              </div>
            </div>
            {/* Sidebar */}
            <div className="w-1/4">
              <Sidebar
                events={events}
                selectedDate={selectedDate}
                onSelectDate={setSelectedDate}
              />
            </div>
          </div>
        </main>
      </div>
    </PageLayout>
  );
}

export default Discover;
