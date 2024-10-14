import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from '../constants';
import { StarIcon } from '@heroicons/react/24/solid';

export default function Navbar() {
  const navigate = useNavigate();

  const onLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const handleLogin = () => {
    navigate('/login');
  };

  const handleRegister = () => {
    navigate('/register');
  };

  const isLoggedIn = !!localStorage.getItem(ACCESS_TOKEN);

  return (
    <div className="navbar bg-dark-purple">
      <StarIcon className="bg-amber-300 text-xl h-8 w-9 text-dark-purple rounded cursor-pointer mr-2" />
      <div className="navbar-start">
        <a className="btn btn-ghost text-xl p-0">EventEase</a>
      </div>
      <div className="navbar-end">
        {isLoggedIn ? (
          <button className="btn" onClick={onLogout}>
            Logout
          </button>
        ) : (
          <>
            <button className="btn" onClick={handleLogin}>
              Login
            </button>
            <button className="btn ml-2" onClick={handleRegister}>
              Sign Up
            </button>
          </>
        )}
      </div>
    </div>
  );
}