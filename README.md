# Health Information System

A comprehensive health information system for managing clients and health programs/services. This system allows healthcare providers to register clients, create health programs, and enroll clients in multiple health programs.

## Features

- **User Authentication**: Secure login and signup process for healthcare providers
- **Client Management**: Register, search, and update client information
- **Health Program Management**: Create and manage health programs (e.g., TB, Malaria, HIV)
- **Client Enrollment**: Enroll clients in one or more health programs
- **Client Search**: Find clients by name from the registered client list
- **Client Profile**: View detailed client information including enrolled programs
- **RESTful API**: Expose client profile information through RESTful APIs for external system integration
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technologies Used

- **Backend**: Django 5.2
- **API**: Django REST Framework
- **Frontend**: Tailwind CSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Installation and Setup

### Prerequisites
- Python 3.10+
- Node.js and npm (for Tailwind CSS)
- Git

### Clone the repository
```bash
git clone https://github.com/kahenyamercy/Health-Info-System.git
cd Health-Info-System
```

### Set up a virtual environment
```bash
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:****
source venv/bin/activate
```

### Install dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Tailwind CSS dependencies
python manage.py tailwind install
```

### Apply migrations
```bash
python manage.py migrate
```

### Create a superuser (admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin user
```

### Running the development server
```bash
# Run the Django development server
python manage.py runserver

# In a separate terminal, compile Tailwind CSS (optional, for development)
python manage.py tailwind start
```