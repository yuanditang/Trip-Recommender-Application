# Trip Recommender Application

**Team Members:**  
- John Creighton  
- Yuandi Tang  

**Course:** DS5110 - Summer 2025  
**Instructor:** Professor Nafa  

---

## Project Overview

The Trip Recommender Application helps users discover personalized travel destinations based on preferences such as budget, climate, trip duration, and origin city. It leverages real-time APIs, a user-friendly interface, and the ChatGPT API to translate natural language questions into SQL queries that dynamically fetch relevant destinations from a structured database.

---

## Key Features

- 🧠 Natural Language Querying via ChatGPT API  
  Users input questions like “Where can I travel for under $1000 with warm weather?” and receive recommendations in plain English.

- 🗃️ Structured Trip Database  
  Cities, hotels, distances, prices, and amenities stored in a normalized SQL database.

- 🌐 API Integration  
  Uses external APIs (e.g., Amadeus, Numbeo) to populate destination information.

- 📊 Contextual Result Explanation  
  Results returned as natural-language responses summarizing query results.

---

## Technologies Used

- Python (Flask, Pandas, SQLAlchemy)  
- SQLite (development) / PostgreSQL (production)  
- OpenAI GPT API (text-to-SQL)  
- Bootstrap (UI), HTML/CSS  
- RESTful API and JSON

---

## New Workflow Architecture

1. User inputs a natural question:  
   e.g., "Show me cities under $800 that are beach destinations."

2. GPT model converts the question → SQL query:  
   SELECT name FROM Destination WHERE avg_price < 800 AND tags LIKE '%beach%';

3. SQL query is run against trip_recommender.db

4. Results are formatted back into human-friendly sentences:  
   e.g., “Here are some beach destinations under $800: Miami, Cancun, and Lisbon.”

---

## Updated Project Timeline (8 Weeks)

| Week | Deliverables                                                   |
|------|----------------------------------------------------------------|
| 1    | Define requirements, finalize API list, and ChatGPT setup      |
| 2    | Build destination database schema and populate initial data    |
| 3    | Design natural language → SQL prompt patterns                  |
| 4    | Create back-end endpoint to call GPT and query DB              |
| 5    | Build front-end form and display results                       |
| 6    | Refine prompts and response formatting                         |
| 7    | Conduct full testing; polish interface and fix edge cases      |
| 8    | Final documentation, presentation, and demo                    |

---

## Future Enhancements

- Intelligent follow-up questions to refine recommendations  
- Visualization of travel clusters (map + distance)  
- Auto-evaluation of GPT SQL performance and accuracy  
- Voice-based queries

---

## Contact

- John Creighton – creighton.jo@northeastern.edu  
- Yuandi Tang – tang.yuand@northeastern.edu
