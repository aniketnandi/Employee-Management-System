# Employee-Management-System
My undergrad project originally done using php and mysql, now revamped, modernized, and production grade.

Project overview & features - A full-stack Employee Management System built with **FastAPI**, **React**, and **PostgreSQL** (via Docker).  
Provides secure authentication, employee data management, and an intuitive frontend dashboard.

**Project Features**
- User Authentication (JWT-based login)
- View Employee Details (name, email, role, department, etc.)
- Add / Edit / Delete Employees (backend API)
- Search & Filter Employees
- Responsive React Frontend
- PostgreSQL Database (containerized with Docker)
- FastAPI Interactive API Docs at `/docs`

**Tech stack**
1) Frontend:
- React + Vite
- Axios for API requests
- TailwindCSS for styling

2) Backend:
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication

3) DevOps:
- Docker & Docker Compose

**Local run (Docker Compose) steps**
```
1️) Clone the Repository
bash
git clone https://github.com/aniketnandi/Employee-Management-System.git
cd Employee-Management-System

2) Create .env Files
Backend .env (example):-
DATABASE_URL=postgresql://postgres:postgres@db:5432/employees
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256

Frontend .env (example):-
VITE_API_URL=http://localhost:8000/api/v1

3) Start the Application
docker compose up --build

Backend will be at: http://localhost:8000
Frontend will be at: http://localhost:5173
```

**Screenshots (login, employees)**

<img width="561" height="252" alt="image" src="https://github.com/user-attachments/assets/4a153356-a612-4c42-ac1f-f7f00a2307c8" />
<img width="463" height="317" alt="image" src="https://github.com/user-attachments/assets/5d54a2f2-db09-4cac-84d7-c929581cad07" />

API docs link (/docs)

Live demo (when you deploy)
