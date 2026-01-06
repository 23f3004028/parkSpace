# 🚗 ParkSpace — Parking Lot Booking & Management System

ParkSpace is a **full‑stack parking lot management and booking system** that supports **admin and user roles**, real‑time slot availability, booking lifecycle management, analytics dashboards, and background task processing.

This project is an **improved and extended version** of an earlier parking lot management application, rebuilt to demonstrate stronger backend design, async processing, and a richer admin/user workflow.

---

## 📌 Project Purpose

The goal of ParkSpace is to model a **realistic parking system** similar to what is used in malls, offices, or gated communities:

* Users can discover parking lots, book spots, release them, and view history
* Admins can create and manage lots, spots, users, and view operational analytics
* Background jobs handle exports and scheduled notifications

This repository is intended for **learning and demonstration of real-world backend and system design concepts** rather than production deployment.

---

## ✨ Core Features

### 👤 User Features

* User registration & authentication
* View available parking lots in real time
* Book and release parking spots
* Automatic price calculation based on duration
* Booking history & summary dashboard
* CSV export of booking history (async via Celery)

### 🛠 Admin Features

* Admin‑only dashboard with role enforcement
* Create, update, and delete parking lots
* Dynamic spot creation & removal
* View all registered users
* Advanced search (by email, vehicle number, spot, location)
* Operational summary dashboard (users, bookings, occupancy)

---

## ⚙️ Backend Capabilities

* **Role‑Based Access Control (RBAC)** using Flask sessions
* **Relational data modeling** with SQLite and foreign keys
* **Background jobs** using Celery + Redis
* **Scheduled tasks** (daily reminders, monthly reports)
* **Server‑side caching** using Flask‑Caching (Redis)
* Clean separation of concerns using Flask Blueprints

---

## 🔄 Async & Scheduled Tasks

Implemented using **Celery + Redis**:

* Export user booking history as CSV and send via email (async)
* Daily reminder emails for inactive users
* Monthly activity reports for users

> Email sending is mocked/logged for development visibility.

---

## 🧱 Architecture Overview

```
backend/
├── controllers/        # Route handlers (admin, user, auth)
├── models/             # Database schema & initialization
├── tasks.py            # Celery background & scheduled jobs
├── extensions.py       # Cache & Celery setup
├── __init__.py         # App factory
└── main.py             # Entry point

frontend/
├── src/
│   ├── components/     # Admin & User Vue components
│   ├── router/         # Vue Router with role guards
│   └── main.js         # App bootstrap
└── index.html
```

---

## 🧰 Tech Stack

### Backend

* Python
* Flask (App Factory + Blueprints)
* SQLite
* Flask‑Login & Werkzeug Security
* Celery + Redis
* Flask‑Caching

### Frontend

* Vue.js 3
* Vue Router
* Axios
* Bootstrap 5
* Vite

---

## 🚀 Running the Project Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dharshancs/parking-lot-booking-system-v2.git
cd parking-lot-booking-system-v2
```

---

### 2️⃣ Prerequisites

* Python 3.9+
* Node.js 18+
* Redis (running locally)

---

### 3️⃣ Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

---

### 4️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

### 5️⃣ Redis & Celery (Optional but Recommended)

```bash
redis-server
celery -A backend.extensions.celery_app worker -B --loglevel=info
```

---

### 1️⃣ Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

---

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

### 3️⃣ Redis & Celery (Optional but Recommended)

```bash
redis-server
celery -A backend.extensions.celery_app worker -B --loglevel=info
```

---

## 🔐 Default Admin Credentials

```
Email: admin@admin.com
Password: admin
```

(Automatically seeded on first run)

---

## 📊 What This Project Demonstrates

* Full‑stack system design
* REST API design
* RBAC and session‑based auth
* Async processing and task queues
* Relational database modeling
* Frontend‑backend integration
* Time‑based pricing logic
* Realistic CRUD + analytics workflows

---

## 🧭 Relationship to Previous Project

This repository is an **evolution of an earlier parking lot management app**, with:

* Cleaner backend structure
* Admin analytics dashboards
* Async CSV exports
* Scheduled background jobs
* More complete user lifecycle handling

The earlier project is retained separately to show **progression**, while **this repo represents the more mature implementation**.

---

## 👨‍💻 Author

**Dharshan C S**
Aspiring Software Engineer

---

## 📄 License

This project is intended for **educational and portfolio use only**.
