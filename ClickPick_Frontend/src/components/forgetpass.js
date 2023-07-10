import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './forgetPass.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function ForgetPassword() {
  const [email, setEmail] = useState('');

  useEffect(() => {
    document.body.style.background =
      'linear-gradient(to right, rgba(198, 216, 236, 255) 49.1%, #1f3258 49.1%)';
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
    event.preventDefault(); // Prevent the default form submission behavior

    try {
      // Send a POST request to the API endpoint
      const response = await axios.post('http://127.0.0.1:8000/api/auth/sendOTP/', { email });
      if (response.status === 200) {
        alert(`Password reset instructions sent to ${email}`);
        // Navigate to OTP page upon successful request
        window.location.href = '/otp';
      } else {
        if (response.status === 404) {
          alert(`Email not found`);
        } else {
          // Handle other error responses if needed
          throw new Error(`Error: Email not found`);
        }
      }
    } catch (error) {
      // Handle the request error
      alert(`Email not found`);
    }
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  return (
    <div className="input-container2">
      <div>
        <img
          src="./images/logo3.png"
          alt="Logo"
          className="logos"
          onClick={handleLogoClick}
        />
        <form onSubmit={handleSubmit}>
          <h2 className="hhh">Forgot your password?</h2>
          <p className="hhhhh">Enter your email and we will <br />send you an OTP to reset your password</p>
          <input
            type="email"
            id="email2"
            name="email"
            required
            value={email}
            onChange={handleEmailChange}
            placeholder="Enter your email"
          />
          <br />
          <button id="forget-button" type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default ForgetPassword;
