# Exp-03-Bus-Ticket-Booking: Online Bus Ticket Booking System

## 1. Experiment Overview
- **Experiment No:** 3
- **Course Title:** Internet Programming Lab
- **Category:** Booking & Reservations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Online bus ticketing platform with route search, seat selection grid, passenger info, payment gateway, bus categories (Volvo, Sleeper, Coach), passenger review/comments, and admin bus & report management.

## 3. Key Actors & System Roles
- **Passenger User**
- **Bus Administrator**

## 4. Implemented Features
- User authentication (Login, Register, Forgot Password)
- Search buses by source, destination, date, and departure time
- Bus categories: Volvo Multi-Axle, AC Sleeper, Semi-Sleeper, Luxury Coach
- Interactive 32-seat layout with booked/available/selected states
- Passenger details form & fare calculation with tax
- Simulated secure payment gateway with instant booking confirmation
- Cancel booking ticket module with refund calculation
- User review and comments section for individual bus routes
- Admin bus schedule & category management (add/update bus, photo, route, seats)
- Admin analytics and booking revenue report generation

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser or host via local web server.
2. Use the top navigation role switcher to toggle between system roles: Passenger User, Bus Administrator.
3. Test key workflows such as searching, form submissions, real-time calculations, status updates, and interactive views.
