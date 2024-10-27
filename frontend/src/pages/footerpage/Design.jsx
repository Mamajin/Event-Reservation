import React from 'react';
import PageLayout from '../../components/PageLayout';

function Design() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Design Services</h1>
        <p>
          Our design team specializes in creating visually appealing and user-friendly interfaces for your event platform. We provide:
        </p>
        <ul className="list-disc list-inside mt-2">
          <li>User Interface (UI) Design</li>
          <li>User Experience (UX) Design</li>
          <li>Graphic Design for Marketing Materials</li>
          <li>Responsive Web Design</li>
        </ul>
        <p className="mt-4">
          Let us help you create designs that not only attract attention but also enhance user engagement.
        </p>
      </div>
    </PageLayout>
  );
}

export default Design;
