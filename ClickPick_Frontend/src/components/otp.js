import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './otp.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function OTPVerification() {
  const [number, setNumber] = useState('');

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

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/checkOTP/', {
        otp: number
      });

      const { detail, user_id } = response.data;

      if (detail) {
        window.location.href = `/reset?user_id=${user_id}`;
      } else {
        alert('Invalid OTP. Please try again.');
      }
    } catch (error) {
      console.error('Error: ', error);
      alert('Invalid OTP. Please try again.');
    }
  };

  const handleOTPChange = (event) => {
    setNumber(event.target.value);
  };

  return (
    <div className="input-container3">
      <div>
        <img
          src="./images/logo3.png"
          alt="Logo"
          className="logos"
          onClick={handleLogoClick}
        />
        <form onSubmit={handleSubmit}>
          <h2 className="hhh">OTP Verification</h2>
          <p className="text2">Please Enter your OTP to reset your password</p>
          <input
            type="number"
            id="number"
            name="number"
            required
            value={number}
            onChange={handleOTPChange}
            placeholder="Enter your OTP"
          />
          <br />
          <button id="forget-button" type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default OTPVerification;
