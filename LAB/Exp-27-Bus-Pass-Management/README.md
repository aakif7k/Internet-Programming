# Exp-27-Bus-Pass-Management: Bus Pass Management System with QR Code

## 1. Experiment Overview
- **Experiment No:** 27
- **Course Title:** Internet Programming Lab
- **Category:** Portals & Management
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Digital bus pass issuing system with student concession passes (free for govt schools) and route employee passes, monthly renewal with e-wallet deduction, dynamic QR Code pass generation, and conductor verification scanner.

## 3. Key Actors & System Roles
- **Passenger / Student**
- **Transport Admin**
- **Bus Conductor**

## 4. Implemented Features
- User registration, login, and commuter profile
- Apply for Student Pass: input educational institution, upload photo ID, select validity (government school student free pass option)
- Apply for Route Bus Pass: input employer details, source and destination bus stops, route number
- e-Wallet system: add funds and buy single trip bus e-Tickets
- Monthly pass renewal workflow with automatic e-wallet balance deduction
- Dynamic QR Code pass generation containing encrypted pass ID, holder photo, route, and expiration date
- Bus Conductor portal: interactive QR scanner / Pass ID validator to verify pass authenticity, check route stops, and log bus location

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
