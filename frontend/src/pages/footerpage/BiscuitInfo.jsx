import React from 'react';
import PageLayout from '../../components/PageLayout';

function BiscuitInfo() {
  return (
    <PageLayout>
    <div className="p-4 text-black">
      <h1 className="text-3xl font-bold mb-4">Cookie Policy</h1>
      <p>Effective Date: 26th October 2024</p>
      <p>
        This Cookie Policy explains how EventEase uses cookies and similar technologies to recognize you when you visit our website. It explains what these technologies are, why we use them, and your rights to control our use of them.
      </p>
      <h2 className="text-2xl font-bold mt-4">1. What Are Cookies?</h2>
      <p>
        Cookies are small text files that are used to store small pieces of information. They are stored on your device when the website is loaded on your browser.
      </p>
      <h2 className="text-2xl font-bold mt-4">2. How We Use Cookies</h2>
      <p>
        We use cookies to enhance your experience on our website by remembering your preferences, improving our services, and analyzing how our website is used.
      </p>
      <h2 className="text-2xl font-bold mt-4">3. Types of Cookies We Use</h2>
      <p>
        <strong>Essential Cookies:</strong> These cookies are necessary for the website to function and cannot be switched off in our systems.<br />
        <strong>Performance Cookies:</strong> These cookies allow us to count visits and traffic sources so we can measure and improve our performance.<br />
        <strong>Functional Cookies:</strong> These cookies enable the website to provide enhanced functionality and personalization.
      </p>
      <h2 className="text-2xl font-bold mt-4">4. Your Choices</h2>
      <p>
        You have the right to accept or reject cookies. Most web browsers automatically accept cookies, but you can modify your browser settings to decline cookies if you prefer.
      </p>
      <h2 className="text-2xl font-bold mt-4">5. Changes to This Policy</h2>
      <p>
        We may update this Cookie Policy from time to time. Any changes will be posted on this page, and we encourage you to review this policy periodically.
      </p>
      <h2 className="text-2xl font-bold mt-4">6. Contact Us</h2>
      <p>
        If you have any questions about our use of cookies or other technologies, please contact us at Kasetsart University.
      </p>
    </div>
    </PageLayout>
  );
}

export default BiscuitInfo;
