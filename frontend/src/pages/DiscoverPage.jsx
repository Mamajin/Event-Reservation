import React, { useEffect, useState, useRef } from 'react';
import api from '../api';
import EventCard from '../components/Discovery/EventCard';
import PageLayout from '../components/PageLayout';
import Sidebar from '../components/Discovery/Sidebar';
import { MdOutlineCategory } from "react-icons/md";
import { LuSearch, LuTag, LuClock, LuChevronUp, LuChevronDown, LuListFilter, LuGlobe2, LuChevronLeft, LuChevronRight } from "react-icons/lu";
import { ACCESS_TOKEN } from '../constants';
import Loading from '../components/LoadingIndicator';
export default function Discover() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedvisibility, setSelectedVisibility] = useState('');
  const [showAllTags, setShowAllTags] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const EVENTS_PER_PAGE = 6;
  const MAX_VISIBLE_TAGS = 6;
  const eventListRef = useRef(null);
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, selectedTags, selectedStatus, selectedCategory, selectedvisibility, selectedDate]);

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

  useEffect(() => {
    if (eventListRef.current) {
      eventListRef.current.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }, [currentPage]);

  if (loading) {
    return (
      <Loading></Loading>
  );
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
    const matchesvisibility = !selectedvisibility || event.visibility === selectedvisibility;
    return (
      matchesTags &&
      matchesSearch &&
      matchesDate &&
      matchesStatus &&
      matchesCategory &&
      matchesvisibility
    );
  })

  const indexOfLastEvent = currentPage * EVENTS_PER_PAGE;
  const indexOfFirstEvent = indexOfLastEvent - EVENTS_PER_PAGE;
  const currentEvents = filteredEvents.slice(indexOfFirstEvent, indexOfLastEvent);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const totalPages = Math.ceil(filteredEvents.length / EVENTS_PER_PAGE);
  return (
    <PageLayout>
      <div className="min-h-screen bg-gray-50 w-full relative overflow-hidden">
        <main className="w-full mx-auto px-4 py-8">
        <div className="flex gap-8 max-w-7xl mx-auto">
            {/* Main Content */}
            <div className="flex-1 overflow-y-auto">
              <div className="mb-8 space-y-4">
              <div className="flex items-center gap-4 overflow-visible">
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
                    className="btn btn-sm w-36 bg-dark-purple hover:bg-gray-100 hover:text-black text-white px-4 py-2 rounded-md transition-colors duration-300 flex items-center gap-2"
                  >
                    <LuClock className="h-4 w-4" />
                    <span className="hidden sm:block">{selectedStatus ? `${selectedStatus.charAt(0) + selectedStatus.slice(1).toLowerCase()}` : 'Status'}</span>
                </label>
                  <ul
                    tabIndex={0}
                    className="dropdown-content menu p-1 shadow bg-white rounded-box w-40 text-sm z-50"
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
                    className="btn btn-sm bg-dark-purple w-36 text-white hover:bg-gray-100 hover:text-black px-4 py-2 rounded-md transition-colors duration-300 flex items-center gap-2"
                  >
                    <MdOutlineCategory className="h-4 w-4"/>
                    <span className="hidden sm:block">{selectedCategory ? `${selectedCategory.charAt(0) + selectedCategory.slice(1).toLowerCase()}` : 'Category'}</span>
                  </label>
                  <ul
                    tabIndex={0}
                    className="dropdown-content menu p-1 shadow bg-white rounded-box w-40 text-sm z-50"
                  >
                    {categories.map((category) => (
                      <li key={category}>
                        <button
                          onClick={() => setSelectedCategory(selectedCategory === category ? null : category)}
                          className={`flex items-center gap-2 px-2 py-1 rounded-md ${
                            selectedCategory === category
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
                  className="btn btn-sm w-32 bg-dark-purple hover:bg-gray-100 hover:text-black text-white px-4 py-2 rounded-md transition-colors duration-300 flex items-center gap-2"
                >
                  <LuGlobe2 className="h-4 w-4" />
                  <span className="hidden sm:block">{selectedvisibility ? `${selectedvisibility.charAt(0) + selectedvisibility.slice(1).toLowerCase()}` : 'Visibility'}</span>
                </label>
                <ul
                  tabIndex={0}
                  className="dropdown-content menu p-1 shadow bg-white rounded-box w-40 text-sm z-50"
                >
                  {['PUBLIC', 'PRIVATE'].map((visibility) => (
                    <li key={visibility}>
                      <button
                        onClick={() => setSelectedVisibility(selectedvisibility === visibility ? null : visibility)}
                        className={`flex items-center gap-2 px-2 py-1 rounded-md ${
                          selectedvisibility === visibility
                            ? 'bg-indigo-600 text-white'
                            : 'hover:bg-gray-200 text-gray-700'
                        }`}
                      >
                        {visibility.charAt(0) + visibility.slice(1).toLowerCase()}
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
                <div 
                  ref={eventListRef}
                  className='flex flex-col h-[900px] overflow-y-auto z-0 relative'
                >
                  {filteredEvents.length > 0 ? (
                    <>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {currentEvents.map((event) => (
                          <EventCard key={event.id} event={event} />
                        ))}
                      </div>
                      
                      {/* Pagination */}
                      <div className="sticky bottom-0 bg-white/90 backdrop-blur-sm py-4 z-50">
                        <div className="flex justify-center items-center space-x-4">
                          <button 
                            onClick={() => paginate(currentPage - 1)} 
                            disabled={currentPage === 1}
                            className="btn btn-ghost btn-sm disabled:opacity-0"
                          >
                            <LuChevronLeft className="h-5 w-5" />
                          </button>
                          
                          <div className="join">
                            {[...Array(totalPages)].map((_, index) => (
                              <button
                                key={index}
                                onClick={() => paginate(index + 1)}
                                className={`join-item btn btn-sm ${
                                  currentPage === index + 1 
                                    ? 'btn-active bg-dark-purple text-white' 
                                    : 'btn-ghost'
                                }`}
                              >
                                {index + 1}
                              </button>
                            ))}
                          </div>
                          
                          <button 
                            onClick={() => paginate(currentPage + 1)} 
                            disabled={currentPage === totalPages}
                            className="btn btn-ghost btn-sm disabled:opacity-0"
                          >
                            <LuChevronRight className="h-5 w-5" />
                          </button>
                        </div>
                      </div>
                    </>
                  ) : (
                    <h2 className="flex items-center font-bold justify-center h-64 text-4xl text-dark-purple">
                      No events found
                    </h2>
                  )}
                </div>
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
