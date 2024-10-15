import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import NotFound from './pages/NotFound';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';

function App() {
  const handleLogout = () => {
    localStorage.clear();
  };

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen"> {/* Set up flexbox for full height */}
        <Navbar />
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <div className="flex flex-1">
                  <Sidebar />
                  <main className="flex-1">
                    <Home />
                  </main>
                </div>
                <Footer />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route 
            path="/logout" 
            element={<Navigate to="/" onEnter={handleLogout} />} 
          />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<NotFound />} />
        </Routes>

      </div>
    </BrowserRouter>
  );
}

export default App;