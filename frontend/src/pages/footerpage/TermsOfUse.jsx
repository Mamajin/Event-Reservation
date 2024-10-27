import React from 'react';
import PageLayout from '../../components/PageLayout';

function TermsOfUse() {
  return (
    <PageLayout>
    <div className="p-4 text-black">
      <h1 className="text-3xl font-bold mb-4">Terms of Use</h1>
      <p>Effective Date: 26th October 2024</p>
      <p>
        Welcome to EventEase! By accessing or using our services, you agree to comply with and be bound by the following terms and conditions. If you do not agree with any part of these terms, you must not use our services.
      </p>
      <h2 className="text-2xl font-bold mt-4">1. Acceptance of Terms</h2>
      <p>
        By using our website and services, you confirm that you are at least 18 years old or have the consent of a parent or guardian.
      </p>
      <h2 className="text-2xl font-bold mt-4">2. User Responsibilities</h2>
      <p>
        You are responsible for maintaining the confidentiality of your account information and for all activities that occur under your account. You agree to notify us immediately of any unauthorized use of your account.
      </p>
      <h2 className="text-2xl font-bold mt-4">3. Event Reservations</h2>
      <p>
        You agree to provide accurate and complete information when making reservations. Any fraudulent or misleading information may result in the cancellation of your reservations.
      </p>
      <h2 className="text-2xl font-bold mt-4">4. Intellectual Property</h2>
      <p>
        All content, trademarks, and other intellectual property displayed on our site are the property of EventEase or our licensors. You may not reproduce, distribute, or create derivative works from any content without our prior written consent.
      </p>
      <h2 className="text-2xl font-bold mt-4">5. Limitation of Liability</h2>
      <p>
        In no event shall EventEase be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising from your use of our services.
      </p>
      <h2 className="text-2xl font-bold mt-4">6. Governing Law</h2>
      <p>
        These Terms of Use shall be governed by and construed in accordance with the laws of Thailand. Any disputes arising from these terms shall be resolved in the courts of Thailand.
      </p>
      <h2 className="text-2xl font-bold mt-4">7. Changes to Terms</h2>
      <p>
        We reserve the right to modify these Terms of Use at any time. Your continued use of our services after changes are made will constitute your acceptance of the new terms.
      </p>
    </div>
    </PageLayout>
  );
}

export default TermsOfUse;
