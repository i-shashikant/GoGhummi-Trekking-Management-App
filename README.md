# Trekking Management Application
# 🏔️ GoGhummi

**Discover Trails. Book Adventures.**

GoGhummi is a Trekking Management Web Application developed using Flask and SQLAlchemy as part of the IIT Madras BS Degree Program (MAD-1 Project). The application provides separate dashboards for Admins, Staff, and Users to efficiently manage trekking events, bookings, and participants.

---

## ✨ Features

### 👨‍💼 Admin
- Secure Login
- Dashboard with booking statistics
- Create, Update and Delete Treks
- Assign Staff to Treks
- Approve / Blacklist Staff
- Blacklist / Reactivate Users
- Search Treks, Staff and Users
- View all Bookings

### 🥾 Staff
- Dedicated Dashboard
- View Assigned Treks
- Manage Trek Status
- Update Trek Capacity
- View Participants
- Track Registered Users

### 🎒 User
- Register & Login
- Browse Treks
- Search and Filter Treks
- View Trek Details
- Book Treks
- Cancel Bookings
- View Booking History
- Manage Profile

---

## 🚀 Additional Features

- Role-Based Authentication
- Trek Capacity Management
- Automatic Slot Updates
- Glassmorphism UI
- Responsive Bootstrap 5 Design
- Search Functionality
- Status Badges
- Price Management
- Different Dashboard Backgrounds
- SQLAlchemy ORM with Relationships
- Flask Blueprints Architecture

---

## 🛠️ Tech Stack

### Backend
- Python 3
- Flask
- SQLAlchemy
- SQLite

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Jinja2
- Font Awesome

---

## 📂 Project Structure

```
GoGhummi/
│
├── app.py
├── config.py
├── models/
│   ├── user.py
│   ├── trek.py
│   └── booking.py
│
├── routes/
│   ├── auth.py
│   ├── admin.py
│   ├── staff.py
│   └── user.py
│
├── templates/
│   ├── admin/
│   ├── staff/
│   ├── user/
│   └── layouts/
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── utils/
│
├── requirements.txt
└── README.md
```

---

## 🗄️ Database

The application uses **SQLite** with **SQLAlchemy ORM**.

### Tables

- Users
- Treks
- Bookings

### Relationships

- One User → Many Bookings
- One Trek → Many Bookings
- One Staff → Many Assigned Treks

---

## 📸 Screenshots

> Add screenshots here before submission.

- Landing Page
- Login Page
- Admin Dashboard
- Staff Dashboard
- User Dashboard
- Browse Treks
- Trek Details
- Bookings Page

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://gitHub.com/i-shashikant/Trekking-Management-App
```

Move into the project

```bash
cd GoGhummi
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## 🎯 Future Enhancements

- Online Payment Gateway
- Email Notifications
- GPS Trail Maps
- Weather Integration
- Trek Reviews & Ratings
- Image Gallery
- QR Code Based Check-in
- Admin Analytics Dashboard

---

## 👨‍💻 Author

**Shashikant**

IIT Madras BS Degree Programme

MAD-I Project (2026)

---

## 📜 License

This project was developed for educational purposes as part of the IIT Madras BS Degree Programme.