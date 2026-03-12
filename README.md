# Personal Dashboard

A full‑stack web application for tracking daily habits, productivity,
and wellbeing metrics such as sleep, mood, energy, deep work, exercise,
and lifestyle habits.

This project was built as a learning exercise in modern **full‑stack
development** using **FastAPI** for the backend and **React (Vite)** for
the frontend.

------------------------------------------------------------------------

## Features

-   Create daily entries for personal metrics
-   Edit existing entries
-   Delete entries
-   View history of all entries
-   7‑day summary statistics
-   Input validation on both frontend and backend
-   User‑friendly error handling
-   Responsive dashboard layout
-   Habit tracking flags

Tracked metrics include:

-   Sleep hours
-   Mood (1--10)
-   Energy (1--10)
-   Deep work minutes
-   Exercise minutes
-   Stimulation minutes
-   Water intake
-   Notes
-   Habit flags (No porn, No smoking, No alcohol)

------------------------------------------------------------------------

## Tech Stack

### Backend

-   FastAPI
-   SQLAlchemy
-   Pydantic
-   SQLite

### Frontend

-   React
-   Vite
-   Fetch API
-   CSS

### Development Tools

-   Python virtual environment
-   Node.js / npm
-   Git

------------------------------------------------------------------------

## Project Structure

    personal-dashboard
    │
    ├── app
    │   ├── main.py          # FastAPI routes
    │   ├── models.py        # SQLAlchemy models
    │   ├── schemas.py       # Pydantic schemas
    │   ├── services.py      # Business logic & calculations
    │   └── db.py            # Database setup
    │
    ├── frontend
    │   ├── src
    │   │   ├── App.jsx
    │   │   ├── main.jsx
    │   │   └── App.css
    │   └── package.json
    │
    ├── data                 # SQLite database
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## API Endpoints

### Entries

    GET    /api/entries
    POST   /api/entries
    PATCH  /api/entries/{id}
    DELETE /api/entries/{id}

### Summary

    GET /api/summary

Returns aggregated statistics from the last 7 days.

------------------------------------------------------------------------

## Running the Project

### 1. Clone repository

    git clone https://github.com/yourusername/personal-dashboard.git
    cd personal-dashboard

------------------------------------------------------------------------

### 2. Backend Setup

Create virtual environment:

    python -m venv .venv

Activate:

Windows

    .venv\Scripts\activate

Linux / macOS

    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run backend:

    uvicorn app.main:app --reload

Backend runs on:

    http://127.0.0.1:8001

API documentation:

    http://127.0.0.1:8001/docs

------------------------------------------------------------------------

### 3. Frontend Setup

Navigate to frontend folder:

    cd frontend

Install dependencies:

    npm install

Run development server:

    npm run dev

Frontend runs on:

    http://localhost:5173

------------------------------------------------------------------------

## Example Dashboard Capabilities

### Entry creation

Users can log daily habits and productivity metrics.

### Entry editing

Entries can be updated while preserving historical data.

### Statistics

A summary endpoint aggregates the last 7 days of data:

-   Average sleep
-   Average mood
-   Average energy
-   Total deep work
-   Total exercise
-   Total stimulation
-   Average water intake

------------------------------------------------------------------------

## Validation

Validation is implemented on both layers.

### Backend (FastAPI / Pydantic)

-   mood must be between **1--10**
-   energy must be between **1--10**
-   numeric fields must be valid numbers

### Frontend

Basic validation prevents invalid requests before sending them to the
API.

------------------------------------------------------------------------

## Future Improvements

Potential future features:

-   Authentication system
-   Charts for habit trends
-   Mobile‑friendly UI
-   Data export
-   Multi‑user support

------------------------------------------------------------------------

## Motivation

This project was built to practice:

-   REST API design
-   frontend/backend communication
-   state management in React
-   data validation
-   CRUD operations
-   modular project structure

------------------------------------------------------------------------

## License

MIT License
