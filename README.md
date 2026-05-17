

# LifeLine — Blood Bank Management System

A web-based blood donor management system with admin dashboard, donor registration, and blood group search.

## Features

- **Donor Registration** — register donors with name, blood group, city, and contact
- **Blood Search** — search donors by name, blood group, or city
- **Admin Dashboard** — manage all donors with edit and delete
- **Secure Admin Login** — environment-based credentials
- **Live Donor Count** — real-time registered donor count on homepage

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MongoDB Atlas
- **Frontend:** HTML, Jinja2 templates
- **Containerization:** Docker

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

Create a `.env` file:

```
MONGO_URI=your_mongodb_atlas_uri
SECRET_KEY=your_secret_key
ADMIN_USER=your_admin_username
ADMIN_PASS=your_admin_password
```

## Running with Docker

```bash
docker-compose up
```

Then open `localhost:5000`

---


