# Event-Reservation

[![Django CI](https://github.com/Mamajin/Event-Reservation/actions/workflows/django.yml/badge.svg)](https://github.com/Mamajin/Event-Reservation/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/Mamajin/Event-Reservation/graph/badge.svg?token=UNKZKHCFVV)](https://codecov.io/gh/Mamajin/Event-Reservation)

Welcome to the Event Reservation System! This web application allows users to create, manage, and participate in various events. 
The project is built using Django for the backend and React for the frontend, aiming to provide a practical solution for event discovery, registration, and feedback.

## Table of Contents
- Project Overview
- Features
- Technologies Used
- Installation
- Demo Users
- Usage
- API Documentation
- Project Documents
  
## Project Overview
This application is developed as part of the Individual Software Process course at Kasetsart University. The Event Reservation System focuses on providing features for event management and participant engagement, emphasizing the creation of a functional and accessible web application.

## Features
- **User Authentication**: Secure login and registration for users.
- **Event Management**: Organizers can create, edit, and delete events.
- **Event Discovery**: Users can search for and view available events.
  
## Technologies Used
- **Frontend**: React, Tailwind CSS, DaisyUI, Axios
- **Backend**: Django, Django Ninja, SQLite
- **Tools and Libraries**: Vite (for React development), JWT (for authentication)
  
## Installation
### Prerequisites
- Node.js and npm (for the React frontend)
- Python and Django (for the backend)
- SQLite

### Backend Setup

**1. Clone the Repository:**
```bash
git clone https://github.com/Mamajin/Event-Reservation.git
cd Event-Reservation
```

**2. Install dependencies and load data:**
```bash
pip install -r requirements.txt
```

**3. Load data:**
```bash
py backend/manage.py loaddata data/data.json
```

**4. Navigate to the backend directory and create a virtual environment:**
```bash
cd backend
python -m venv venv
```

**5. Activate the virtual environment:**
```bash
# On Windows
venv\Scripts\activate

# On macOS and Linux
source venv/bin/activate
```

**6. Run the migrations and start the development server:**
```bash
python manage.py migrate
python manage.py runserver
```
### Frontend Setup

**1. Navigate to the frontend directory:**
```bash
cd ../frontend
```

**2. Copy sample.env file into .env file:**
```bash
cp sample.env .env
```

**3. Install dependencies and start the development server:**
```bash
npm install
npm run dev
```
## Demo Users

### User

| Username | Password  |
|----------|-----------|
| demo1    | hackme11  |
| demo2    | hackme22  |
| demo3    | hackme33  |

### Organizer

| Username     | Password     |
|--------------|--------------|
| organizer1   | organizer11  |
| organizer2   | organizer22  |
| organizer3   | organizer33  |

Use these credentials to log in the application.

## Usage
1. **Access the app**: Open http://localhost:5173 in your web browser.
2. **Register/Login**: Create a new account or log in with your credentials.
3. **Create Events**: If you are an organizer, you can create and manage events.

## API Documentation
The backend is built using Django Ninja, which provides a structured approach to API development. Key endpoints include:

- **POST** `/api/users/register/` - User registration
- **POST** `/api/users/login/` - User login
- **GET** `/api/events/events/` - Retrieve a list of events
- **POST** `/api/events/create-events` - Create a new event (for organizers)

For detailed API documentation, refer to [API Documentation](../../wiki/API-Documentation).

## Project Documents
For detailed documentation on the Event Reservation System, please refer to the [Project Wiki](../../wiki/Home). This Wiki includes:

- [Vision and Scope](../../wiki/Vision%20and%20Scope): Overview of the project's goals and purpose.
- [Requirements](../../wiki/Requirements): A comprehensive list of functional and non-functional requirements.
- [Project Development Plan](../../wiki/Project%20Development%20Plan): A detailed plan outlining the project's development phases and schedule.
- [User Stories](../../wiki/User%20Stories): Descriptions of how different users will interact with the system.
- [Domain Model](../../wiki/Domain%20Model): Represents the domain and its concepts in a visual format.
- [Style Guide](../../wiki/Style%20Guide): Guidelines for maintaining consistent visual design across the application.
