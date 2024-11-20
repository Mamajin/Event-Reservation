import React, { useState } from 'react';
import { LuChevronLeft, LuChevronRight, LuCalendarDays } from "react-icons/lu";
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ events = [], selectedDate, onSelectDate }) => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const navigate = useNavigate();

  const daysInMonth = new Date(
    currentMonth.getFullYear(),
    currentMonth.getMonth() + 1,
    0
  ).getDate();

  const firstDayOfMonth = new Date(
    currentMonth.getFullYear(),
    currentMonth.getMonth(),
    1
  ).getDay();

  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);
  const previousMonthDays = Array.from({ length: firstDayOfMonth }, (_, i) => i);

  const getEventsForDate = (date) => {
    return events.filter(
      (event) =>
        new Date(event.start_date_event).toDateString() === date.toDateString()
    );
  };

  const nextMonth = () => {
    setCurrentMonth(new Date(currentMonth.setMonth(currentMonth.getMonth() + 1)));
  };

  const previousMonth = () => {
    setCurrentMonth(new Date(currentMonth.setMonth(currentMonth.getMonth() - 1)));
  };

  const handleDateClick = (date) => {
    if (selectedDate?.toDateString() === date.toDateString()) {
      onSelectDate(null);
    } else {
      onSelectDate(date);
    }
  };

  return (
    <div className="w-80 bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          {currentMonth.toLocaleString('default', { month: 'long', year: 'numeric' })}
        </h2>
        <div className="flex space-x-2">
          <button
            onClick={previousMonth}
            className="p-1 hover:bg-gray-100 rounded-full"
          >
            <LuChevronLeft className="h-5 w-5 text-gray-600" />
          </button>
          <button
            onClick={nextMonth}
            className="p-1 hover:bg-gray-100 rounded-full"
          >
            <LuChevronRight className="h-5 w-5 text-gray-600" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-1 mb-4">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
          <div
            key={day}
            className="text-center text-sm font-medium text-gray-600 py-1"
          >
            {day}
          </div>
        ))}
        
        {previousMonthDays.map((_, index) => (
          <div key={`prev-${index}`} className="text-center py-1" />
        ))}
        
        {days.map((day) => {
          const date = new Date(
            currentMonth.getFullYear(),
            currentMonth.getMonth(),
            day
          );
          const dayEvents = getEventsForDate(date);
          const isSelected = selectedDate?.toDateString() === date.toDateString();
          const hasEvents = dayEvents.length > 0;

          return (
            <button
              key={day}
              onClick={() => handleDateClick(date)}
              className={`
                relative text-center py-1 rounded-full hover:bg-gray-100
                ${isSelected ? 'bg-dark-purple text-white hover:bg-indigo-700' : ''}
              `}
            >
              {day}
              {hasEvents && (
                <span className={`absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 rounded-full ${
                  isSelected ? 'bg-white' : 'bg-indigo-600'
                }`} />
              )}
            </button>
          );
        })}
      </div>

      <div className="mt-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-3">
          {selectedDate ? (
            `Events on ${selectedDate.toLocaleDateString()}`
          ) : (
            'Upcoming Events'
          )}
        </h3>
        <div className="space-y-3">
          {(selectedDate
            ? getEventsForDate(selectedDate)
            : events.slice(0, 3)
          ).map((event) => (
            <div
              key={event.id}
              className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer duration-200"
              onClick={() => navigate(`/events/${event.id}`)}
            >
              <div className="flex items-start space-x-3">
                <img
                   src={event?.event_image || "https://images.unsplash.com/photo-1513623935135-c896b59073c1?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGV2ZW50fGVufDB8fDB8fHww"}
                   alt={event.event_name}
                  className="w-12 h-12 rounded-lg object-cover"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 truncate">
                    {event.event_name}
                  </p>
                  <p className="text-sm text-gray-600">
                    {new Date(event.start_date_event).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                  <div className="flex items-center mt-1 text-xs text-gray-500">
                    <LuCalendarDays className="h-3 w-3 mr-1" />
                    <span>
                      {new Date(event.start_date_event).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;

