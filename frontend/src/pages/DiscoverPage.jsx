import React, { useEffect, useState } from 'react';
import api from '../api';
import EventCard from '../components/EventCard';
import PageLayout from '../components/PageLayout';
import Sidebar from '../components/Discovery/Sidebar';
import { MdOutlineCategory } from "react-icons/md";
import { LuSearch, LuTag, LuClock,LuChevronUp, LuChevronDown, LuListFilter } from "react-icons/lu";
import { ACCESS_TOKEN } from '../constants';

export default function Discover() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [showAllTags, setShowAllTags] = useState(false);
  const [sortBy, setSortBy] = useState('');
  const MAX_VISIBLE_TAGS = 6;

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
  
  const categories = [...new Set(events.flatMap((event => event.category))
  ),
  ];

  const uniqueTags = [
    ...new Set(events.flatMap((event) => (event.tags ? event.tags.split(",") : []))
    ),
  ];
  const visibleTags = showAllTags 
    ? uniqueTags 
    : uniqueTags.slice(0, MAX_VISIBLE_TAGS);
  const hasMoreTags = uniqueTags.length > MAX_VISIBLE_TAGS;

  const filteredEvents = events
  .filter((event) => {
    const matchesTags =
      selectedTags.length === 0 ||
      selectedTags.some((tag) => event.tags.split(",").includes(tag));
    const matchesSearch = event.event_name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesDate =
      !selectedDate ||
      new Date(event.start_date_event).toDateString() ===
        selectedDate.toDateString();
    const matchesStatus = !selectedStatus || event.status === selectedStatus;
    const matchesCategory = !selectedCategory || event.category === selectedCategory;
    return (
      matchesTags &&
      matchesSearch &&
      matchesDate &&
      matchesStatus &&
      matchesCategory
    );
  })
  .sort((a, b) => {
    if (sortBy === 'POPULARITY') {
      return b.engagement.total_like - a.engagement.total_like ; // Sort descending by likes
    }
    if (sortBy === 'DATE') {
      return new Date(b.start_date_event) - new Date(a.start_date_event); // Sort descending by date
    }
    return 0; // Default: no sorting
  });

  return (
    <PageLayout>
      <div className="min-h-screen bg-gray-50 w-full relative overflow-hidden">
        <main className="w-full mx-auto px-4 py-8">
        <div className="flex gap-8 max-w-7xl mx-auto">
            {/* Main Content */}
            <div className="flex-1 overflow-y-auto">
              <div className="mb-8 space-y-4">
              <div className="flex items-center gap-4">
                <div className="relative w-7/12 max-w">
                  <LuSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <input
                    type="search"
                    placeholder="Search events..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg bg-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                <div className="dropdown">
                  <label
                    tabIndex={0}
                    className="btn btn-sm bg-dark-purple hover:bg-gray-100 hover:text-black text-white px-4 py-2 rounded-md transition-colors duration-300 flex items-center gap-2"
                  >
                    <LuClock className="h-4 w-4" />
                    <span className="hidden sm:block">Status</span>
                  </label>
                  <ul
                    tabIndex={0}
                    className="dropdown-content menu p-1 shadow bg-white rounded-box w-40 text-sm"
                  >
                    {['UPCOMING', 'ONGOING', 'COMPLETED'].map((status) => (
                      <li key={status}>
                        <button
                          onClick={() => setSelectedStatus(selectedStatus === status ? null : status)}
                          className={`flex items-center gap-2 px-2 py-1 rounded-md ${
                            selectedStatus === status
                              ? 'bg-indigo-600 text-white'
                              : 'hover:bg-gray-200 text-gray-700'
                          }`}
                        >
                          {status.charAt(0) + status.slice(1).toLowerCase()}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="dropdown">
                  <label
                    tabIndex={0}
                    className="btn btn-sm bg-dark-purple text-white hover:bg-gray-100 hover:text-black px-4 py-2 rounded-md transition-colors duration-300 flex items-center gap-2"
                  >
                    <MdOutlineCategory className="h-4 w-4"/>
                    <span className="hidden inline-block sm:inline-block">Category</span>
                  </label>
                  <ul
                    tabIndex={0}
                    className="dropdown-content menu p-1 shadow bg-white rounded-box w-40 text-sm"
                  >
                    {categories.map((category) => (
                      <li key={category}>
                        <button
                          onClick={() => setSelectedCategory(selectedStatus === category ? null : category)}
                          className={`flex items-center gap-2 px-2 py-1 rounded-md ${
                            selectedStatus === category
                              ? 'bg-indigo-600 text-white'
                              : 'hover:bg-gray-200 text-gray-700'
                          }`}
                        >
                          {category.charAt(0) + category.slice(1).toLowerCase()}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="dropdown">
                  <label
                    tabIndex={0}
                    className="btn btn-sm bg-dark-purple hover:bg-gray-100 hover:text-black text-white px-4 py-2 rounded-md transition-colors duration-300 flex items-center gap-2"
                  >
                    <LuListFilter className="h-4 w-4" />
                    <span className="hidden sm:block">Sort By</span>
                  </label>
                  <ul
                    tabIndex={0}
                    className="dropdown-content menu p-1 shadow bg-white rounded-box w-40 text-sm"
                  >
                    {['POPULARITY', 'DATE'].map((sortOption) => (
                      <li key={sortOption}>
                        <button
                          onClick={() => setSortBy(sortOption)}
                          className={`flex items-center gap-2 px-2 py-1 rounded-md ${
                            sortBy === sortOption
                              ? 'bg-indigo-600 text-white'
                              : 'hover:bg-gray-200 text-gray-700'
                          }`}
                        >
                          {sortOption.charAt(0) + sortOption.slice(1).toLowerCase()}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
                <div className="flex flex-wrap gap-2">
                  {visibleTags.map((tag) => (
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
                    {hasMoreTags && (
                      <button
                        variant="ghost"
                        size="sm"
                        onClick={() => setShowAllTags(!showAllTags)}
                        className="flex items-center text-sm text-gray-600 hover:text-gray-900"
                      >
                        {showAllTags ? (
                          <>
                            <LuChevronUp className="h-4 w-4 mr-1 inline-block align-middle" />
                            Show Less Tags
                          </>
                        ) : (
                          <>
                            <LuChevronDown className="h-4 w-4 mr-1 inline-block align-middle" />
                            Show {uniqueTags.length - MAX_VISIBLE_TAGS} More Tags
                          </>
                        )}
                      </button>
                    )}
                </div>
                {filteredEvents.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
