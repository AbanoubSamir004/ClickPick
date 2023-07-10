import React from 'react';
import { BrowserRouter, Route, Routes ,Link } from 'react-router-dom';
import Navbar from './components/Navbar.js';
import SignInPage from './components/signIn';
import ProductSearchResults from './components/products.js';
import Sales from './components/sales.js';
import Fav from './components/fav.js';
import Prom from './components/promotions.js';
import Home from './components/home.js';
import Product from './components/Product.js';
import Navbar_not_Signin from './components/Navbar_not_Signin.js';

function App() {
  return (
    <link rel="icon"  href="clickpick4.png" />

  //   <BrowserRouter>
  //     <div>
  //       <Navbar_not_Signin />
  //       <Routes>
  //         <Route path="/" element={<Sales />} />
  //         <Route path="/promotion" element={<Prom />} />
  //         <Route path="/favorites" element={<Fav />} />
  //         <Route path="/signin" element={<SignInPage />} />
  //         <Route path="/productsearchresults" element={<ProductSearchResults />} />
  //         <Route path='/Product/' element={<Product/>}/>
  //         <Route path="/home" element={<Home />} />
  //       </Routes>
  //     </div>
  //   </BrowserRouter>
  );
}

export default App;
