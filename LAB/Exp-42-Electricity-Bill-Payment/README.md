# Exp-42-Electricity-Bill-Payment: Online Electricity Bill Payment System

## 1. Experiment Overview
- **Experiment No:** 42
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Online electricity bill calculation and payment system implementing exact domestic and commercial tariff slabs, bi-monthly billing cycles, late payment fine calculation (Rs. 10/day), and receipt generator.

## 3. Key Actors & System Roles
- **Electricity Consumer**
- **Board Billing Admin**

## 4. Implemented Features
- Consumer registration, login, and connection profile (Consumer Number, Meter ID)
- Exact Tariff Calculation Engine implemented strictly per norms:
-   * Domestic Connection: First 100 units @ Rs. 1.00/unit | 101-200 units @ Rs. 2.50/unit | 201-500 units @ Rs. 4.00/unit | >500 units @ Rs. 6.00/unit
-   * Commercial Connection: First 100 units @ Rs. 2.00/unit | 101-200 units @ Rs. 4.50/unit | 201-500 units @ Rs. 6.00/unit | >500 units @ Rs. 7.00/unit
- Bi-monthly billing period cycle (start date, end date, last date of payment)
- Late Fine Calculator: automatically applies Rs. 10 per day fine for payments made after the last date
- Bill breakdown display: energy charges by slab, fixed charges, late fine, and net payable amount
- Multi-method payment gateway (Credit Card, Debit Card, Net Banking, UPI, Digital Wallet)
- Downloadable & printable official EB Payment Receipt with transaction reference
- Admin portal: update tariff slab rates, modify billing cycle dates, inspect consumer payment records

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
