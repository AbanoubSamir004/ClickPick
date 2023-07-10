import React, { useState } from 'react';
import './Navbar.css';
import { BrowserRouter, Route, Routes, Link, ReactDOM } from 'react-router-dom';

function Navbar() {
  const [searchValue, setSearchValue] = useState('');

  const handleSearchChange = (event) => {
    setSearchValue(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    // Navigate to the search results page
    window.location.href = `/Products/search/${searchValue}`;
  };


  const handleLogoClick = () => {
    // Navigate to #home anchor
    window.location.href = '/';
  };

  const logoutUser = () => {
    // Perform logout actions

    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    console.log('Logged out');
    window.location.href = '/';

  };

  return (
    <nav className="navv">
      <img
        src={'/images/logo3.png'}
        alt="Logo"
        className="logo1"
        onClick={handleLogoClick}
      />
      <div className="search3">
        <form onSubmit={handleSearchSubmit}>
          <input
            type="text"
            placeholder="Search..."
            style={{ width: '100%' }}
            value={searchValue}
            onChange={handleSearchChange}
          />
        </form>
      </div>
      <ul className="navbar-links">
        <li>
          <Link to="/sales">Sales</Link>
        </li>
        <li>
          <Link to="/favorites">Favorites</Link>
        </li>
        <li>
          <Link to="/promotion">Promotion</Link>
        </li>
        <li>
          <Link to="/" onClick={logoutUser}>Sign Out</Link>
        </li>
        <li>
          <a href="/aboutUs/">About Us</a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
