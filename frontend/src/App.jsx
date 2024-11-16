import React from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import NotFound from './pages/NotFound';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import CreateEvent from './pages/CreateEvent';
import AccountInfo from './pages/AccountInfo';
import AppliedEvents from './pages/AppliedEvents';
import ApplyOrganizer from './pages/ApplyOrganizer';
import EventDetailPage from './pages/EventDetailPage';
import Discover from './pages/Discover';
import TermsOfUse from './pages/footerpage/TermsOfUse';
import PrivacyInfo from './pages/footerpage/PrivacyInfo';
import BiscuitInfo from './pages/footerpage/BiscuitInfo';
import AboutUs from './pages/footerpage/AboutUs';
import Contact from './pages/footerpage/Contact';
import Jobs from './pages/footerpage/Jobs';
import PressKit from './pages/footerpage/PressKit';
import Advertisement from './pages/footerpage/Advertisement';
import Branding from './pages/footerpage/Branding';
import Design from './pages/footerpage/Design';
import Marketing from './pages/footerpage/Marketing';
import MyEvents from './pages/MyEvents';
import OrganizerInfo from './pages/OrganizerInfo';
import Bookmark from './pages/BookMark';
import Logout from './pages/Logout';
import EditEventPage from './pages/EditEvent';

function App() {

  return (
    <GoogleOAuthProvider clientId="987028649849-8uhmhr5qrkg494ren8um9prtdsavd6uv.apps.googleusercontent.com">
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Navbar />  
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/discover" element={<Discover />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/become-organizer" element={<ApplyOrganizer />} />
          <Route path="/events/:eventId" element={<EventDetailPage />} />
          <Route path="/logout" element={<Logout />} />

          {/* Footer Page */}
          <Route path="/legal/terms-of-use" element={<TermsOfUse />} />
          <Route path="/legal/privacy-policy" element={<PrivacyInfo />} />
          <Route path="/legal/cookie-policy" element={<BiscuitInfo />} />

          <Route path="/team/about-us" element={<AboutUs />} />
          <Route path="/team/contact" element={<Contact />} />
          <Route path="/team/jobs" element={<Jobs />} />
          <Route path="/team/press-kit" element={<PressKit />} />

          <Route path="/services/branding" element={<Branding />} />
          <Route path="/services/design" element={<Design />} />
          <Route path="/services/marketing" element={<Marketing />} />
          <Route path="/services/advertisement" element={<Advertisement />} />
          
          {/* Protected Routes */}
          <Route path="/account-info" element={<ProtectedRoute><AccountInfo /></ProtectedRoute>} />
          <Route path="/organizer-info" element={<ProtectedRoute><OrganizerInfo /></ProtectedRoute>} />
          <Route path="/applied-events" element={<ProtectedRoute><AppliedEvents /></ProtectedRoute>} />
          <Route path="/create-event" element={<ProtectedRoute><CreateEvent /></ProtectedRoute>} />
          <Route path="/my-events" element={<ProtectedRoute><MyEvents /></ProtectedRoute>} />
          <Route path="/bookmarks" element={<ProtectedRoute><Bookmark /></ProtectedRoute>} />
          <Route path="/events/:eventId/edit" element={<ProtectedRoute><EditEventPage /></ProtectedRoute>} />

          {/* Fallback Route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
    </GoogleOAuthProvider>
  );
}

export default App;
