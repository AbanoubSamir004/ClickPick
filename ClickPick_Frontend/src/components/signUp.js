import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './signUp.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const API_BASE_URL = 'http://127.0.0.1:8000/api/auth';

function SignUpPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [full_name, setFullName] = useState('');
  const [birth_date, setBirthday] = useState('');
  const [address, setAddress] = useState('');

  useEffect(() => {
    document.body.style.background =
      'linear-gradient(to right, rgba(198, 216, 236, 255) 48.07%, #1f3258 48.07%)';
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

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Perform form validation
    if (password !== confirmPassword) {
      alert('Passwords do not match');
    } else {
      try {
        const response = await axios.post(`${API_BASE_URL}/register/`, {
          email,
          password,
          full_name,
          birth_date,
          address,
        });
        console.log('Signup successful:', response.data);
        // Navigate to sign-in page upon successful sign-up
        window.location.href = '/signIn';
      } catch (error) {
        console.error('Signup failed:', error);
        if (error.response && error.response.status === 500) {
          alert('This email already exists. Please choose a different email.');
        }
      }
    }
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
  };

  const handleFullNameChange = (event) => {
    setFullName(event.target.value);
  };

  const handleBirthdayChange = (event) => {
    setBirthday(event.target.value);
  };

  const handleAddressChange = (event) => {
    setAddress(event.target.value);
  };

  return (
    <div className="input-container">
      <div>
        <img
          src="./images/logo3.png"
          alt="Logo"
          className="logos"
          onClick={handleLogoClick}
        />
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            id="FullName"
            name="FullName"
            required
            placeholder="Enter Your FullName"
            value={full_name}
            onChange={handleFullNameChange}
          />
          <br />
          <input
            type="email"
            id="email"
            name="Email"
            required
            placeholder="Enter Your Email"
            value={email}
            onChange={handleEmailChange}
          />
          <br />
          <input
            type="password"
            id="password"
            name="Password"
            required
            placeholder="Enter Your Password"
            value={password}
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
          {password !== confirmPassword && (
            <script>{`alert('Passwords do not match');`}</script>
          )}
          <br />
          <input
            type="date"
            id="birthday"
            name="Birthday"
            required
            placeholder="Enter Your Birth Date"
            value={birth_date}
            onChange={handleBirthdayChange}
          />
          <br />
          <input
            type="text"
            id="address"
            name="Address"
            required
            placeholder="Enter Your Address"
            value={address}
            onChange={handleAddressChange}
          />
          <br />
          <button id="signup-btn" type="submit">
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
}

export default SignUpPage;
