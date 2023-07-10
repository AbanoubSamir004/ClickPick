import React, { useState, useEffect, useRef } from 'react';
import './promotions.css';
import Navbar_not_Signin from './Navbar_not_Signin.js';
import axios from 'axios';
import { css } from '@emotion/react';
import { ClipLoader } from 'react-spinners';
import Navbar from './Navbar.js';

function Promotions() {
  const [marketplaceFilter, setMarketplaceFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [promotions, setPromotions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [page, setPage] = useState(1);
  const [showFirstSpinner, setShowFirstSpinner] = useState(true);
  const loader = useRef(null);
  const isLoggedIn = localStorage.getItem('accessToken') && localStorage.getItem('refreshToken');

  useEffect(() => {
    document.body.style.backgroundColor = '#FDFDFD';
    fetchPromotions();
    const options = {
      root: null,
      rootMargin: '20px',
      threshold: 1.0,
    };
    const observer = new IntersectionObserver(handleObserver, options);
    if (loader.current) {
      observer.observe(loader.current);
    }
  }, []);

  useEffect(() => {
    if (page > 1) {
      fetchPromotions();
    }
  }, [page]);

  async function fetchPromotions() {
    try {
      setIsLoading(true);
      const response = await axios.get(`http://127.0.0.1:8000/api/promotions/?page=${page}`);
      const data = response.data.results;
      setPromotions((prevPromotions) => [...prevPromotions, ...data]);
      setIsLoading(false);
      setIsLoadingMore(false);
      if (showFirstSpinner) {
        setShowFirstSpinner(false);
      }
    } catch (error) {
      console.error('Error fetching promotions:', error);
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  }

  const filteredProducts = promotions.filter((product) => {
    return (
      (product.Marketplace === marketplaceFilter || marketplaceFilter === '') &&
      (product.PromotionsTitle.toLowerCase().includes(searchQuery.toLowerCase()) || searchQuery === '')
    );
  });

  const handleObserver = (entities) => {
    const target = entities[0];
    if (target.isIntersecting) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  const override = css`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 9999;
  `;

  const handleViewMoreClick = async () => {
    setIsLoadingMore(true);
    setPage((prevPage) => prevPage + 1);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/promotions/?page=${page}`);
      const data = response.data.results;
      setPromotions((prevPromotions) => [...prevPromotions, ...data]);
      setIsLoadingMore(false);
    } catch (error) {
      console.error('Error fetching promotions:', error);
      setIsLoadingMore(false);
    }
  };

  return (
    <div className="product-search-results2">
      {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
      <div className="filters2">
        <div className="marketplace-filter2">
          <label style={{ fontSize: '25px', fontWeight: 'bold', marginTop: '20px', marginBottom: '20px', paddingRight: '20px' }}>
            Marketplace:
          </label>
          <select onChange={(event) => setMarketplaceFilter(event.target.value)}>
            <option value="">All</option>
            <option value="Amazon">Amazon</option>
            <option value="Noon">noon</option>
            <option value="Jumia">Jumia</option>
          </select>
        </div>
      </div>
      <div className="product-list-container">
        <div className="product-list2">
          {showFirstSpinner && isLoading ? (
            <div className="spinner-container1">
              <ClipLoader color="#000" loading={isLoading} css={override} size={50} />
            </div>
          ) : (
            filteredProducts.map((product, index) => (
              <div key={product.PromotionID} className="product2">
                <div className="product-details2">
                  <img src={`./images/${product.Marketplace}.png`} alt={product.Marketplace} className="mlogo2" />
                  <h3>{product.PromotionsTitle}</h3>
                  <p className="coupon">
                    <strong>Coupon Code:</strong> {product.PromotionsCoupon}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
        {!isLoadingMore && !isLoading && filteredProducts.length > 0 && filteredProducts.length % 21 === 0 && (
          <div className="view-more">
            <button type="button" onClick={handleViewMoreClick}>
              View More
            </button>
          </div>
        )}
        {isLoadingMore && (
          <div className="spinner-container2">
            <ClipLoader color="#000" loading={isLoadingMore} css={override} size={50} />
          </div>
        )}
      </div>
    </div>
  );
}

export default Promotions;
