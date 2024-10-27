import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ACCESS_TOKEN, USER_STATUS, USER_NAME } from '../constants';
import { StarIcon } from '@heroicons/react/24/solid';

function Navbar() {
  const navigate = useNavigate();

  const onLogout = () => {
    localStorage.clear();
    navigate('/login');
  };
  const handleCreateEvent = () => {
    navigate('/create-event');
  };
  const handleLogin = () => {
    navigate('/login');
  };
  const handleRegister = () => {
    navigate('/register');
  };

  const isLoggedIn = localStorage.getItem(ACCESS_TOKEN) !== null;
  const isOrganizer = localStorage.getItem(USER_STATUS) === "Organizer";
  const username = localStorage.getItem(USER_NAME);

  return (
    <nav className="navbar bg-dark-purple fixed top-0 left-0 right-0 z-50">
      <StarIcon className="bg-amber-300 text-xl h-8 w-9 text-dark-purple rounded cursor-pointer mr-2" />
      <div className="navbar-start">
        <span className="btn btn-ghost text-white text-xl p-0 cursor-pointer">
          <Link to="/">EventEase</Link>
        </span>
      </div>
      <div className="navbar-end">
        {isLoggedIn ? (
          <>
            {isOrganizer && (
              <button className="btn ml-2 bg-amber-300 text-dark-purple" onClick={handleCreateEvent} aria-label="Create Event">
                Create Event
              </button>
            )}
            <div className="avatar placeholder pl-4 pr-3 dropdown dropdown-end">
              <div
                tabIndex={0}
                className="bg-gradient-to-r from-slate-300 to-amber-500 text-neutral-content w-9 h-9 flex items-center justify-center rounded-full cursor-pointer"
              >
                <span className="text-md text-dark-purple">
                  {username.charAt(0)}
                </span>
              </div>
              <ul
                tabIndex={0}
                className="menu dropdown-content bg-gray-100 rounded-box z-[1] mt-4 w-36 p-2 shadow"
              >
                <li>
                  <a className="justify-between text-dark-purple">
                  <Link to="/account-info">Account</Link>
                  </a>
                </li>
                <li>
                  <button className="w-full text-left text-dark-purple" onClick={onLogout}>
                    Logout
                  </button>
                </li>
              </ul>
            </div>
          </>
        ) : (
          <div className="avatar placeholder pl-4 pr-3 dropdown dropdown-end">
            <div
              tabIndex={0}
              className="bg-gradient-to-r from-slate-300 to-amber-500 text-neutral-content w-9 h-9 flex items-center justify-center rounded-full cursor-pointer"
            >
              <span className="text-md text-dark-purple">?</span>
            </div>
            <ul
              tabIndex={0}
              className="menu dropdown-content bg-gray-100 rounded-box z-[1] mt-4 w-36 p-2 shadow"
            >
              <li>
                <button className="w-full text-left text-dark-purple" onClick={handleLogin}>
                  Login
                </button>
              </li>
              <li>
                <button className="w-full text-left text-dark-purple" onClick={handleRegister}>
                  Sign Up
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;