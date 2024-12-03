import React, { useState } from 'react';
import api from '../api'; // Your Axios instance or API configuration

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await api.post('/users/forgot-password', { email });
      setMessage('Password reset link sent! Please check your email.');
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <div className="card w-full max-w-md bg-base-100 shadow-xl relative">
        {isLoading && (
          <div className="absolute inset-0 bg-base-100/50 backdrop-blur-sm flex items-center justify-center z-50 rounded-2xl">
            <span className="loading loading-spinner loading-lg text-primary"></span>
          </div>
        )}
        <div className="card-body bg-white">
          {/* Header Section */}
          <div className="flex flex-col items-center gap-2 mb-4">
            <h2 className="card-title text-2xl text-dark-purple font-bold">Forgot Password</h2>
            <p className="text-base-content/90 text-center">
              Enter your email to receive a password reset link.
            </p>
          </div>
          {/* Alert Messages */}
          {message && (
            <div className="alert alert-success">
              <span>{message}</span>
            </div>
          )}
          {error && (
            <div className="alert alert-error">
              <span>{error}</span>
            </div>
          )}
          {/* Forgot Password Form */}
          <form onSubmit={handleForgotPassword} className="space-y-4">
            <input
              type="email"
              placeholder="Your Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="input bg-white input-bordered w-full"
            />
            <button type="submit" className="btn bg-dark-purple text-white w-full">
              Send Reset Link
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
