# Exp-02-Hotel-Room-Booking: Online Hotel Room Booking System

## 1. Experiment Overview
- **Experiment No:** 2
- **Course Title:** Internet Programming Lab
- **Category:** Booking & Reservations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Responsive hotel booking portal allowing users to search by destination, dates, and guests across 4 room types. Features strict 3-day cancellation/change policy enforcement, availability tracking, and admin dashboard for pricing and static page management.

## 3. Key Actors & System Roles
- **Customer User**
- **Hotel Administrator**

## 4. Implemented Features
- User registration, login, and profile modification
- Search by destination, check-in/out dates, and guest count
- 4 Room Types: Standard ($80/night), Deluxe ($120/night), Executive Suite ($200/night), Presidential Suite ($350/night)
- Real-time room availability checker
- Booking history dashboard with booking status
- Change booking or cancel booking with 3-day arrival policy check (strict date difference validation)
- Admin panel to manage room quantity and price for all 4 room types
- Admin booking management (modify or cancel any specific booking)
- Admin CMS to edit static pages: About Us, Room Info, Contact Us, Q&A, Travel Guide, Privacy Policy

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser or host via local web server.
2. Use the top navigation role switcher to toggle between system roles: Customer User, Hotel Administrator.
3. Test key workflows such as searching, form submissions, real-time calculations, status updates, and interactive views.
