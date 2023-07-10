import React, { useState, useEffect } from 'react';
import Navbar_not_Signin from './Navbar_not_Signin.js';
import './fav.css';
import { Link } from 'react-router-dom';
import { FaStar } from 'react-icons/fa';
import Navbar from './Navbar.js';
import axios from 'axios';
import { css } from '@emotion/react';
import { ClipLoader } from 'react-spinners';
import SliderComponent from './SliderComponent';

const override = css`
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
`;

function Fav() {
  const [numProducts, setNumProducts] = useState(21);
  const [productsData, setProductsData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const isLoggedIn = localStorage.getItem('accessToken') && localStorage.getItem('refreshToken');
  useEffect(() => {
    document.body.style.backgroundColor = '#FDFDFD';
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setIsLoading(true); // Set loading state to true
      const response = await axios.get('http://127.0.0.1:8000/api/auth/favMatchingProducts/?page=1', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      });
      const { data } = response;
      const products = data.results.products;
      setProductsData(products);
      setIsLoading(false); // Set loading state to false
    } catch (error) {
      console.log(error);
      setIsLoading(false); // Set loading state to false in case of an error
    }
  };

  const handleFavoriteClick = async (event, productID) => {
    event.preventDefault();
    event.target.classList.toggle('clicked');

    if (isLoggedIn) {
      try {
        const accessToken = localStorage.getItem('accessToken');
        const headers = {
          Authorization: `Bearer ${accessToken}`
        };

        await axios.post(`http://127.0.0.1:8000/api/auth/favoriteList/`, { product_id: productID }, { headers });

        // Remove the product from the list
        const updatedProducts = productsData.filter((product) => product.ProductID !== productID);
        setProductsData(updatedProducts);
      } catch (error) {
        console.error('Error Deleting favorite:', error);
      }
    }
  };

  const handleViewMoreClick = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/auth/favMatchingProducts/?page=${Math.ceil((numProducts + 1) / 21)}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      });
      const { data } = response;
      const products = data.results.products;
      setProductsData([...productsData, ...products]);
      setNumProducts(numProducts + 21);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="product-search-result1">
      {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
      <div className="product-list1">
      {isLoading ? (
        <div className="loading" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', marginLeft: '45vw' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <ClipLoader css={override} size={50} color={'#000000'} loading={isLoading} />
          </div>
          </div>
        ) : (
          productsData.map((product) => (
            <div key={product.ProductID} className="product1">
              <Link key={product.ProductID} to={`/product`} className="product-link2">
                <img src={product.ProductImage} alt={product.ProductTitle} />
                <div className="product-details1">
                  <h3>{product.ProductTitle.length > 35 ? product.ProductTitle.substr(0, 25) + '...' : product.ProductTitle}</h3>
                </div>
              </Link>
              <div className="product-actions">
                <p className="price1">EGP {product.ProductPrice}</p>
                {product.ProductOldPrice && <p className="before1">EGP {product.ProductOldPrice}</p>}
                <p1>{product.ProductRatings} ({product.ProductRatingCount})</p1>
                <div className='ProductRatings1'><FaStar className='star-icon' /></div>
                <button className="favorite-button1" onClick={(event) => handleFavoriteClick(event, product.ProductID)}></button>
              </div>
            </div>
          ))
        )}
      </div>
      {numProducts < productsData.length && (
        <button className="view1" onClick={handleViewMoreClick}>View More</button>
      )}
    </div>
  );
  
}

export default Fav;
