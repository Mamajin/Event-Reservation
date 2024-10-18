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


function App() {
  const handleLogout = () => {
    localStorage.clear();
  };

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/accountinfo" element={<AccountInfo />}/>
          <Route path="/appliedevents" element={<AppliedEvents />}/>
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Navigate to="/" onEnter={handleLogout} />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/create-event" 
            element={
              <ProtectedRoute>
                  <AccountInfo />
                  <AppliedEvents/>
                  <CreateEvent />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>

      </div>
    </BrowserRouter>
  );
}

export default App;