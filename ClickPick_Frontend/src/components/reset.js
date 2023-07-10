import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './reset.css';
import { useLocation } from 'react-router-dom';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function Reset() {
  const [new_password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const location = useLocation();

  useEffect(() => {
    document.body.style.background =
      'linear-gradient(to right, rgba(198, 216, 236, 255) 48.075%, #1f3258 48.075%)';
    document.body.style.position = 'relative';
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.display = 'flex';
    document.body.style.justifyContent = 'center';
    document.body.style.alignItems = 'center';

    return () => {
      // Cleanup: Reset body styles when component unmounts
      document.body.style.background = '';
      document.body.style.position = '';
      document.body.style.margin = '';
      document.body.style.padding = '';
      document.body.style.display = '';
      document.body.style.justifyContent = '';
      document.body.style.alignItems = '';
    };
  }, []);

  const handleLogoClick = () => {
    // Navigate to #home anchor
    window.location.href = '/';
  };

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    if (new_password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    const user_id = new URLSearchParams(location.search).get('user_id');

    if (!user_id) {
      alert('Invalid URL. Please try again.');
      return;
    }

    // Handle form submission logic here
    // You can use the `user_id` for further processing
    // For example: Send a POST request to update the user's password
    axios
      .post('http://127.0.0.1:8000/api/auth/resetPassword/', { user_id, new_password })
      .then(response => {
        // Handle success
        console.log(response.data);
        if (response.data.detail === 'Password Changes Successfully.') {
          window.location.href = '/signIn';
        }
      })
      .catch(error => {
        // Handle error
        console.error(error);
      });
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
    setPasswordError('');
  };

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
    setPasswordError('');
  };

  return (
    <div className="input-container4">
      <div>
        <img
          src="./images/logo3.png"
          alt="Logo"
          className="logos"
          onClick={handleLogoClick}
        />
        <form onSubmit={handleSubmit}>
          <h2 className="hhh">Reset Password</h2>
          <p className="text3">Please enter your new password</p>
          <input
            type="password"
            id="password"
            name="password"
            required
            placeholder="Enter Your Password"
            value={new_password}
            onChange={handlePasswordChange}
          />
          <br />
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            required
            placeholder="Confirm Your Password"
            value={confirmPassword}
            onChange={handleConfirmPasswordChange}
          />
          <br />
          <button id="forget-button" type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default Reset;
