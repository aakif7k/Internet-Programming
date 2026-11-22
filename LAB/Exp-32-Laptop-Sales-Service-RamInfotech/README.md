# Exp-32-Laptop-Sales-Service-RamInfotech: Ram Infotech - Laptop Sales & Service Portal

## 1. Experiment Overview
- **Experiment No:** 32
- **Course Title:** Internet Programming Lab
- **Category:** E-Commerce & Marketplaces
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Dual laptop sales and service management system featuring detailed model specs, service repair booking & ticket tracking, laptop rental agreement generator, and shop stock inventory control.

## 3. Key Actors & System Roles
- **Customer**
- **Service Technician**
- **Store Admin**

## 4. Implemented Features
- Online Laptop Store: filter laptops by brand (Dell, HP, Lenovo, Apple), processor, RAM, graphics, and price
- Laptop specifications modal with high-res photos and purchase checkout
- Service Center module: schedule laptop repair, specify fault symptoms (Screen, Motherboard, Battery, OS), and receive Service Ticket ID
- Real-time Service Status Tracker: check repair progress (Diagnosing, Waiting for Parts, Repaired, Ready for Pickup)
- Laptop Rental Agreement generator: select rental period, configuration, security deposit, and generate printable lease contract
- Admin Stock & Service Dashboard: track hardware stock in shop, manage pending repairs, assign technician tasks

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
