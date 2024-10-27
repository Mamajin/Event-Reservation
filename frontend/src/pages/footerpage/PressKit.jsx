import React from 'react';
import PageLayout from '../../components/PageLayout';

function PressKit() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Press Kit</h1>
        <p>
          Welcome to the EventEase Press Kit. Here, you can find our latest assets, logos, and information about our project.
        </p>
        <h2 className="text-2xl font-bold mt-4">Project Overview</h2>
        <p>
          EventEase is a platform designed to simplify event reservations, created by students at Kasetsart University as part of a university project.
        </p>
        <h2 className="text-2xl font-bold mt-4">Brand Assets</h2>
        <p>
          For official EventEase logos and media assets, please contact our team at <a href="mailto:media@eventease.com" className="text-blue-500">media@eventease.com</a>.
        </p>
        <p className="mt-4">
          Any media inquiries or additional information requests are welcome.
        </p>
      </div>
    </PageLayout>
  );
}

export default PressKit;
