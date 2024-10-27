import React from 'react';
import PageLayout from '../../components/PageLayout';

function Branding() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Branding Services</h1>
        <p>
          At EventEase, we understand the importance of a strong brand identity. Our branding services are designed to help you establish a memorable presence in the event industry. We offer:
        </p>
        <ul className="list-disc list-inside mt-2">
          <li>Brand Strategy Development</li>
          <li>Logo and Visual Identity Design</li>
          <li>Brand Messaging and Voice</li>
          <li>Brand Guidelines and Documentation</li>
        </ul>
        <p className="mt-4">
          Contact us today to elevate your brand with our comprehensive branding solutions!
        </p>
      </div>
    </PageLayout>
  );
}

export default Branding;
