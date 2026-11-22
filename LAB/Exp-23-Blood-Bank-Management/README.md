# Exp-23-Blood-Bank-Management: Blood Management Information System

## 1. Experiment Overview
- **Experiment No:** 23
- **Course Title:** Internet Programming Lab
- **Category:** Portals & Management
- **Status:** Completed & Fully Functional

## 2. Problem Statement
National blood donor registry and hospital inventory system facilitating rapid donor discovery, real-time blood bank stock tracking (A, B, AB, O +/-), and emergency hospital blood requisition management.

## 3. Key Actors & System Roles
- **Blood Donor / User**
- **Hospital & Blood Bank Admin**

## 4. Implemented Features
- Donor registration with blood group (A+, A-, B+, B-, AB+, AB-, O+, O-), contact, city, and last donation date
- Donor dashboard: update donor availability status, view personal donation history, eligibility check
- Public donor search: filter verified donors by required blood group and city
- Hospital portal: register blood bank, manage available blood units inventory matrix
- Emergency blood request broadcast module with urgent SMS/call indicator
- Hospital blood stock reports: safe reserves monitoring, expired blood unit tracking
- Confidential medical records management and donor health screening checklist

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
