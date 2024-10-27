import React from 'react';
import PageLayout from '../../components/PageLayout';

function Marketing() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Marketing Services</h1>
        <p>
          Our marketing services are tailored to help you promote your events effectively. We offer a range of marketing solutions, including:
        </p>
        <ul className="list-disc list-inside mt-2">
          <li>Social Media Marketing</li>
          <li>Email Marketing Campaigns</li>
          <li>Content Marketing and Strategy</li>
          <li>Search Engine Optimization (SEO)</li>
        </ul>
        <p className="mt-4">
          Partner with us to reach your target audience and maximize event attendance.
        </p>
      </div>
    </PageLayout>
  );
}

export default Marketing;
