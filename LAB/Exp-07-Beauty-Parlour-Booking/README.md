# Exp-07-Beauty-Parlour-Booking: Beauty Parlour Appointment Booking System

## 1. Experiment Overview
- **Experiment No:** 7
- **Course Title:** Internet Programming Lab
- **Category:** Booking & Reservations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Online appointment system for beauty salons featuring service catalog, stylist profiles, interactive reservation calendar with lockout hours, partial deposit or full payment (Stripe/PayPal), and salon manager dashboard.

## 3. Key Actors & System Roles
- **Customer**
- **Salon Manager / Stylist**

## 4. Implemented Features
- Browse salon services (Hair Styling, Facial & Cleanup, Bridal Makeup, Spa & Wellness)
- Stylist profiles with experience, specialty, and ratings
- Interactive reservation calendar: select date, available time slots, and lockout of booked hours
- Payment options: Full payment or partial deposit via simulated Stripe / PayPal
- Automatic booking confirmation and appointment reminders
- Customer personal account: view upcoming reservations, booking history, reschedule/cancel
- Salon manager dashboard: reservations calendar, add/edit bookings, stylist shift management
- Customer feedback and service review module

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, cart updates, and administrative modifications).
