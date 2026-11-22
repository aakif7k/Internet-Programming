# Exp-46-Phone-Bill-Payment: Online Phone Bill Payment System

## 1. Experiment Overview
- **Experiment No:** 46
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Online telecommunications billing and payment platform with monthly billing duration, last date overdue fine calculation (Rs. 10/day), flexible full/custom amount payments, and receipt generator.

## 3. Key Actors & System Roles
- **Telecom Customer**
- **Telecom Billing Admin**

## 4. Implemented Features
- Customer registration, login, and telecom account dashboard (Mobile Number, Plan Details)
- Monthly billing period tracking (Billing Start Date, End Date, Due Date)
- Outstanding bill breakdown: plan rental, data add-ons, roaming, and previous balance
- Late Fine Calculation: automatically computes Rs. 10 per day fine for payments after the due date
- Flexible payment modes: Pay Full Outstanding Bill or Enter Custom Partial Amount
- Multi-channel payment options (Credit/Debit Card, Net Banking, UPI, Mobile Wallets)
- Instant payment confirmation with digital transaction receipt and simulated email delivery
- Billing history ledger and recurring payment autopay configuration
- Admin portal: update monthly billing cycle dates, manage tariff plans, inspect subscriber payment logs

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
