# Exp-15-Toll-Payment-EasyToll: EasyToll - Online Toll Payment System

## 1. Experiment Overview
- **Experiment No:** 15
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Advanced toll management system allowing drivers to recharge e-Wallets, buy advance toll e-Tickets, apply for monthly toll passes with QR Codes, and enable toll booth operators to scan & verify passes instantly.

## 3. Key Actors & System Roles
- **Driver User**
- **Toll Booth Officer**
- **Toll Admin**

## 4. Implemented Features
- Driver registration, login, and vehicle plate registration
- e-Wallet balance management with instant add-money simulation
- Buy advance single/return toll e-Tickets to skip toll booth queues
- Apply for new monthly toll pass & renew existing toll passes
- Dynamic QR Code generation for vehicle toll passes
- Toll Gate Operator interface: QR Code scanner / Pass ID verifier, check ticket validity, update toll gate location
- Admin portal: approve toll passes, manage toll booth logins, create toll gates & rate slabs, inspect transaction ledger

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
