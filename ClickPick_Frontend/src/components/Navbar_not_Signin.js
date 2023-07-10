import React, { useState } from 'react';
import './Navbar_not_Signin.css';
import { Link} from 'react-router-dom';

function Navbar_not_Signin() {
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
    // Navigate to the home page
    window.location.href = '/';

  };

  const handleFavoritesClick = (event) => {
    if (!isLoggedIn()) {
      event.preventDefault();
      // Redirect the user to the SignIn page
      window.location.href = '/SignIn';

    }
  };

  const isLoggedIn = () => {
    // Check if the access token exists in the local storage
    const accessToken = localStorage.getItem('accessToken');
    
    // Add your logic to validate the access token
    // For example, you can check if the access token is not null or empty
    if (accessToken && accessToken.trim() !== '') {
      return true; // User is logged in
    } else {
      return false; // User is not logged in
    }
  };
  

  return (
    <nav className="nav2">
      <img
        src={'/images/logo3.png'}
        alt="Logo"
        className="logo"
        onClick={handleLogoClick}
      />
      <div className="search2">
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
      <ul className="navmenu">
        <li>
          <Link to="/sales">Sales</Link>
        </li>
        <li>
          <Link to="/favorites" onClick={handleFavoritesClick}>
            Favorites
          </Link>
        </li>
        <li>
          <Link to="/promotion">Promotion</Link>
        </li>
        <li>
          <Link to="/signIn">Sign In</Link>
        </li>
        <li>
          <a href="/aboutUs/">About Us</a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar_not_Signin;
