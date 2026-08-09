# Trekking Management Application

A role-based web application for managing trekking activities, trek staff, trekkers, bookings, and trekking history.

## Features

### Admin
- Admin dashboard with statistics
- Create, edit, and delete treks
- Assign approved staff to treks
- Approve trek staff registrations
- Blacklist and unblacklist users and staff
- Search treks, users, and staff by name or ID
- View all bookings

### Trek Staff
- Staff registration and login
- Admin approval before dashboard access
- View assigned treks
- View registered participants
- Update available trek slots
- Update trek status
- Manage only assigned treks

### Trekker
- Trekker registration and login
- View open treks
- Search treks by name
- Filter treks by difficulty and location
- Book treks
- View booking status and trekking history
- Edit profile

### Booking Controls
- Prevent duplicate bookings
- Prevent overbooking
- Allow booking only for Open treks
- Automatically reduce available slots after booking

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-Login
- Flask-Bcrypt
- Jinja2
- HTML
- Bootstrap

## Project Structure

```text
trekking-management/
├── app.py
├── config.py
├── extensions.py
├── create_db.py
├── create_admin.py
├── requirements.txt
├── models/
├── routes/
├── templates/
└── static/