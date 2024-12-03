import React, { useState, useEffect } from 'react';
import { LuLoader2 } from "react-icons/lu";
import PageLayout from './PageLayout';

const Loading = () => {
  const texts = [
    'Preparing your experience',
    'Loading event details',
    'Setting up the magic',
    'Almost there',
  ];

  const [currentTextIndex, setCurrentTextIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTextIndex((prevIndex) => (prevIndex + 1) % texts.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <PageLayout>
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
        <div className="text-center space-y-6 max-w-md w-full">
          {/* Spinner */}
          <div className="flex justify-center">
            <LuLoader2 className="animate-spin text-amber-500" size={48} strokeWidth={2} />
          </div>

          {/* Title */}
          <h1 className="text-3xl font-bold text-gray-800 tracking-wide">Discover</h1>

          {/* Loading Text */}
          <div className="relative h-12 overflow-hidden">
            <p
              key={currentTextIndex}
              className="absolute inset-0 text-xl text-gray-600 opacity-0 translate-y-4 transition-all duration-500 ease-out animate-textSlide"
            >
              {texts[currentTextIndex]}
            </p>
          </div>

          {/* Progress Dots */}
          <div className="flex justify-center space-x-2">
            {texts.map((_, index) => (
              <div
                key={index}
                className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  index === currentTextIndex ? 'bg-amber-500 scale-125' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
            <div className="bg-amber-500 h-1.5 w-full animate-runningBar" />
          </div>
        </div>
      </div>
    </PageLayout>
  );
};

export default Loading;
