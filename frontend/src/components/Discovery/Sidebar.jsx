import React, { useState } from 'react';
import { LuChevronLeft, LuChevronRight, LuCalendarDays } from "react-icons/lu";
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ events = [], selectedDate, onSelectDate }) => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const navigate = useNavigate();

  return (
    <div className="w-80 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold text-gray-900">
        Sidebar Component
      </h2>
    </div>
  );
};

export default Sidebar;