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
            <h3 className="text-xl font-semibold">Phantawat Lueangsiriwattana</h3>
            <p>Email: <a href="mailto:phantawat.l@ku.th" className="text-blue-500">phantawat.l@ku.th</a></p>
            <p>Phone: (+66) 456-7890</p>
            <p>Role: Backend Developer</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Napoldej Passornratchakul</h3>
            <p>Email: <a href="mailto:napoldej.p@ku.th" className="text-blue-500">napoldej.p@ku.th</a></p>
            <p>Phone: (+66) 555-7891</p>
            <p>Role: Backend Developer</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Sunthorn Kompita</h3>
            <p>Email: <a href="mailto:sunthorn.ko@ku.th" className="text-blue-500">sunthorn.ko@ku.th</a></p>
            <p>Phone: (+66) 555-7892</p>
            <p>Role: Frontend Developer</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Phasit Ruangmak</h3>
            <p>Email: <a href="mailto:phasit.r@ku.th" className="text-blue-500">phasit.r@ku.th</a></p>
            <p>Phone: (+66) 555-7893</p>
            <p>Role: Frontend Developer</p>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default Contact;
