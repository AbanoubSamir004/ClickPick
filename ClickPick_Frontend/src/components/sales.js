import React, { useState, useEffect, useRef } from 'react';
import './products.css';
import Navbar_not_Signin from './Navbar_not_Signin.js';
import { Link, useLocation, useParams } from 'react-router-dom';
import { css } from '@emotion/react';
import { ClipLoader } from 'react-spinners';
import SliderComponent from './SliderComponent';
import { FaStar } from 'react-icons/fa';
import axios from 'axios';
import Navbar from './Navbar.js';

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

//const brands = ["Apple", "Samsung", "Microsoft"]
const marketplaces = ["Amazon", "Noon", "Jumia"];

const MIN = 100;
const MAX = 100000;

function ProductSearchResults() {
  const [brands, setBrands] = useState([]);
  const [brandFilter, setBrandFilter] = useState([]);
  const [marketplaceFilter, setMarketFilter] = useState([]);
  const [priceFilter, setPriceFilter] = useState([MIN, MAX]);
  const [numProductsShown, setNumProductsShown] = useState(21);
  const [productsData, setProductsData] = useState([]); // Define productsData and set initial value to an empty array
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMoreData, setHasMoreData] = useState(true);
  const [fetchedProducts, setFetchedProducts] = useState([]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [initialLoad, setInitialLoad] = useState(true);
  const isLoggedIn = localStorage.getItem('accessToken') && localStorage.getItem('refreshToken');
  const location = useLocation();
  const { query, subcategory } = useParams();
  const [favoriteProducts, setFavoriteProducts] = useState([]);

  if (location.pathname.includes('/Products/search')) {
    console.log('Search query:', query);
  } else if (location.pathname.includes('/Products/subcategory')) {
    console.log('Subcategory:', subcategory);
  }

  useEffect(() => {
    document.body.style.backgroundColor = '#FDFDFD';
    
    const fetchData = async () => {
      try {
        setIsLoading(true);
    
        let endpoint = 'http://127.0.0.1:8000/api/sales/filter/';
        
        const response = await axios.get(endpoint, {
          params: {
            page: currentPage,
            numProducts: numProductsShown,
          },
        });
    
        if (response.data.results.length === 0) {
          setHasMoreData(false);
        } else {
          setFetchedProducts((prevData) => {
            // Append the new products to the end of the array
            return [...prevData, ...response.data.results];
          });
        }
    
        setIsLoading(false);
        setTotalProducts(response.data.count);
        setProductsData(response.data.results);
        console.log('Products Data:', response.data.results);
      } catch (error) {
        console.error('Error fetching data:', error);
        setIsLoading(false);
        setInitialLoad(false);
      }
    };

    fetchData();
  }, [currentPage, query, subcategory, numProductsShown]);

 const fetchFavoriteProducts = async () => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const headers = {
        Authorization: `Bearer ${accessToken}`
      };
  
      const response = await axios.get('http://127.0.0.1:8000/api/auth/favoriteList/', { headers });
      setFavoriteProducts(response.data.favorite_products);
    } catch (error) {
      console.error('Error fetching favorite products:', error);
    }
  };
  useEffect(() => {
    // Other code...
  
    fetchFavoriteProducts();
  }, []);
  
  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/sales/unique-brands/');
        const brands = response.data;
        setBrands(brands);
        console.log('Brands:', brands);
      } catch (error) {
        console.error('Error fetching brands:', error);
      }
    };

    fetchBrands();
  }, []);
  console.log('Brands:', brands);
  

  function handleBrandFilterChange(ProductBrand) {
    if (brandFilter.includes(ProductBrand)) {
      setBrandFilter(brandFilter.filter(item => item !== ProductBrand));
    } else {
      setBrandFilter([...brandFilter, ProductBrand]);
    }
  }

  function handleMarketFilterChange(Marketplace) {
    if (marketplaceFilter.includes(Marketplace)) {
      setMarketFilter(marketplaceFilter.filter(item => item !== Marketplace));
    } else {
      setMarketFilter([...marketplaceFilter, Marketplace]);
    }
  }

  function handlePriceFilterChange(newValues) {
    setPriceFilter(newValues);
  }

  const filteredProducts = fetchedProducts.map(product => ({
    ...product,
    isFavorite: favoriteProducts.includes(product.ProductID)
  })).filter(product =>
    (brandFilter.length === 0 || brandFilter.includes(product.ProductBrand)) &&
    (marketplaceFilter.length === 0 || marketplaceFilter.includes(product.Marketplace)) &&
    (parseInt(product.ProductPrice) >= priceFilter[0] && parseInt(product.ProductPrice) <= priceFilter[1])
  );
  function handleFavoriteClick(event, productID) {
    event.preventDefault();
    if (isLoggedIn) {
      event.target.classList.toggle('clicked');
  
      const accessToken = localStorage.getItem('accessToken');
      const headers = {
        Authorization: `Bearer ${accessToken}`
      };
  
      axios
        .post('http://127.0.0.1:8000/api/auth/favoriteList/', { product_id: productID }, { headers })
        .then((response) => {
          console.log('Favorite Added:', response.data);
          fetchFavoriteProducts(); // Fetch the updated favorite products list
        })
        .catch((error) => {
          console.error('Error adding favorite:', error);
        });
    } else {
      window.location.href = '/SignIn';
    }
  }
    
  function handleViewMoreClick() {
    const remainingProducts = totalProducts - fetchedProducts.length;
    const productsToFetch = Math.min(remainingProducts, numProductsShown);
    setNumProductsShown((prevNum) => prevNum + productsToFetch);
    setCurrentPage((prevPage) => prevPage + 1);
  }

  



  return (
    <div className="product-search-results">
      {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
      <div className="filters">
        <h2 style={{ fontSize: '27px' }}>Filters</h2>
        <div className="price-filter">
          <SliderComponent setPriceFilter={handlePriceFilterChange} />
        </div>
        <div className="marketplace-filter">
          <label style={{ fontSize: '20px', fontWeight: 'bold' }}>Marketplace:</label>
          {marketplaces.map(Marketplace => (
            <div key={Marketplace} className="checkbox-container">
              <input
                type="checkbox"
                id={`marketplace-${Marketplace.toLowerCase()}`}
                value={Marketplace}
                onChange={event => handleMarketFilterChange(event.target.value)}
                checked={marketplaceFilter.includes(Marketplace)}
              />
              <label htmlFor={`marketplace-${Marketplace.toLowerCase()}`}>{Marketplace}</label>
            </div>
          ))}
        </div>
        <div className="brand-filter">
          <label style={{ fontSize: '20px', fontWeight: 'bold' }}>Brand:</label>
          {brands.map(ProductBrand => (
          <div key={ProductBrand} className="checkbox-container">
            <input
              type="checkbox"
              id={`brand-${ProductBrand.toLowerCase()}`}
              value={ProductBrand}
              onChange={event => handleBrandFilterChange(event.target.value)}
              checked={brandFilter.includes(ProductBrand)}
            />
            <label htmlFor={`brand-${ProductBrand.toLowerCase()}`}>{ProductBrand}</label>
          </div>
          ))}
        </div>
      </div>
     
      <div className="product-list">
        
        {filteredProducts.length === 0 && !isLoading && (
        <h3>No products found.</h3>
      )}
        {filteredProducts.map(product => (
            <div key={product.ProductID} className="product">
              <Link key={product.ProductID} to={`/product/${product.ProductID}`} className="product-link2">
                <img src={product.ProductImage} alt={product.ProductTitle} />
                <div className="product-details">
                  <h3>{product.ProductTitle.length > 25 ? product.ProductTitle.substr(0, 25) + '...' : product.ProductTitle}</h3>
                </div>
              </Link>
              <div className="product-actions">
                <p className="price">EGP {product.ProductPrice}</p>
                {product.ProductOldPrice && <p className="before">EGP {product.ProductOldPrice}</p>}
                <p className='ratingcount'>
                  {product.ProductRatings !== '' ? (
                    `${product.ProductRatings} (${product.ProductRatingCount})`
                  ) : (
                    <>
                      No Rating{' '}
                      {product.ProductRatingCount.length === 0 ? '(0)' : `(${product.ProductRatingCount})`}
                    </>
                  )}
                </p>
                <div className='ProductRatings0'><FaStar className='star-icon' /></div>
                </div>
              <button
            className={`favorite-button ${product.isFavorite ? 'clicked' : ''}`}
            onClick={(event) => handleFavoriteClick(event, product.ProductID)}
          ></button>            </div>
        ))}
        {isLoading && (
          <div className="loading">
            <ClipLoader css={override} size={50} color={'#000000'} loading={isLoading} />
          </div>
        )}
        
        { !isLoading && initialLoad && hasMoreData && filteredProducts.length > 0 && (
          <div className="view-more">
            <button className="view-more-button" type="button" onClick={handleViewMoreClick}>
              View More
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductSearchResults;