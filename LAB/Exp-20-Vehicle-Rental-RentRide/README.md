# Exp-20-Vehicle-Rental-RentRide: RentRide - Modern Vehicle Rental Platform

## 1. Experiment Overview
- **Experiment No:** 20
- **Course Title:** Internet Programming Lab
- **Category:** Booking & Reservations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Vehicle rental platform offering a fleet of sedans, SUVs, and trucks with date-range rental booking, check-in forms with driver's license verification, booking history, and admin fleet management.

## 3. Key Actors & System Roles
- **Customer**
- **Rental Admin**

## 4. Implemented Features
- Customer registration, login, and user dashboard
- Search and filter vehicle fleet by vehicle type (Sedan, Compact SUV, Luxury, Pickup Truck), seating capacity, and transmission
- Vehicle details with daily rates, mileage allowance, and high-res photos
- Booking engine: select pickup and return dates, calculate total rental cost with insurance options
- Online check-in form submitting driver's license number and identification details
- Customer booking history with real-time reservation status
- Admin vehicle manager: add vehicle, update price, manage maintenance status
- Admin booking manager: approve or decline customer bookings, monitor vehicle utilization

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
