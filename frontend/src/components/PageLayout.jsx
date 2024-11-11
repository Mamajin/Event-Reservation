// src/components/PageLayout.js
import React from 'react';
import Sidebar from './Sidebar';
import Footer from './Footer';

function PageLayout({ children }) {
  return (
    <div className="flex flex-col bg-gray-50 min-h-screen">
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1">
          <div className="bg-gray-50 min-h-screen  pt-20">
            {children}
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
}

export default PageLayout;
