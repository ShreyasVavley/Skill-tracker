# 🏅 Skill & Certification Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38b2ac.svg)

A comprehensive, high-performance Database Management System (DBMS) project built to seamlessly track and manage professional skills and certifications. 

Featuring a blazing-fast **FastAPI** backend, robust **PostgreSQL** relational database, and a beautiful, minimalist **"Midnight Obsidian"** themed frontend dashboard.

---

## ✨ Key Features

- **Relational Database Schema**: Well-structured entities utilizing SQLAlchemy ORM mapping (`Users`, `Organizations`, `Certifications`, and a many-to-many `UserCertifications` junction table).
- **Comprehensive CRUD Interface**: Fully documented RESTful endpoints to manage all entities.
- **Advanced Renewal Alert Logic**: Specialized endpoints utilizing SQL `BETWEEN` operations to dynamically surface credentials expiring within 30 days.
- **Dynamic Stats Dashboard**: Real-time aggregation of active vs. expired certifications.
- **Premium User Interface**: A bespoke, responsive dark-mode frontend built with Tailwind CSS, emphasizing typography, spacing, and micro-animations.

---

## 🏗️ Architecture

```text
skill-tracker/
├── backend/
│   ├── main.py           # FastAPI application & REST routing
│   ├── database.py       # SQLAlchemy engine & session configuration
│   ├── models.py         # Database schema & entity definitions
│   ├── schemas.py        # Pydantic validation models
│   └── requirements.txt  # Python dependency manifest
├── frontend/
│   ├── index.html        # Single-page dashboard application
│   ├── style.css         # Custom CSS & scrollbar styling
│   └── script.js         # Asynchronous API integration logic
└── README.md
```

---

## 🚀 Getting Started

Follow these instructions to run the project in your local development environment.

### 1. Database Configuration
By default, the application is configured to connect to PostgreSQL. However, it will gracefully fall back to a local SQLite database for instant setup.
- **(Optional) PostgreSQL**: Set your connection string:
  ```bash
  export DATABASE_URL="postgresql://postgres:password@localhost:5432/skill_tracker"
  ```
  *(On Windows use `$env:DATABASE_URL="..."`)*

### 2. Backend Setup
Create a virtual environment and install dependencies:
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Server
Launch the FastAPI ASGI server using Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```

---

## 🌐 API Documentation & Usage

Once the server is running, the application serves the frontend and auto-generated API documentation on the same port:

- **Interactive Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger UI (API Docs)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc (Alternative Docs)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Testing the Renewal Logic
To test the advanced SQL query logic, add a certification to a user via the dashboard or API, setting the `expiry_date` within the next 30 days. Refresh the dashboard to see it trigger the alert feed automatically!

---

## 🛠️ CI/CD & Production Deployment
This repository is structured for streamlined CI/CD pipelines (e.g., GitHub Actions, Docker).
1. Isolate the `backend` folder as your build context.
2. Ensure `psycopg2-binary` is installed for PostgreSQL connectivity.
3. Serve with `uvicorn main:app --host 0.0.0.0 --port 80` in your production container.

---
*Built with ❤️ for elegant data management.*
