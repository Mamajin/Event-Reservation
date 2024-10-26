import React from 'react';
import PageLayout from '../components/PageLayout';

function TermsOfUse() {
  return (
    <PageLayout>
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Terms of Use</h1>
        <p className="mb-4">
          Welcome to our website. By using our services, you agree to the following terms and conditions.
        </p>
        <h2 className="text-xl font-semibold mb-2">Usage Policy</h2>
        <p className="mb-4">
          [Details about usage policy, user responsibilities, etc.]
        </p>
        {/* Add more sections as necessary */}
      </div>
    </PageLayout>
  );
}

export default TermsOfUse;
