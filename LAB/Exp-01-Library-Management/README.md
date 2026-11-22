# Exp-01-Library-Management: Local Library Management System

## 1. Experiment Overview
- **Experiment No:** 1
- **Course Title:** Internet Programming Lab
- **Category:** Portals & Management
- **Status:** Completed & Fully Functional

## 2. Problem Statement
A streamlined library system with catalog search, user accounts for borrowing and managing books, librarian admin dashboard for inventory, issuing/returning books, fine calculation (Rs. 5/day), and semester-wise study material downloads.

## 3. Key Actors & System Roles
- **Librarian Admin**
- **Student User**

## 4. Implemented Features
- Librarian Admin login & dashboard
- Add, update, and delete books from catalog
- Issue book to student with issue & return dates
- Return book status & automatic overdue fine calculation
- Semester & year-wise study material upload & management
- Student registration & login
- Book catalog search & real-time availability check
- My Borrow History (issue date, expiry date, return status)
- Check & pay overdue fines
- Search & download academic study materials by year/semester
- Student profile management

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser or host via local web server.
2. Use the top navigation role switcher to toggle between system roles: Librarian Admin, Student User.
3. Test key workflows such as searching, form submissions, real-time calculations, status updates, and interactive views.
