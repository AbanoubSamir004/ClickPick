import React, { useState, useEffect } from 'react';
import './signIn.css';
// import './forgetPass.css';
// import './reset.css';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const API_BASE_URL = 'http://127.0.0.1:8000/api/auth';

function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  // Function to handle user login and token storage
  const loginUser = async (email, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/login/`, {
        email,
        password
      });
      const { access, refresh } = response.data;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      console.log('Login successful');
      // Redirect to the desired page or perform any other actions
      window.location.href = '/';
    } catch (error) {
      console.error('Login failed', error);
      alert('Email or password is incorrect. Please enter correct data.');
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    loginUser(email, password);
  };

  const handleSignUpClick = () => {
    window.location.href = '/signUp';
  };

  const handleForgotPasswordClick = () => {
    window.location.href = '/forgetPass';
  };

  useEffect(() => {
    document.body.style.background =
      'linear-gradient(to right, rgba(198, 216, 236, 255) 48.6%, #1f3258 48.6%)';
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

  return (
    <div className="input-container">
      <div>
        <img
          src={'./images/logo3.png'}
          alt="Logo"
          className="logos"
          onClick={handleLogoClick}
        />
        <h1 className="don">Sign in to your account</h1>
        <h1 className="have">
          Don't have an account?
          <button className="signup-button" onClick={handleSignUpClick}>
            Sign up
          </button>
        </h1>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            id="email5"
            name="Email"
            required
            value={email}
            onChange={handleEmailChange}
            placeholder="Enter Your Email"
          />
          <br />
          <input
            type="password"
            id="password5"
            name="Password"
            required
            value={password}
            onChange={handlePasswordChange}
            placeholder="Enter Your password"
          />
          <br />
          <button id="signin-btn" type="submit">
            Sign in
          </button>
        </form>
        <label htmlFor="forgotPassword">
          <span
            className="forgot-password"
            style={{ borderBottom: '1px solid black' }}
            onClick={handleForgotPasswordClick}
          >
            Forgot your password?
          </span>
        </label>
      </div>
    </div>
  );
}

export default SignInPage;
