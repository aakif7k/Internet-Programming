# Exp-16-Grievance-Redressal-ComplainEase: ComplainEase - Grievance Redressal System

## 1. Experiment Overview
- **Experiment No:** 16
- **Course Title:** Internet Programming Lab
- **Category:** Portals & Management
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Online public grievance filing platform with category classification, interactive map pin location marking, proof-of-work status updates by municipal officers, and full administrative governance.

## 3. Key Actors & System Roles
- **Citizen User**
- **Municipal Officer**
- **System Admin**

## 4. Implemented Features
- Citizen registration & login
- Submit complaint form with category (Roads, Water, Sanitation, Electricity, Garbage), detailed description, and interactive map coordinate pin
- Real-time grievance tracking with status timeline (Submitted, Under Review, In Progress, Resolved)
- Citizen feedback submission on resolved complaints
- Officer portal: view assigned ward complaints, update resolution status, upload photo proof-of-work
- Admin control panel: generate credentials for officers, manage department accounts, view system reports, configure feature visibility

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
