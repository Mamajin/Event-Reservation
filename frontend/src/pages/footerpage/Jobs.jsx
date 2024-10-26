import React from 'react';
import PageLayout from '../../components/PageLayout';

function Jobs() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Jobs</h1>
        <p>
          Interested in joining our team? EventEase is always looking for passionate individuals who want to make an impact. Check back here for updates on open positions.
        </p>
        <h2 className="text-2xl font-bold mt-4">Open Positions</h2>
        <p>
          Currently, we are seeking enthusiastic team members in the following areas:
        </p>
        <ul className="list-disc list-inside mt-2">
          <li>Frontend Developer (React)</li>
          <li>Backend Developer (Django Ninja)</li>
          <li>UX/UI Designer</li>
          <li>Marketing and Outreach Specialist</li>
        </ul>
        <p className="mt-4">
          Please reach out to us at <a href="mailto:careers@eventease.com" className="text-blue-500">careers@eventease.com</a> with your resume and a brief cover letter if you are interested.
        </p>
      </div>
    </PageLayout>
  );
}

export default Jobs;
