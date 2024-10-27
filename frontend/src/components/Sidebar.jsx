import { Link } from 'react-router-dom';
import { useState } from 'react';
import { ArrowLeftCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/solid';

function Sidebar() {
    const [open, setOpen] = useState(true);
    const Menus = [
        { title: "Discover", path: "/discover" },
        { title: "Applied Event", path: "/applied-events" },
        { title: "Accepted Event", path: "/accepted-events" },
        { title: "Invitation", path: "/invitation" },
        { title: "Become Organizer", path: "/become-organizer" },
    ];
    
    return (
        <div className="flex">
            <div className={`bg-dark-purple h-screen p-5 pt-20 fixed 
                ${open ? "w-72" : "w-20"} duration-300`}
            >
                <ArrowLeftCircleIcon 
                    className={`bg-white text-dark-purple w-9 h-9
                        rounded-full absolute -right-5 top-40 border-dark-purple cursor-pointer 
                        ${!open && "rotate-180"}`} 
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
                        <li key={index} className="text-gray-300 text-sm flex
                            items-center gap-x-4 cursor-pointer p-6" >
                            <Link to={menu.path} className="flex items-center w-full">
                                <span className={`text-base font-medium flex-1 ${!open && "hidden"}`}>{menu.title}</span>
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
            <div className={`p-7 transition-all duration-300 w-full ${open ? "ml-72" : "ml-20"}`}>
            </div>
        </div>
    );
}

export default Sidebar;