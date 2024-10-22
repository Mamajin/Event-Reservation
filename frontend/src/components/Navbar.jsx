import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from '../constants';
import { StarIcon } from '@heroicons/react/24/solid';

function Navbar() {
  const navigate = useNavigate();

  const onLogout = () => {
    localStorage.clear();
    navigate('/login');
  };
  const handleHome = () => {
    navigate('')
  }
  const handleLogin = () => {
    navigate('/login');
  };
  const handleCreateEvent = () => {
    navigate('/create-event');
  }

  const handleRegister = () => {
    navigate('/register');
  };

  const isLoggedIn = !!localStorage.getItem(ACCESS_TOKEN);

  return (
    <div className="navbar bg-dark-purple">
      <StarIcon className="bg-amber-300 text-xl h-8 w-9 text-dark-purple rounded cursor-pointer mr-2" />
      <div className="navbar-start">
        <a className="btn btn-ghost text-xl p-0" onClick={handleHome}>EventEase </a>
      </div>
      <div className="navbar-end">
        {isLoggedIn ? (
          <>
          <button className="btn ml-2 bg-amber-300 text-dark-purple" onClick={handleCreateEvent}>
            Create Event
          </button>
          <button className="btn ml-2 bg-amber-300 text-dark-purple " onClick={onLogout}>
            Logout
          </button>
          </>
        ) : (
          <>
            <button className="btn ml-2 bg-amber-300 text-dark-purple" onClick={handleLogin}>
              Login
            </button>
            <button className="btn ml-2 bg-amber-300 text-dark-purple" onClick={handleRegister}>
              Sign Up
            </button>
          </>
        )}
      </div>
    </div>
  );
}
export default Navbar