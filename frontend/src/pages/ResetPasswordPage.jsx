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

  useEffect(() => {
    if (userId && token) {
      // You can validate the token here if necessary, e.g., by calling an API
      validateResetToken();
    }
  }, [userId, token]);

  const validateResetToken = async () => {
    try {
      const response = await api.get(`/users/reset-password/${userId}/${token}`);
      const data = await response.json();

      if (response.ok && data.valid) {
        setSuccess('Token is valid, you can reset your password.');
      } else {
        setError('Invalid or expired reset token.');
      }
    } catch (error) {
      setError('Error validating the token. Please try again.');
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    try {
      const response = await api.post('/users/reset-password', {
        user_id: userId,
        token,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess('Password reset successfully. You can now log in.');
        navigate('/login');  // Redirect to the login page
      } else {
        setError(data.detail || 'Failed to reset password. Please try again.');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div className="card w-96 mx-auto bg-base-100 shadow-lg">
      <div className="card-body">
        <h2 className="card-title">Reset Password</h2>
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
        <form onSubmit={handleResetPassword} className="space-y-4">
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
            className="input input-bordered w-full"
          />
          <input
            type="password"
            placeholder="Confirm New Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            className="input input-bordered w-full"
          />
          <button type="submit" className="btn btn-primary w-full">
            Reset Password
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;
