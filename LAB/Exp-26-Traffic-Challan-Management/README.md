# Exp-26-Traffic-Challan-Management: Traffic Squad - E-Challan & Penalty Management

## 1. Experiment Overview
- **Experiment No:** 26
- **Course Title:** Internet Programming Lab
- **Category:** Portals & Management
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Traffic police e-challan enforcement portal enabling officers to issue violation cases with photographic evidence, allowing citizens to search and pay fines online, with live traffic advisory updates.

## 3. Key Actors & System Roles
- **Citizen Vehicle Owner**
- **Traffic Police Officer**
- **Admin**

## 4. Implemented Features
- Citizen portal: lookup e-Challans by vehicle registration number or challan ID
- View violation details: date, time, location, rule broken, fine penalty amount, and officer photo proof
- Secure online fine payment gateway with digital payment receipt generation
- Police Officer portal: authenticate badge ID, access traffic rules handbook with predefined fines
- Create violation case: enter vehicle plate, select violation rule, upload photographic proof, generate instant e-Challan
- Live traffic advisory module: post road closures, accident alerts, and traffic congestion map links
- Admin portal: police officer credentials management, daily fine collection audit reports

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
