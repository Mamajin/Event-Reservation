import React from 'react';
import PageLayout from '../components/PageLayout';

function PrivacyInfo() {
  return (
    <PageLayout>
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
        <p className="mb-4">
          This Privacy Policy explains how we collect, use, and protect your personal information.
        </p>
        <h2 className="text-xl font-semibold mb-2">Information We Collect</h2>
        <p className="mb-4">
          [Details about what data is collected, e.g., names, emails, etc.]
        </p>
        {/* Add more sections as necessary */}
      </div>
    </PageLayout>
  );
}

export default PrivacyInfo;
