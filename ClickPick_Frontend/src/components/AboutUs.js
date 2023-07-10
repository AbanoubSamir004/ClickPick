import React from 'react';
import { Link } from 'react-router-dom';
import Navbar_not_Signin from './Navbar_not_Signin.js';
import Navbar from './Navbar.js';
import './AboutUs.css';

class AboutUs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchValue: '',
      isLoggedIn: false,
    };
  }

  componentDidMount() {
    document.body.classList.add('fixed-background');
    this.checkLoginStatus();
  }

  componentWillUnmount() {
    document.body.classList.remove('fixed-background');
    document.body.style.backgroundImage = '';
    document.body.style.backgroundSize = '';
    document.body.style.backgroundPosition = '';
    document.body.style.backgroundRepeat = '';
    document.body.style.backgroundAttachment = '';
  }

  checkLoginStatus = () => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    const isLoggedIn = accessToken && refreshToken;
    this.setState({ isLoggedIn });
  };

  render() {
    const { isLoggedIn } = this.state;

    return (
      <div>
        <div className="header-container">
          {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
        </div>

        <div className="aboutus-container">
          <h1>About Us</h1>
          <p>
            Welcome to our website! We are a team of dedicated student AI enthusiasts who have come together to create a platform that revolutionizes the online shopping experience. Our mission is to make decision-making in online shopping more flexible and easy for users like you.
          </p>
          <p>
            By aggregating products from different marketplaces and utilizing AI technology, we ensure that you have access to a comprehensive selection of products. We provide detailed feature comparisons, price analysis, and sentiment analysis on product and seller reviews, allowing you to make informed decisions effectively.
          </p>
          <p>
            We are passionate about enhancing your online shopping experience and helping you make smarter choices. With our user-friendly platform, navigating the online marketplace and finding the perfect product has never been easier.
          </p>
          <p>
            Thank you for choosing our website. We look forward to assisting you in making confident and informed purchasing decisions.
          </p>
        </div>
      </div>
    );
  }
}

export default AboutUs;
