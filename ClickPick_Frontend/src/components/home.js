import React from 'react';
import { Link } from 'react-router-dom';
import Navbar_not_Signin from './Navbar_not_Signin.js';
import Navbar from './Navbar.js';
import './home.css';

const categories = [
  {
    name: 'Electronics',
    subcategories: ['Mobile Phones', 'Tablets', 'Laptops', 'Headphones'],
  },
  {
    name: 'Gaming',
    subcategories: ['Games', 'Controllers', 'Cards'],
  },
  {
    name: 'Fashion',
    subcategories: ['Men', 'Women', 'Kids', 'Accessories'],
  },
  {
    name: 'Beauty',
    subcategories: ['Makeup', 'Skin Care', 'Body Care'],
  },
];

class Categories extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedCategory: categories[0],
      searchValue: '',
      isLoggedIn: false,
    };
  }

  handleCategoryHover = (category) => {
    this.setState({ selectedCategory: category });
  };

  handleContainerMouseLeave = () => {
    this.setState({ selectedCategory: categories[0] });
  };

  handleSearchChange = (event) => {
    this.setState({ searchValue: event.target.value });
  };

  handleSearchSubmit = (event) => {
    event.preventDefault();
    // window.location.href('`/Products/subcategory/${subcategory}`');
  };

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
    const { selectedCategory, isLoggedIn } = this.state;

    return (
      <div>
        <div className="header-container">
          {isLoggedIn ? <Navbar /> : <Navbar_not_Signin />}
        </div>

        <div className="categories-container" onMouseLeave={this.handleContainerMouseLeave}>
          <div className="Categories">
            <table className="categories-table">
              <tbody>
                {categories.map((category, index) => (
                  <tr
                    key={index}
                    className={`category-row ${category === selectedCategory ? 'selected' : ''}`}
                    onMouseEnter={() => this.handleCategoryHover(category)}
                  >
                    <td>{category.name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="subcategories-container">
            <table className="subcategories-table">
              <tbody>
                {selectedCategory &&
                  selectedCategory.subcategories.map((subcategory, index) => (
                    <tr key={index}>
                      <td>
                        <Link to={`/Products/subcategory/${subcategory}`} className="subcategory-link">{subcategory}</Link>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}

export default Categories;
