import React, { useState } from 'react';
import { LuChevronLeft, LuChevronRight, LuCalendarDays } from "react-icons/lu";
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ events = [], selectedDate, onSelectDate }) => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const navigate = useNavigate();
  const nextMonth = () => {
    setCurrentMonth(new Date(currentMonth.setMonth(currentMonth.getMonth() + 1)));
  };
  
  const previousMonth = () => {
    setCurrentMonth(new Date(currentMonth.setMonth(currentMonth.getMonth() - 1)));
  };
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
  return (
  <div>
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
        <div key={day} className="text-center text-sm font-medium text-gray-600 py-1">
          {day}
        </div>
      ))}

      {previousMonthDays.map((_, index) => (
        <div key={`prev-${index}`} className="text-center py-1" />
      ))}
    {days.map((day) => {
      const date = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);
      const dayEvents = getEventsForDate(date);
      const hasEvents = dayEvents.length > 0;
      return (
        <button
          key={day}
          className="relative text-center py-1 rounded-full hover:bg-gray-100"
        >
          {day}
          {hasEvents && (
            <span className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 rounded-full bg-indigo-600" />
          )}
        </button>
      );
    })}
    </div>
  </div>
  );
};

export default Sidebar;