import React from 'react';
import PageLayout from '../../components/PageLayout';

function Contact() {
  return (
    <PageLayout>
      <div className="p-4 text-black">
        <h1 className="text-3xl font-bold mb-4">Contact Us</h1>
        <p>Get in touch with our team for any inquiries or support.</p>
        
        <h2 className="text-2xl font-bold mt-4">Team Contacts</h2>
        <div className="mt-4 space-y-3">
          <div>
            <h3 className="text-xl font-semibold">John Smith</h3>
            <p>Email: <a href="mailto:john.smith@university.edu" className="text-blue-500">john.smith@university.edu</a></p>
            <p>Phone: (123) 456-7890</p>
            <p>Role: Project Manager</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Alice Johnson</h3>
            <p>Email: <a href="mailto:alice.johnson@university.edu" className="text-blue-500">alice.johnson@university.edu</a></p>
            <p>Phone: (123) 555-7891</p>
            <p>Role: Lead Developer</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Michael Brown</h3>
            <p>Email: <a href="mailto:michael.brown@university.edu" className="text-blue-500">michael.brown@university.edu</a></p>
            <p>Phone: (123) 555-7892</p>
            <p>Role: UX/UI Designer</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Emma White</h3>
            <p>Email: <a href="mailto:emma.white@university.edu" className="text-blue-500">emma.white@university.edu</a></p>
            <p>Phone: (123) 555-7893</p>
            <p>Role: Marketing Specialist</p>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default Contact;
