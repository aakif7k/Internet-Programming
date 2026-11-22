# Exp-22-Solid-Waste-Management: Smart Solid Waste Management System

## 1. Experiment Overview
- **Experiment No:** 22
- **Course Title:** Internet Programming Lab
- **Category:** Portals & Management
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Smart municipal waste management platform tracking sensor-monitored garbage bins, calculating optimal truck collection routes to dumping sites, logging driver loads, and processing public overflow complaints.

## 3. Key Actors & System Roles
- **Municipal Administrator**
- **Sanitation Truck Driver**
- **General Public**

## 4. Implemented Features
- Admin dashboard: interactive smart bin map with live fill-level percentages (0-100%) and segregation categories (Organic, Recyclable, Hazardous)
- Automated optimal collection route algorithm simulating best route through overflowing bins to the final dumping site
- Driver management and route assignment module
- Driver portal: view daily assigned collection route, update bin collection status, log collected garbage load (kg)
- General public portal: submit overflowing bin complaints with street address and photo proof
- Admin analytics: daily waste collection reports, driver efficiency stats, and resolved citizen complaints

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
