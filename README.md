# Tutoring Booking System

## Project Description
This project is a web-based Tutoring Booking System that allows users to browse available tutors, schedule sessions, and complete payments either online or offline.  
It includes user authentication (OAuth2), booking management, payment integration, and administrative functionalities.  
The system follows MVC / REST API architecture and uses RabbitMQ for asynchronous processing of notifications and payment updates.

## Main Features

### Student
- User registration & login via OAuth2
- Browse tutors by subject (Math, Programming, Languages)
- Book tutoring sessions
- Make online or offline payments
- View booking history and status
- Receive notifications about bookings and payments

### Admin
- Manage tutors (add/edit/delete)
- View all bookings
- Approve offline payments
- Monitor payment statuses

### System
- REST API / MVC architecture
- Asynchronous tasks with RabbitMQ
- Automated unit & integration tests (≥50% coverage)

## Tech Stack
- Backend: Python (Flask)
- Database: PostgreSQL / SQLite
- Authentication: OAuth2 (Google)
- Payment Gateway: Stripe (sandbox)
- Queue: RabbitMQ
- Frontend: HTML + Bootstrap
- Testing: PyTest

## Installation & Setup
1. Clone the repository:
```bash
git clone https://orkan.tu.kielce.pl/gitlab/ISE_TutoringBooking/tutoring-booking-system.git
 