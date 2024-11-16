import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ACCESS_TOKEN, USER_STATUS, USER_NAME, PROFILE_PICTURE } from '../constants';
import { StarIcon } from '@heroicons/react/24/solid';

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate('/logout');
  };

  const isLoggedIn = localStorage.getItem(ACCESS_TOKEN) !== null;
  const isOrganizer = localStorage.getItem(USER_STATUS) === "Organizer";
  const username = localStorage.getItem(USER_NAME);
  const profilePicture = localStorage.getItem(PROFILE_PICTURE);

  return (
    <nav className="navbar bg-dark-purple fixed top-0 left-0 right-0 z-50">
      <StarIcon className="bg-amber-300 text-xl h-8 w-9 text-dark-purple rounded cursor-pointer mr-2" />
      <div className="navbar-start">
        <Link to="/" className="btn btn-ghost text-white text-xl p-0">
          EventEase
        </Link>
      </div>
      <div className="navbar-end">
        {isLoggedIn ? (
          <>
            {isOrganizer && (
              <Link to="/create-event" className="btn ml-2 bg-amber-300 text-dark-purple">
                Create Event
              </Link>
            )}
            <div className="avatar placeholder pl-4 pr-3 dropdown dropdown-end">
              <div
                tabIndex={0}
                className="bg-gradient-to-r from-slate-300 to-amber-500 text-neutral-content w-9 h-9 flex items-center justify-center rounded-full cursor-pointer"
              >
                {profilePicture ? (
                  <img src={profilePicture} alt="Profile" className="rounded-full w-9 h-9" />
                ) : (
                  <span className="text-md text-dark-purple">
                    {username ? username.charAt(0) : "?"}
                  </span>
                )}
              </div>
              <ul
                tabIndex={0}
                className="menu dropdown-content bg-gray-100 rounded-box z-[1] mt-4 w-36 p-2 shadow"
              >
                <li>
                  <Link to="/account-info" className="justify-between text-dark-purple">
                    Account
                  </Link>
                </li>
                <li>
                  <button className="w-full text-left text-dark-purple" onClick={handleLogout}>
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
                <Link to="/login" className="w-full text-left text-dark-purple">
                  Login
                </Link>
              </li>
              <li>
                <Link to="/register" className="w-full text-left text-dark-purple">
                  Sign Up
                </Link>
              </li>
            </ul>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;