# Exp-04-Train-Reservation: Online Train Reservation System

## 1. Experiment Overview
- **Experiment No:** 4
- **Course Title:** Internet Programming Lab
- **Category:** Booking & Reservations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Comprehensive railway reservation portal with route/class search, real-time seat availability, PNR generation, PNR status tracker (CNF/RAC/WL), ticket printing, cancellation with refund rules, and admin train master management.

## 3. Key Actors & System Roles
- **Passenger**
- **Railway Administrator**

## 4. Implemented Features
- Passenger login and registration with journey details
- Train search by origin, destination, date, and travel class (1A, 2A, 3A, SL, CC)
- Available train list with route via-details and live seat quotas
- Online / offline payment mode simulation
- Unique 10-digit PNR generation upon booking confirmation
- PNR Status inquiry (Confirmed, RAC, Waiting List)
- Cancellation module with refund rules (date of reservation, ticket fare, refundable %)
- Printable e-Ticket with passenger list and QR code
- Admin dashboard: add/update train details, zone/class/date fare management, view payment records

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser or host via local web server.
2. Use the top navigation role switcher to toggle between system roles: Passenger, Railway Administrator.
3. Test key workflows such as searching, form submissions, real-time calculations, status updates, and interactive views.
