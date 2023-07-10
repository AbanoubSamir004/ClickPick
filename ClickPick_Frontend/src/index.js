import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Fav from './components/fav.js';
import Prom from './components/promotions.js';
import Sales from './components/sales.js';
import SignInPage from './components/signIn';
import SignUpPage from './components/signUp.js';
import ForgetPass from './components/forgetpass.js';
import OTP from './components/otp.js';
import Home from './components/home.js';
import Products from './components/products.js';
import Product from './components/Product.js';
import AboutUs from './components/AboutUs.js';
import Reset from './components/reset.js';

<link rel="icon"  href="clickpick4.png" />

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/Products/search/:query/' element={<Products />} />
      <Route path='/Products/subcategory/:subcategory' element={<Products />} />
      <Route path='/Product/:Product_id' element={<Product />} />
      <Route path='/aboutUs/' element={<AboutUs />} />
      <Route path="/promotion" element={<Prom />} />
      <Route path="/favorites" element={<Fav />} />
      <Route path="/sales" element={<Sales />} />
      <Route path="/signIn" element={<SignInPage />} />
      <Route path="/signUp" element={<SignUpPage />} />
      <Route path="/forgetPass" element={<ForgetPass />} />
      <Route path="/otp" element={<OTP />} />
      <Route path="/reset" element={<Reset />} />
      {/* <Route path="/BarChart" element={<BarChart />} />
      <Route path="/PieChart" element={<PieChart />} /> */}

    </Routes>
  </BrowserRouter>
);
