import { useState } from 'react';
import { ArrowLeftCircleIcon, MagnifyingGlassIcon} from '@heroicons/react/24/solid';

function Sidebar() {
    const [open,setOpen] = useState(true);
    const Menus = [
        {title: "Discover"},
        {title: "Apply Event"},
        {title: "Accepted Event"},
        {title: "Invitation"},
        {title: "Become Holder"},
        {title: "Account Info"},
    ];
    return (
        <div className="flex bg-white">
            <div className={`bg-dark-purple h-screen p-5 pt-8 
                ${open ? "w-72": "w-20"} duration-300 relative`}
            >
            <ArrowLeftCircleIcon className={`bg-white text-dark-purple w-9 h-9
                rounded-full absolute -right-5 top-9 border-dark-purple cursor-pointer 
                ${!open && "rotate-180"}`} onClick={()=> setOpen (!open)} 
            />
            <div className={`input input-bordered bg-light-white rounded-md flex items-center gap-2 ${!open ? "px-2.5 w-10 h-10" : "px-4"} py-2`}>
                <input 
                    type="search" 
                    className={`grow border-none bg-transparent w-full focus:outline-none ${!open && "hidden"}`}
                    placeholder="Search" 
                />
                <MagnifyingGlassIcon className={`text-white text-lg w-5 h-5 cursor-pointer ${open && "mr-2"}`} />
            </div>
            <ul className="pt-2">
                {Menus.map((menu, index)=>(
                    <>
                        <li key={index} className="text-gray-300 text-sm flex
                        items-center gap-x-4 cursor-pointer p-6" >
                            <span className={`text-base font-medium flex1 ${!open && "hidden"}`}>{menu.title}</span>
                        </li>
                    </>
                ))}

            </ul>
            </div>
            <div className="p-7">
                <h1 className="text-2xl font-semibold"></h1>
            </div>
        </div>

    )
}

export default Sidebar