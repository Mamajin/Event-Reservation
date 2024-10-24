// src/components/PageLayout.js
import React from 'react';
import Sidebar from './Sidebar';
import Footer from './Footer';

function PageLayout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1">
          <div className="bg-white min-h-screen p-6">
            {children}
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
}

export default PageLayout;
