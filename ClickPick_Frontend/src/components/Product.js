import React, { useEffect, useState } from 'react';
import { FaStar } from 'react-icons/fa';
import Navbar_not_Signin from './Navbar_not_Signin.js';
import Navbar from './Navbar.js';
import './Product.css';
import axios from 'axios';
import { Link, useLocation, useParams } from 'react-router-dom';
import { css } from '@emotion/react';
import { ClipLoader } from 'react-spinners';
import SliderComponent from './SliderComponent';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import ColorBoxes from './ColorBoxes';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ReferenceLine,
  LabelList,
} from 'recharts';

const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const override = css`
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
`;


function Product() {
  const [activeButton, setActiveButton] = useState('specifications');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSellerInfo, setShowSellerInfo] = useState(false);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const { Product_id } = useParams();
  const [positiveReviewsCount , setPositiveReviewsCount ] = useState(0);
  const [negativeReviewsCount , setNegativeReviewsCount ] = useState(0);
  const [Positive , setPositive] = useState(0);
  const [Negative , setNegative] = useState(0);
  const [ReviewsCount, setReviewsCount] = useState(0);
  const [dataArr, setData] = useState([]);
  const [favoriteProducts, setFavoriteProducts] = useState([]);

  const [aspedct_list, setAspectList] = useState([]);
  const [sub_Category, setsub_Category] = useState('');


  const handleButtonClick = (buttonName) => {
    setActiveButton(buttonName);
  };

  const handleSellerInfoClick = (productId) => {
    setShowSellerInfo((prevState) =>
      prevState === productId ? null : productId
    );
  };
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
          // Update the favorite products list after adding a favorite
          fetchFavoriteProducts();
        })
        .catch((error) => {
          console.error('Error adding favorite:', error);
        });
    } else {
      window.location.href = '/SignIn';
    }
  }

  useEffect(() => {
    checkLoginStatus();
    document.body.style.backgroundColor = 'white';
    fetchProducts();
  }, []);

  const checkLoginStatus = () => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    const isLoggedIn = accessToken && refreshToken;
    setIsLoggedIn(isLoggedIn);
  };
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
  
  const fetchProducts = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/product/${Product_id}`
      );
      const data = response.data;

      console.log(data);
      setsub_Category(data[0].ProductSubCategory)
      ///////// Aspect Part ////////
      console.log(data[0].ProductAspects)
      console.log("Seller Sentiment Resutls",data[0].SellerSentimentAnalysis);

      // Given data in string format

      // Convert the string to an array of JavaScript objects
      const aspect_data = eval(data[0].ProductAspects.replace(/OrderedDict/g, ''));

      // Create a new list with separate dictionaries
      const newDataList = aspect_data.map(item => {
        const newItem = {};
        Object.entries(item).forEach(([key, value]) => {
          newItem[key] = value;
        });
        return newItem;
      });
      const aspect_dic = newDataList.map(obj => {
        const newObj = {};
        newObj['Topic'] = obj[0];
        newObj['ReviewsCount'] = obj[1];
        newObj['PositivePercentage'] = obj[2];
        newObj['NegativePercentage'] = obj[3];
        return newObj;
      });
      console.log(aspect_dic);
      const sortedList = aspect_dic.sort((a, b) => b.ReviewsCount - a.ReviewsCount);
      const largestTenReviews = sortedList.slice(0, 10);

      console.log("Largeest 10: Topics: ",largestTenReviews)
      setAspectList(largestTenReviews)
      


      //////////////Sentiment Part////////
      const regex = /[0-9.]+/g;
      const matches = data[0].ProductSentimentAnalysis.match(regex);
      console.log(matches)
      // Convert the extracted values to numbers
      const values = matches.map(match => parseFloat(match));
      const positiveValue=values[0]
      const negativeValue=values[1]
      const reviewsCount=values[2]

      console.log("Sentiment Resutls",values); // Output: [96.97, 3.03, 33]
      
      const positiveReviewsCount = Math.round(reviewsCount * (positiveValue / 100));
      const negativeReviewsCount = Math.round(reviewsCount * (negativeValue / 100));
      console.log(positiveReviewsCount)
      // Define the data array
      const dataArr = [
        { name: 'Positive', value:positiveValue},
        { name: 'Negative', value:negativeValue},
      ];
      console.log(dataArr)
      // Set the calculated values and data array to state
      setPositiveReviewsCount(positiveReviewsCount);
      setNegativeReviewsCount(negativeReviewsCount);

      setPositive(positiveValue);
      setNegative(negativeValue);
      setReviewsCount(reviewsCount);
      setData(dataArr);

      setProducts(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching products:', error);
      setIsLoading(false);
    }
  };

  const getSortedProducts = () => {
    return Object.values(products).sort(
      (a, b) =>
        parseFloat(a.ProductPrice.replace(',', '')) -
        parseFloat(b.ProductPrice.replace(',', ''))
    );
  };

  const sortedProducts = getSortedProducts();
  const cheapestProduct = products[0];
  const productBoxes = sortedProducts.map((product) => (
    <div key={product.ProductID} className="product-box">
      <div className="product-info">
        <img
          src={`/images/${product.Marketplace}.png`}
          alt={product.Marketplace}
          className="mlogo"
        />
        <div className="title">
          {isLoading ? (
            <ClipLoader size={20} color={'#000000'} loading={isLoading} />
          ) : (
            product.ProductTitle
          )}
        </div>
        <div className="price">
          <span className="currency">EGP</span>
          {product.ProductPrice}
        </div>
      </div>
      <div className="seller-button-container">
        <button
          className="seller-button"
          onClick={() => handleSellerInfoClick(product.ProductID)}
        >
          Seller Info
        </button>
      </div>
      {showSellerInfo === product.ProductID && (
        <div className="seller-info-box">
          <div className="SellerName">{product.SellerName}</div>
          <p className="selleranalysis">Reviews Analysis</p>
          <div className="seller-info-list">
            {product.SellerSentimentAnalysis.split(',').map((item, index) => (
              <div key={index} className="seller-info-item">
                <strong>{item.replace(/[\[\]\'\"]+/g, '').trim()}</strong>
              </div>
            ))}
          </div>
        </div>
      )}
      <a
        href={product.ProductLink}
        className="product-link"
        style={{
          fontSize: '18px',
          textDecoration: 'none',
          color: 'blue',
          pointerEvents: 'none !important',
        }}
      >
        Go To The Product {'>>'}
      </a>
    </div>
  ));

  const goToHomePage = () => {
    // Perform the navigation to the home page
    window.location.href='/';
  };

  const goToProductsPage = () => {
    // Perform the navigation to the products page
    window.location.href=`/Products/subcategory/${sub_Category}`;
  };

  // Conditional rendering check
  if (!products || products.length === 0) {
    return (
      <div>
        {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
        <div className="header-container"></div>
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh' // Adjust this value based on your requirements
          }}
        >
          <div className="cat-text">
            {isLoading ? (
              <div className="loading">
                <ClipLoader css={override} size={50} color={'#000000'} loading={isLoading} />
              </div>
            ) : null}
          </div>
        </div>
      </div>
    );
  }
  const chartWidth = aspedct_list.length < 5 ? 600 : aspedct_list.length > 10 ? 910 : 910;
  const marginLeft = aspedct_list.length < 5 ? '160px' : '';
  const COLORS = ['#00D100', '#f44336'];
  const isProductFavorite = favoriteProducts.includes(cheapestProduct.ProductID);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        
        <div
          className="custom-tooltip"
          style={{
            backgroundColor: 'rgba(245, 245, 245, 0.7)',
            padding: '10px',
            borderRadius: '4px',
          }}
        >
          <p className="label">{`${label}`}</p>
          <p className="review-count">{`Reviews Count: ${payload[0].payload.ReviewsCount}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    
    <div>
      {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
      <div className="header-container"></div>
      <div className="cat-text">
        <button type="button" onClick={goToHomePage}>
          {cheapestProduct && cheapestProduct.ProductCategory}
        </button>
        <span className="cat-sub">
          /
        </span>
        <button type="button" onClick={goToProductsPage}>
          {cheapestProduct && cheapestProduct.ProductSubCategory}
        </button>
      </div>
      <div className="cheapest-product">
        {cheapestProduct && (
          <React.Fragment>
            <div className="ProductImage">
              <img
                className="product-image"
                src={cheapestProduct.ProductImage}
                alt="Product"
              />
            </div>

            <div>
              <div className="ProductTitle">{cheapestProduct.ProductTitle}</div>
              
              <div className="ProductRatings">
              <FaStar className="star-icon" />{' '}
              {cheapestProduct.ProductRatings !== '' ? (
                <>
                  {cheapestProduct.ProductRatings} ({cheapestProduct.ProductRatingCount})
                </>
              ) : (
                <>
                  No Rating{' '}
                  {cheapestProduct.ProductRatingCount.length === 0 ? '(0)' : `(${cheapestProduct.ProductRatingCount})`}
                </>
              )}
            <button
              className={`favorite2-button ${isProductFavorite ? 'clicked' : ''}`}
              onClick={(event) => handleFavoriteClick(event, cheapestProduct.ProductID)}
            ></button>
            </div>

              <div className="ProductPrice">
                Price: EGP {cheapestProduct.ProductPrice}
              </div>
              {cheapestProduct.ProductOldPrice && (
                <p className="ProductPrice_before">
                  EGP {cheapestProduct.ProductOldPrice}
                </p>
              )}
              <div className="Description">Description</div>
              <div className="ProductDescription">
                {cheapestProduct.ProductDescription}
              </div>
            </div>
          </React.Fragment>
        )}
      </div>

      <div className="product-buttons">
        <button
          className={`button-specifications ${
            activeButton === 'specifications' ? 'active' : ''
          }`}
          onClick={() => handleButtonClick('specifications')}
        >
          Specifications
        </button>
        <button
          className={`button-prices ${activeButton === 'price' ? 'active' : ''}`}
          onClick={() => handleButtonClick('price')}
        >
          Prices
        </button>
      </div>
      <hr />

      {isLoading ? (
        <div className="loading">
          <ClipLoader css={override} size={50} color={'#000000'} loading={isLoading} />
        </div>
      ) : (
        <React.Fragment>
             {activeButton === 'specifications' && (
    <div className="product-info">
      <div className="specifications">
        <table>
          <tbody>
            {cheapestProduct && cheapestProduct.ProductSpecifications && (
              cheapestProduct.ProductSpecifications
                .slice(1, -1) // Remove the opening and closing brackets
                .split(', ') // Split the string into individual specifications
                .filter(specification => specification.startsWith("'")) // Filter out the unwanted specifications
                .map((specification, index) => {
                  const specificationParts = specification.slice(1, -1).split(':');
                  if (specificationParts.length === 2) {
                    const key = specificationParts[0].trim();
                    const value = specificationParts[1].trim();
                    return (
                      <tr key={index}>
                        <td>{key}</td>
                        <td>{value}</td>
                      </tr>
                    );
                  } else {
                    return null;
                  }
                })
            )}
              {!cheapestProduct || !cheapestProduct.ProductSpecifications || cheapestProduct.ProductSpecifications.length === 0 && (
                <tr>
                  <td colSpan="2">No specifications available</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

              <div className="sentiment">
                <p className="Reviews-Analysis">Reviews Analysis</p>
                {/* <PieChartComponent productId={productId_charts} /> */}
                <ResponsiveContainer width="100%" height="100%">
                  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', paddingTop: 0, marginBottom: 0 }}>
                    {ReviewsCount > 0 ? (
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <PieChart width={400} height={400}>
                          <Pie
                            data={dataArr }
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={renderCustomizedLabel}
                            outerRadius={125}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {dataArr.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip
                            contentStyle={{
                              backgroundColor: 'rgba(245, 245, 245, 0.7)',
                              borderRadius: '4px',
                              width:'250px'
                            }}
                            formatter={(value, name, props) => {
                              if (name === 'Positive') {
                                return [
                                  <span>
                                    {`${Positive}%`}
                                    <br />
                                    Positive Reviews Count: {positiveReviewsCount}
                                  </span>,
                                  name,
                                ];
                              } else if (name === 'Negative') {
                                return [
                                  <span>
                                    {`${Negative}%`}
                                    <br />
                                    Negative Reviews Count: {negativeReviewsCount}
                                  </span>,
                                  name,
                                ];
                              }
                              return [value, name];
                            }}
                          />
                        </PieChart>
                        <ColorBoxes/>
                      </div>
                    ) : (
                      <div style={{ position: 'relative' }}>
                        <p style={{ marginLeft: '50px', marginTop: "100px", fontSize: "19px" }}>This Product Doesn't Have Any Reviews</p>
                      </div>
                    )}
                  </div>
                </ResponsiveContainer>
              </div>
              <div className="summarization">
                <p className="Reviews-summarization">
                  Product Aspect Sentiment Analysis
                </p>
                {aspedct_list.length > 0 } {/* Place the ColorBoxes component before the ResponsiveContainer */}


                <ResponsiveContainer width={chartWidth} height={650}>
                  <div style={{ width: '100%', height: '100%', marginLeft }}>
                    {aspedct_list.length > 0 ? (
                      <BarChart
                        width={chartWidth}
                        height={650}
                        data={aspedct_list}
                        margin={{
                          top: 25,
                          right: 30,
                          left: 45,
                          bottom: 30,
                        }}
                        barCategoryGap={8}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                          dataKey="Topic"
                          interval={0}
                          angle={-30}
                          textAnchor="end"
                          height={100}
                        />
                        <YAxis
                          label={{
                            value: 'Percentage',
                            angle: -90,
                            position: 'insideRight',
                            offset: 50,
                            right: 50,
                            fontSize: 18,
                          }}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <ReferenceLine y={0} stroke="#000" />
                        <Bar dataKey="PositivePercentage" fill="#00D100">
                          <LabelList
                            dataKey="PositivePercentage"
                            position="top"
                            formatter={(value) => `${value}`}
                          />
                        </Bar>
                        <Bar dataKey="NegativePercentage" fill="#f44336">
                          <LabelList
                            dataKey="NegativePercentage"
                            position="top"
                            formatter={(value) => `${value}`}
                          />
                        </Bar>

                      </BarChart>
                      
                    ) : (
                      <div style={{ textAlign: 'center', marginTop:"60px",fontSize:"20px" }}>
                        <p>No data available</p>
                      </div>
                    )}
                      </div>

                  </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeButton === 'price' && <div className="price">{productBoxes}</div>}
        </React.Fragment>
      )}
    </div>
  );
}
Product.demoUrl = 'https://codesandbox.io/s/pie-chart-with-customized-label-dlhhj';

export default Product;
