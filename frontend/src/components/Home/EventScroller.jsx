import React, { useRef } from 'react';
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";
import EventCard from './EventCard';

export default function EventScroller({ title, description, events }) {
    const scrollRef = useRef(null);

    const scroll = (direction) => {
        if (scrollRef.current) {
            const scrollAmount = direction === 'left' ? -400 : 400;
            scrollRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        }
    };

    return (
        <div className="relative py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">{title}</h2>
                    <p className="text-gray-600">{description}</p>
                </div>

                <div className="relative group">
                    <button
                        onClick={() => scroll('left')}
                        className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 bg-white rounded-full p-2 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <LuChevronLeft className="w-6 h-6 text-gray-600" />
                    </button>

                    <div
                        ref={scrollRef}
                        className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth pb-4 w-full"
                        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                    >
                        {events.map((event) => (
                            <div key={event.id} className="flex-none w-[350px] h-[100%]">
                                <div className="flex flex-col h-full">
                                    <EventCard event={event} />
                                </div>
                            </div>
                        ))}
                    </div>

                    <button
                        onClick={() => scroll('right')}
                        className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 bg-white rounded-full p-2 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <LuChevronRight className="w-6 h-6 text-gray-600" />
                    </button>
                </div>
            </div>
        </div>
    );
}
