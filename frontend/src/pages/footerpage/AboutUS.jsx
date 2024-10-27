import React from 'react';
import PageLayout from '../../components/PageLayout';

function AboutUs() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">About Us</h1>
        <p>
          EventEase is a university-led project developed by a dedicated team of students at Kasetsart University. Our mission is to create an intuitive and reliable event reservation platform for the community, leveraging the latest in technology to streamline event planning and participation.
        </p>
        <h2 className="text-2xl font-bold mt-4">Our Vision</h2>
        <p>
          To build an accessible and efficient event management system that connects organizers with participants seamlessly, fostering a stronger, engaged community.
        </p>
        <h2 className="text-2xl font-bold mt-4">Our Team</h2>
        <p>
          Our diverse team includes developers, designers, and project managers, all working together to deliver the best possible experience for users.
        </p>
      </div>
    </PageLayout>
  );
}

export default AboutUs;
