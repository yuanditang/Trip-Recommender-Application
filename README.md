Here is a revised README, incorporating the detailed information and technical specifics from the original LaTeX technical report.

# Trip Recommender Application

**Team Members:**

  - John Creighton
  - Yuandi Tang

**Course:** DS5110 - Summer 2025
**Instructor:** Professor Nafa

-----

## Project Overview

Modern travel planning is often overwhelming. While online travel agencies (OTAs) offer countless options, users can experience **decision fatigue** from navigating complex filters and pre-packaged deals that lack deep personalization.

This project addresses that gap with a data-driven Trip Recommender system. It provides a more intuitive and personalized planning experience by translating simple, conversational user queries into sophisticated, multi-constraint database queries. Our system moves beyond basic filters to holistically consider a user's budget, time constraints, climate preferences, and even visa requirements to suggest genuinely tailored travel itineraries.

-----

## Key Features

  - **Conversational Querying:** Utilizes OpenAI's **GPT-4** to translate natural language prompts (e.g., *"I want to go somewhere historical in March for a week from Philadelphia"*) into precise SQL queries.
  - **Multi-Source Data Integration:** The recommendation engine is powered by a comprehensive knowledge base built from multiple sources:
      - **NASA POWER API:** For historical climate data across 774 destinations.
      - **Amadeus API:** For real-time hotel pricing and availability.
      - **Numbeo:** For granular cost-of-living indices.
      - **Custom Datasets:** For visa requirements, destination metadata, and a pre-computed matrix of **598,302** distances.
  - **Dynamic Constraint Handling:** Intelligently filters destinations based on a combination of user needs:
      - **Budget & Time:** Dynamically calculates a feasible travel radius based on total budget and trip duration.
      - **Climate:** Filters by temperature and precipitation preferences based on the month of travel.
      - **Logistics:** Automatically validates visa requirements and safety indices for the traveler's citizenship.
  - **Transparent & Interactive UI:** A web interface built with **Flask** and **Bootstrap** provides a seamless user experience. To build trust and offer educational insight, the application transparently displays the generated SQL query alongside the natural language recommendations.
  - **Contextual Result Explanation:** Raw data results are transformed back into a friendly, natural-language summary, explaining *why* each destination was recommended.

-----

## 🏛️ System Architecture

The application is built on a modular, **three-tier architecture** for scalability and maintainability:

1.  **Presentation Layer (Frontend):** A responsive Flask web application using Bootstrap for styling. This layer handles all user interaction.
2.  **Business Logic Layer (Backend):** The core Python engine that integrates with the GPT-4 API for natural language processing and implements the constraint-based filtering algorithms.
3.  **Data Access Layer (Database):** A normalized **SQLite** database designed with an optimized schema to support complex, multi-table queries efficiently.

-----

##  Technologies Used

  - **Backend:** Python (Flask, Pandas, SQLAlchemy)
  - **Database:** SQLite
  - **NLP:** OpenAI GPT-4 API
  - **Frontend:** HTML/CSS, Bootstrap 5
  - **Core Libraries:** `requests` (for API integration), `concurrent.futures` (for parallel data fetching)

-----

## Workflow

1.  **User Input:** A user enters a natural language query into the web interface.

      - *e.g., "I want to travel within the US from Boston for $2000"*

2.  **Text-to-SQL Conversion:** The backend sends the query and database schema context to the GPT-4 API.

      - *GPT-4 generates a corresponding SQL query.*

    <!-- end list -->

    ```sql
    SELECT DISTINCT Dest.name FROM Distance AS D JOIN Destination AS Dest ON D.destination_id = Dest.destination_id JOIN CostOfLiving AS Cl ON Dest.destination_id = Cl.destination_id WHERE D.origin_id = (SELECT destination_id FROM Destination WHERE name LIKE '%Boston%') AND D.distance_km <= ((2000 - 15 - (5 * Cl.daily_avg_usd)) / 0.53) AND (Dest.country_id = 193) LIMIT 5;
    ```

3.  **Database Query:** The validated SQL query is executed against the `trip_recommender.db` database.

4.  **Response Generation:** The query results (a list of destinations) are sent back to GPT-4 to be formatted into a human-friendly paragraph.

      - *e.g., "Sure, I've found several exciting destinations within your budget. 1. Jacksonville: Famous for its beautiful beaches... 2. Philadelphia: Renowned for its rich history..."*

-----

## ✨ Future Enhancements

  - **Machine Learning Personalization:** Integrate user feedback and history to learn individual preferences.
  - **Interactive Map Visualization:** Display recommended destinations on an interactive map.
  - **Real-Time Pricing:** Integrate with live flight and hotel pricing APIs for bookable itineraries.
  - **Voice-Based Queries:** Allow users to ask questions via a voice interface.
  - **Collaborative Filtering:** Recommend destinations based on what similar users have enjoyed.

-----

## Contact

  - John Creighton – creighton.jo@northeastern.edu
  - Yuandi Tang – tang.yuand@northeastern.edu
