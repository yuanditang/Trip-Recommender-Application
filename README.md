# 🌍 Trip Recommender Application

**Team Members:**  
- John Creighton  
- Yuandi Tang  

**Course:** DS5110 - Summer 2025  
**Instructor:** Professor Nafa  
**Date:** June 2, 2025  

---

## 📌 Project Overview

The **Trip Recommender Application** helps users discover personalized travel destinations based on preferences such as budget, climate, trip duration, and origin city. It leverages real-time APIs, a custom-built recommendation engine, and a user-friendly interface to generate curated travel suggestions.

---

## 🚀 Features

- **Real-Time Data Integration:**  
  Weather, cost of living, attractions, and more

- **Smart Recommendation Engine:**  
  Matches user preferences with destination data

- **Custom Database:**  
  Efficient storage and retrieval of API data

- **User-Friendly Interface:**  
  Web UI for inputs and travel suggestions

---

## 🛠️ Technologies Used

- **Languages:** Python, JavaScript, HTML/CSS  
- **Frameworks & Libraries:** Flask, SQLAlchemy, Bootstrap  
- **Database:** PostgreSQL / SQLite  
- **APIs:** OpenWeatherMap, Numbeo, Travel Advisor, others

---

## 📅 Project Timeline (8 Weeks)

| Week | Deliverables                                               |
|------|------------------------------------------------------------|
| 1    | Define requirements, finalize tech stack & API shortlist   |
| 2    | Design and initialize database schema                      |
| 3    | Build backend API integration; pull/store real-time data   |
| 4    | Begin logic for recommendation system                      |
| 5    | Develop frontend UI; link user input forms                 |
| 6    | Integrate UI, backend, and recommendation logic            |
| 7    | Conduct full testing; debug; polish UI                     |
| 8    | Final presentation, documentation, and deployment          |

---

## 📤 Work Distribution

### John Creighton
- API research & integration
- Database schema design
- Recommendation engine core logic
- Input validation

### Yuandi Tang
- Database implementation & optimization
- UI development and integration
- Recommendation system refinement
- Frontend-backend linking

---

## 📋 Project Planning & Management

### 1. Project Kickoff
- **Goals:** Create a functional, user-friendly trip recommendation app based on real-time destination data and user preferences.
- **Scope Definition:** Focus only on core features (data retrieval, UI, logic). Exclude advanced ML, account systems, or booking features.
- **Phase Deliverables:** APIs selected → DB schema built → Logic implemented → UI integrated → Testing and final delivery
- **Milestones:** Aligned to 8-week timeline above
- **Team Capabilities:** Adequate for MVP. Minor upskilling needed for front-end frameworks and API optimization.
- **Dataset Availability:** No static dataset; real-time API data will be pulled and stored dynamically.

### 2. Team Discussions
- **Core Skills:**
  - John: Data modeling, backend development, logic design
  - Yuandi: Front-end design, integration, performance optimization
- **Missing Skills:** None critical; slight gap in front-end polish (addressed with Bootstrap)
- **Tool Experience:** Python, Flask, Git, basic SQL; need familiarity with React/Bootstrap
- **Language/Platform Choice:** Python (Flask), SQLAlchemy, Bootstrap or plain HTML/CSS

### 3. Skills & Tools Assessment
- **External Resources:** Rely on course mentors and documentation
- **Best-Suited Tools:** Flask, PostgreSQL, requests, SQLAlchemy, Bootstrap
- **Tool Comfort:** Shared documentation and setup sessions will ensure alignment
- **Role Assignments:** Tasks distributed by individual strengths (see Work Distribution above)

### 4. Initial Setup
- **Environment:** Python virtualenv, GitHub repo, API keys configured
- **Version Control:** GitHub repo with branches for dev, features
- **Libraries Installed:** Flask, SQLAlchemy, requests, dotenv
- **Testing:** API response validation, DB test inserts, UI rendering
- **Troubleshooting Plan:** Use logs, debug mode, and shared setup doc

### 5. Progress Review
- **Achievements:** Repo setup, APIs researched, DB schema drafted
- **Issues:** Some APIs have limits or missing data (workarounds planned)
- **Team Contributions:** Balanced as expected
- **Timeline Check:** On track
- **Objective Alignment:** MVP features being implemented within scope

### 6. Plan Revision
- **Timeline Adjustments:** Add buffer before Week 8 for UI testing
- **Task Reassignments:** Assist where needed on integration and testing
- **Next Steps:** Focused check-ins weekly; assign goals per sprint
- **Communication:** Slack (daily), GitHub Issues (task tracking), weekly summary doc
- **Progress Tracking:** GitHub Projects / Kanban board with milestones

---

## 📂 Repository Structure
Here’s your project directory structure in Markdown format for direct inclusion in your README.md file, complete with code block formatting and descriptive comments:

## 📁 Project Directory Structure
Here’s your project directory structure in Markdown format for direct inclusion in your README.md file, complete with code block formatting and descriptive comments:

## 📁 Project Directory Structure

trip-recommender/
│
├── backend/                # Flask server & APIs
│   ├── api/                # API data retrieval
│   ├── recommendation/     # Recommendation logic
│   └── db/                 # Database models and utilities
│
├── frontend/               # Static files and templates
│   ├── templates/          # HTML files
│   └── static/             # CSS and JS
│
├── docs/                   # Proposal, planning, documentation
├── tests/                  # Unit and integration tests
└── README.md               # Project overview and planning



Let me know if you’d like to generate a live GitHub Pages version of the documentation or a downloadable README.md file!


---

## 🧪 Future Enhancements

- Machine learning for smarter recommendations
- User login and saved trip preferences
- Travel route optimization and booking integrations
- Social features for group trip planning

---

## 📫 Contact

- John Creighton – [creighton.jo@northeastern.edu]  
- Yuandi Tang – [tang.yuand@northeastern.edu]
