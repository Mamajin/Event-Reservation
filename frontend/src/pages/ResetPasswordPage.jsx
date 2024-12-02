import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

const ResetPassword = () => {
  const { userId, token } = useParams();
  const navigate = useNavigate();
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (userId && token) {
      console.log(userId);
      console.log(token);
      
      validateResetToken();
    }
  }, [userId, token]);

  const validateResetToken = async () => {
    try {
      setIsLoading(true);

      const response = await api.get(`/users/reset-password/${userId}/${token}`);
      if (response.data.valid) {
        setSuccess('Token is valid, you can reset your password.');
      } else {
        setError('Invalid or expired reset token.');
      }
    } catch (error) {
      setError('Error validating the token. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      setIsLoading(false);
      return;
    }

    try {
      const response = await api.post(`/users/reset-password/${userId}`, {
        user_id: userId,
        new_password: newPassword,
        confirm_password: confirmPassword
      });

      setSuccess('Password reset successfully. You can now log in.');
      navigate('/login');
    } catch (error) {
      setError(error.response?.data?.detail || 'An error occurred. Please try again.');
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
          {/* Logo Section */}
          <div className="flex flex-col items-center gap-2 mb-4">
            <div className="avatar">
              {/* Add your logo here */}
            </div>
            <h2 className="card-title text-2xl text-dark-purple font-bold">Reset Your Password</h2>
            <p className="text-base-content/90 text-center">
              Enter your new password below to reset it.
            </p>
          </div>
          {/* Alert Messages */}
          {error && (
            <div className="alert alert-error">
              <span>{error}</span>
            </div>
          )}
          {success && (
            <div className="alert alert-success">
              <span>{success}</span>
            </div>
          )}
          {/* Reset Password Form */}
          <form onSubmit={handleResetPassword} className="space-y-4">
            <input
              type="password"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              className="input bg-white input-bordered w-full"
            />
            <input
              type="password"
              placeholder="Confirm New Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="input bg-white input-bordered w-full"
            />
            <button type="submit" className="btn bg-dark-purple text-white w-full">
              Reset Password
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
