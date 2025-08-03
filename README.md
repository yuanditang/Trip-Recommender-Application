# Trip Recommender Application

**Team Members:** John Creighton, Yuandi Tang  
**Course:** DS5110 - Summer 2025  
**Instructor:** Professor Nafa  

---

## Project Overview

Planning travel today often involves wading through overwhelming amounts of information. Online travel agencies (OTAs) like Expedia, Kayak, and Google Travel offer countless options, but users still suffer from decision fatigue due to rigid filters and limited personalization.

Our project addresses this challenge with a data-driven Trip Recommender system that empowers users to ask simple, natural language questions like “Where can I go from Boston in April for under $1500?” and receive contextual, tailored travel recommendations. The application interprets the user’s query using GPT-4 and translates it into a precise SQL query, considering constraints like budget, climate, safety, lodging costs, and visa requirements.

---

## Deliverables

- [**Final Technical Report**](https://www.overleaf.com/read/qxxdhcfswcdv#ee741e)  
- [**Final Presentation Slides**](https://docs.google.com/presentation/d/1HwGILmvC6zpBUzfZ58Yq7H0yq7zYspyp0qVOfqlfz5Y/edit?usp=sharing)

---

## File Structure

* Trip_Recommender_Application/
  * [Data_Files/](/Data_Files)                  --All intermediate datasets and raw data sources
    * (e.g., Destination.csv, Lodging.csv, climate_data.csv)
  * Web/                          --Core application logic and interface
    * [app.py](/web/app.py)                      --Main Flask application
    * [model.py](/web/model.py)                    --Business logic and recommendation engine
    * [trip_recommender.db](/web/trip_recommender.db)         --SQLite database
    * [trip_recommender.sql](/web/trip_recommender.sql)        --SQL schema for database setup
    * [template/](/web/template)                  --HTML templates
      * [system.html](/web/template/system.html)
  * README.md                     --Project overview and instructions

---

## Key Features

- **Conversational Querying**: Transforms natural language questions into SQL using OpenAI's GPT-4.
- **Smart Filtering**: Applies contextual constraints including:
  - Budget & time constraints
  - Temperature & weather preferences
  - Visa and safety considerations
- **Data-Rich Backend**: Integrates:
  - NASA POWER API (10 years of weather data)
  - Numbeo Cost of Living indices
  - Custom datasets (visa, lodging, metadata)
  - 598,302 precomputed distances via Haversine
- **Interactive UI**: Displays both the natural language answer and SQL query transparently.

---

## Methodology

### Data Challenges & Decisions

Despite initial attempts to use APIs like Amadeus for hotel data and Wikitravel for destination metadata, both services proved unreliable. Amadeus’s free tier frequently timed out and suffered from rate limits, while Wikitravel explicitly forbids scraping and has no API. Due to these limitations and our tight timeline, we shifted to generating synthetic lodging and destination descriptions using GPT-4. This decision allowed us to fill schema gaps without violating terms of service or stalling development.

### Literature Review

Our system builds on work from both academia and industry:
- OTAs like Expedia and Google Travel have started integrating LLM-based assistants but still lack deep personalization [1][2].
- Research shows hybrid models (collaborative + content-based) outperform static filters [3].
- GPT-based text-to-SQL has emerged as a powerful tool for building conversational recommender systems [4][5].

> Full references included in our [final report](https://www.overleaf.com/read/qxxdhcfswcdv#ee741e).

---

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, Bootstrap 5
- **Database:** SQLite
- **NLP:** OpenAI GPT-4
- **Core Libraries:** `pandas`, `requests`, `concurrent.futures`, `sqlalchemy`

---

## System Pipeline

1. **User Query** (e.g., "cheap destinations from NYC for March")
2. **Text-to-SQL via GPT-4**  
3. **SQL Executed on trip_recommender.db**
4. **Result Translated Back to Human-Readable Response**
5. **Displayed on Web App**

Example output:

> “Here are some affordable destinations you can visit from NYC in March: 1. Jacksonville – warm and budget-friendly, 2. San Antonio – great food and walkable downtown…”

---

## Future Enhancements

- Real-time pricing and booking integration (e.g., Skyscanner API)
- User login and saved trips
- Interactive map of suggested destinations
- Voice input and mobile-friendly interface
- Machine learning-based personalization

---

## Contact

- **John Creighton** – creighton.jo@northeastern.edu  
- **Yuandi Tang** – tang.yuand@northeastern.edu
