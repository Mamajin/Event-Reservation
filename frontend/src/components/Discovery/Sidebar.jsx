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
  return (
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
  );
};

export default Sidebar;