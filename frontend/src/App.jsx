import React, { useEffect } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { scheduleTokenRefresh, getAccessToken } from './utils/tokenManager';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Login from './pages/LoginPage';
import Register from './pages/RegisterPage';
import Home from './pages/HomePage';
import NotFound from './pages/NotFound';
import CreateEvent from './pages/CreateEventPage';
import AccountInfo from './pages/AccountInfo';
import AppliedEvents from './pages/AppliedEvents';
import ApplyOrganizer from './pages/ApplyOrganizerPage';
import EventDetail from './pages/EventDetailPage';
import Discover from './pages/DiscoverPage';
import MyEvents from './pages/MyEvents';
import OrganizerInfo from './pages/OrganizerInfo';
import Bookmark from './pages/BookMark';
import Logout from './pages/LogoutPage';
import EditEvent from './pages/EditEventPage';
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
import VirtualTicket from './pages/VirtualTicket';
import MyTickets from './pages/MyTickets';
import TicketDetail from './pages/TicketDetail';

function App() {
  useEffect(() => {
    const token = getAccessToken();
    
    if (token) {
      scheduleTokenRefresh();
    }
  }, []);

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
          <Route path="/events/:eventId" element={<EventDetail />} />
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
          <Route path="/my-tickets" element={<ProtectedRoute><MyTickets /></ProtectedRoute>} />
          <Route path="/virtual-ticket/:ticketId" element={<ProtectedRoute><VirtualTicket /></ProtectedRoute>} />
          <Route path="/ticket/:ticketId" element={<ProtectedRoute><TicketDetail /></ProtectedRoute>} />
          <Route path="/events/:eventId/edit" element={<ProtectedRoute><EditEvent /></ProtectedRoute>} />

          {/* Fallback Route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
    </GoogleOAuthProvider>
  );
}

export default App;
