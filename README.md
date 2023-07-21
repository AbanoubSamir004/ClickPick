# ClickPick Website

## Abstract
E-commerce websites often face challenges in helping customers find specific products quickly and differentiating themselves in a competitive market. ClickPick is an e-commerce platform that addresses these challenges by providing a user-friendly and intelligent design. This readme file provides an overview of the ClickPick website, its objectives, and the solutions it offers to enhance the shopping experience for customers.

## Table of Contents
1. [Introduction](#introduction)
    - [Problem](#problem)
    - [Objective](#objective)
    - [Solution](#solution)
2. [Features](#features)
    - [Aggregating Products](#aggregating-products)
    - [Filtering Options](#filtering-options)
    - [Product Information](#product-information)

## Introduction<a name="introduction"></a>
ClickPick is an innovative e-commerce platform that aims to provide users with a seamless and efficient online shopping experience. By utilizing statistical analysis techniques such as sentiment analysis and aspect sentiment analysis (topic modeling), ClickPick offers a range of features to help users find the best products from multiple marketplaces.

### Problem<a name="problem"></a>
E-commerce websites often struggle to help customers find products efficiently and stand out among their competitors. Customers may spend significant time searching for specific products, comparing prices, and analyzing reviews across various websites. This process can be time-consuming and overwhelming, hindering the overall shopping experience.

### Objective<a name="objective"></a>
The objective of ClickPick is to address these challenges by providing a user-friendly platform that simplifies the product search and decision-making process. ClickPick aims to aggregate products from multiple marketplaces, offer effective filtering options, present comprehensive product information, and implement a referral system for easy purchasing.

### Solution<a name="solution"></a>
ClickPick's solution involves utilizing statistical analysis techniques, such as sentiment analysis and aspect sentiment analysis (topic modeling), to enhance the shopping experience. By aggregating products from multiple marketplaces, providing filtering options, presenting detailed product information (including pros, cons, and pricing), and implementing a referral system, ClickPick aims to streamline the product discovery and purchasing process for users.

## Features<a name="features"></a>

### Aggregating Products<a name="aggregating-products"></a>
ClickPick aggregates products from multiple marketplaces (Amazon, Jumia and Noon), ensuring that users have access to a wide range of options. By bringing products from various sources onto a single platform, ClickPick simplifies the search process and saves users time and effort.

### Filtering Options<a name="filtering-options"></a>
ClickPick provides advanced filtering options to help users find the best product that meets their specific requirements. Users can filter products based on criteria such as price range, brand, category, and more. These filtering options enable users to quickly narrow down their choices and find products that align with their preferences.

### Product Information<a name="product-information"></a>
ClickPick presents comprehensive product information to assist users in making informed decisions. Along with detailed descriptions, ClickPick provides an analysis of the sentiment and aspect sentiment (topic modeling) of product reviews. Users can access pros, cons, pricing information, and valuable insights from other customers, all in one place.

The project documentation will cover various aspects, including stakeholder analysis, user analysis, system analysis and design, functional and non-functional requirements, design diagrams, development tools, and detailed explanations of the main features and models used.

## Methodology<a name="methodology"></a>
ClickPick utilizes the following methodologies and models to enhance the platform's functionality:

- **Product Matching Model:** Utilizes the product2vec model to convert preprocessed product text data into numerical feature vectors. Cosine similarity is calculated to determine similarities between products in specific categories. Logistic regression is used for classification and finding matching pairs based on similarity scores.

- **Sentiment Analysis Model:** Combines machine learning and deep learning techniques. Text data is preprocessed and TF-IDF vectorization is applied to convert it into numerical features. Various machine learning models (Random Forest, Logistic Regression, SVC, Naive Bayes) and deep learning models (RNN, LSTM, BILSTM, CNN, BIGRU) are trained and evaluated for sentiment analysis.

- **Aspect Sentiment Analysis:** Two approaches are used - topic modeling and supervised learning. Topic modeling involves preprocessing and clustering using the LDA algorithm. Sentiment analysis is conducted using logistic regression on the identified topics. Supervised learning involves initially unlabeled reviews, TF-IDF feature extraction, and logistic regression training for sentiment prediction.

## Technologies Used<a name="technologies-used"></a>
ClickPick utilizes the following technologies for development:

- Python
- keras
- Tensorflow
- Discord
- Jupyter Notebook
- Visual Studio Code
- Google Colab
- React
- Django
- MongoDB
- Kaggle
- GitHub

The chosen technologies provide a robust and efficient development environment for implementing the ClickPick e-commerce platform.

## Demo Video<a name="demo-video"></a>
To get a glimpse of how ClickPick works and the features it offers, please watch our demo video below:


https://github.com/AbanoubSamir004/ClickPick/assets/60902991/928539ab-4e7c-4192-84b7-d38f65e08798


## About Us<a name="about-us"></a>
We are a team of dedicated student AI enthusiasts who have come together to create ClickPick, a platform that revolutionizes the online shopping experience. Our mission is to make decision-making in online shopping more flexible and easy for users like you.

By aggregating products from different marketplaces and utilizing AI technology, we ensure that you have access to a comprehensive selection of products. We provide detailed feature comparisons, price analysis, and sentiment analysis on product and seller reviews, allowing you to make informed decisions effectively.

We are passionate about enhancing your online shopping experience and helping you make smarter choices. With our user-friendly platform, navigating the online marketplace and finding the perfect product has never been easier.

Thank you for choosing our website. We look forward to assisting you in making confident and informed purchasing decisions.


## Our Team<a name="our-team"></a>
We are proud to introduce our talented team of AI enthusiasts who have worked tirelessly to bring you the ClickPick platform. Here are the members of our team:

1. Abanoub Samir - [GitHub](https://github.com/AbanoubSamir004)
2. Aram Gamal - [GitHub](https://github.com/aramgamal)
3. Joyce Fayek - [GitHub](https://github.com/JoyceFayek)
4. Dina Zakaria - [GitHub](https://github.com/dinazak)
5. Fady Essam - [GitHub](https://github.com/fadyyessam11)

Each member of our team has brought their unique skills and expertise to develop and enhance ClickPick. We are committed to delivering the best possible online shopping experience for our users.

If you have any questions or feedback, please don't hesitate to reach out to us. Happy shopping!
