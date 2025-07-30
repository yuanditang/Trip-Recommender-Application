# Trip Recommender Application

**Team Members:**  
- John Creighton  
- Yuandi Tang  

**Course:** DS5110 - Summer 2025  
**Instructor:** Professor Nafa    

---

## Project Overview

The Trip Recommender Application helps users discover personalized travel destinations based on preferences such as budget, climate, trip duration, and origin city. It integrates real-time travel-related data and a custom-built recommendation engine, backed by a structured SQLite database. The application is designed to be modular, expandable, and able to support a range of data insights such as cost, safety, sentiment, and transportation efficiency.

---

## Features

- Real-Time API Integration (Amadeus, OpenWeatherMap, etc.)
- Destination database with city, region, and country-level detail
- Recommendation engine based on KNN (user preference similarity)
- Distance calculation using the Haversine formula
- Data extraction modules to populate destination and lodging tables
- Scalable project structure with testable modules

---

## Technologies Used

- Languages: Python, HTML/CSS (for future UI)
- Libraries: requests, pandas, sqlite3, scikit-learn, geopy
- Data: Real-time API (Amadeus), custom CSVs, SQLite DB
- Tools: Jupyter Notebook, Git, VS Code, SQLite CLI

---

## Dataset Description

This project uses multiple sources:

- Destination.csv: Custom-built list of over 80 destinations globally with columns for destination_id, name, region, latitude, longitude, and IATA code.
- Amadeus Hotel API: Retrieves hotelId, name, rating, pricing, geo location.
- HotelSentiment API: Sentiment and rating scores for sampled hotels.
- SQLite database: trip_recommender.db with schema tables Destination and Lodging.

The database contains location metadata for each destination and links to Lodging data via destination_id. Lodging includes hotel name, type, star rating, price per night, and sentiment scores.

---

## Tools and Methodologies

We use the following key tools and models:

- Python + Requests: API querying and automation
- pandas: Data wrangling, transformation, and I/O
- sqlite3: Relational database operations
- KNN Algorithm (Scikit-learn): Used for finding nearest destination neighbors based on user features
- Distance Matrix: Precomputed using Haversine formula and exported to CSV for modeling

Why KNN?
- It is interpretable, easy to update with new destinations, and does not require extensive training. This makes it ideal for prototyping a recommender system based on user similarity vectors.

---

## Preliminary Timeline (8 Weeks)

| Week | Tasks                                                                 |
|------|-----------------------------------------------------------------------|
| 1    | Finalize project scope, assign roles, explore APIs, gather city data |
| 2    | Design and create SQLite DB schema (Destination & Lodging)          |
| 3    | Write API wrappers for Amadeus & HotelSentiment                      |
| 4    | Fetch and load real data into DB (with sampling + error handling)   |
| 5    | Build distance matrix and KNN model for destination recommendation  |
| 6    | Construct prototype recommender function (with constraints)         |
| 7    | Test with mock user profiles and edge cases                         |
| 8    | Compile final report, markdown files, and submit codebase           |

---

## Entity Relationship Summary

- Destination Table  
  Columns: destination_id, name, country, region, latitude, longitude, iata

- Lodging Table  
  Columns: lodging_id, destination_id (FK), name, type, avg_price_per_night, rating, url, description

- Distance Table (intermediate CSV)  
  Columns: destination_id_1, destination_id_2, distance_km

---

## KNN Implementation Plan

- Normalize user inputs (e.g. budget, trip length, interest)
- Assign vectors to each destination (climate, avg cost, safety, etc.)
- Use scikit-learn NearestNeighbors to return Top 3–5 matching destinations

We plan to initially use manual feature weights and expand to more data-driven modeling later (e.g. PCA, clustering, or collaborative filtering).

---

## Progress and Observations

As of July 30:

- Successfully loaded 80+ destinations into SQLite
- Implemented hotel sampling from Amadeus & HotelSentiment APIs
- Created robust distance matrix using Haversine formula
- Built modular scripts for destination, hotel, and sentiment ingestion

---

## Future Extensions

- Travel time estimation from distance using multivariate regression
- Integration of real-time flight price APIs
- Full-stack web deployment with Flask or Streamlit
- More advanced ML models (e.g. content-based or hybrid recommender systems)
- User login, saved trips, collaborative filtering based on peer preferences

---

## Contacts

- John Creighton – creighton.jo@northeastern.edu  
- Yuandi Tang – tang.yuand@northeastern.edu
