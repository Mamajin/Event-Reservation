import React from 'react';
import PageLayout from '../components/PageLayout';

function BiscuitInfo() {
  return (
    <PageLayout>
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Cookie Policy</h1>
        <p className="mb-4">
          This Cookie Policy explains how we use cookies and similar technologies.
        </p>
        <h2 className="text-xl font-semibold mb-2">What Are Cookies?</h2>
        <p className="mb-4">
          [Description of cookies and their purpose]
        </p>
        {/* Add more sections as necessary */}
      </div>
    </PageLayout>
  );
}

export default BiscuitInfo;
