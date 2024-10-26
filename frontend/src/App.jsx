import React from 'react';
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
import AcceptedEvents from './pages/AcceptedEvents';
import ApplyOrganizer from './pages/ApplyOrganizer';
import EventDetailPage from './pages/EventDetailPage';

function App() {
  const handleLogout = () => {
    localStorage.clear();
  };

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Navbar />  
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/become-organizer" element={<ApplyOrganizer />} />
          <Route path="/events/:eventId" element={<EventDetailPage />} />
          <Route path="/logout" element={<Navigate to="/" onEnter={handleLogout} />} />
          
          {/* Protected Routes */}
          <Route path="/account-info" element={<ProtectedRoute><AccountInfo /></ProtectedRoute>} />
          <Route path="/applied-events" element={<ProtectedRoute><AppliedEvents /></ProtectedRoute>} />
          <Route path="/accepted-events" element={<ProtectedRoute><AcceptedEvents /></ProtectedRoute>} />
          <Route path="/create-event" element={<ProtectedRoute><CreateEvent /></ProtectedRoute>} />

          {/* Fallback Route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
