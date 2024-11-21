import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { ArrowLeftCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/solid';
import { ACCESS_TOKEN, USER_STATUS } from '../constants';

function Sidebar() {
    const [open, setOpen] = useState(() => {
        const savedState = localStorage.getItem('sidebarOpen');
        return savedState !== null ? JSON.parse(savedState) : true;
    });

    const isLoggedIn = localStorage.getItem(ACCESS_TOKEN) !== null;
    const isOrganizer = localStorage.getItem(USER_STATUS) === "Organizer";

    // Define the menu items with conditional inclusion of "My Events"
    const Menus = [
        { title: "Discover", path: "/discover" },
        { title: "Applied Events", path: "/applied-events" },
        ...(isLoggedIn && isOrganizer ? [{ title: "My Events", path: "/my-events" }] : []),  // Only show if the user is an organizer
        { title: "My Tickets", path: "/my-tickets" },
        { title: "Bookmarks", path: "/bookmarks" },
        { title: "Become Organizer", path: "/become-organizer" },
        
    ];

    useEffect(() => {
        localStorage.setItem('sidebarOpen', JSON.stringify(open));
    }, [open]);

    return (
        <div className="flex">
            <div 
                className={`bg-dark-purple h-screen p-5 pt-20 fixed ${open ? "w-72" : "w-20"} duration-500 transition-all`} 
                onMouseEnter={() => setOpen(true)}
                onMouseLeave={() => setOpen(false)}
            >
                <ArrowLeftCircleIcon 
                    className={`bg-white text-dark-purple w-9 h-9 rounded-full absolute -right-5 top-40 border-dark-purple cursor-pointer ${!open && "rotate-180"}`} 
                    onClick={() => setOpen(!open)} 
                />
                <div className={`input input-bordered bg-light-white rounded-md flex items-center gap-2 ${!open ? "px-2.5 w-10 h-10" : "px-4"} py-2 mt-4`}>
                    <input 
                        type="search" 
                        className={`grow border-none bg-transparent w-full focus:outline-none ${!open && "hidden"}`}
                        placeholder="Search" 
                    />
                    <MagnifyingGlassIcon className={`text-white text-lg w-5 h-5 cursor-pointer ${open && "mr-2"}`} />
                </div>
                <ul className="pt-6">
  {Menus.map((menu, index) => (
    <li
      key={index}
      className="text-white text-md flex items-center gap-x-4 cursor-pointer p-6"
    >
      <Link to={menu.path} className="flex items-center w-full">
        <span
          className={`text-base font-medium flex-1 ${
            !open
              ? "opacity-0 translate-x-4"
              : "opacity-100 translate-x-0 transition-all duration-1000 ease-out"
          }`}
        >
          {menu.title}
        </span>
      </Link>
    </li>
  ))}
</ul>
            </div>
            <div className={`p-7 pr-0 transition-all duration-500 w-full ${open ? "ml-72" : "ml-20"}`}>
            </div>
        </div>
    );
}

export default Sidebar;
