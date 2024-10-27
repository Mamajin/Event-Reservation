import React from 'react';
import PageLayout from '../../components/PageLayout';

function Advertisement() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Advertisement Services</h1>
        <p>
          We provide comprehensive advertising solutions to ensure your events gain maximum visibility. Our services include:
        </p>
        <ul className="list-disc list-inside mt-2">
          <li>Digital Advertising (Google Ads, Social Media Ads)</li>
          <li>Print Advertising (Brochures, Flyers)</li>
          <li>Event Sponsorship Opportunities</li>
          <li>Promotional Campaigns</li>
        </ul>
        <p className="mt-4">
          Reach out to us for creative advertising strategies that resonate with your audience and drive engagement.
        </p>
      </div>
    </PageLayout>
  );
}

export default Advertisement;
