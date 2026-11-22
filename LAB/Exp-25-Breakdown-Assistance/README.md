# Exp-25-Breakdown-Assistance: On-Road Breakdown Assistance System

## 1. Experiment Overview
- **Experiment No:** 25
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Emergency road assistance platform connecting stranded drivers with nearby certified mechanics via GPS location simulation, breakdown service requests (tire, battery, towing), and mechanic rating reviews.

## 3. Key Actors & System Roles
- **Stranded Driver**
- **Licensed Mechanic**
- **System Admin**

## 4. Implemented Features
- Driver registration and vehicle details management
- Emergency SOS breakdown request: select vehicle issue (Flat Tire, Battery Jumpstart, Engine Overheating, Towing Service)
- Simulated GPS radar locating nearest licensed mechanics with distance and estimated time of arrival (ETA)
- Mechanic registration with trade license verification and admin approval workflow
- Mechanic portal: toggle online/offline availability, receive SOS dispatch requests, accept jobs, view customer location
- Real-time assistance status tracking for driver (Dispatched, En Route, Arrived, Completed)
- Post-service feedback, rating, and transparent billing summary

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
