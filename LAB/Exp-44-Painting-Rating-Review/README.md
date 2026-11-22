# Exp-44-Painting-Rating-Review: Painting Rating & Review Platform

## 1. Experiment Overview
- **Experiment No:** 44
- **Course Title:** Internet Programming Lab
- **Category:** Portfolios, Blogs & Content
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Art review platform where admin uploads paintings under scheduled packages, painting owners track audience critiques, and customers rate paintings 1 to 5 stars with positive and negative sentiment analysis.

## 3. Key Actors & System Roles
- **Art Customer**
- **Painting Owner / Artist**
- **Art Admin**

## 4. Implemented Features
- Customer authenticated login via simulated social media or email ID
- Painting display gallery showcasing active exhibited artwork with title, artist, medium, and description
- Interactive 5-Star Rating System and structured feedback submission (Positive highlights and constructive critique)
- Real-time dynamic calculation of average star rating and positive/negative sentiment summary percentages
- Painting Owner portal: register painting, select exhibition package duration (days), complete package fee payment, and inspect reviews analytics
- Admin dashboard: upload new scheduled paintings, review historical feedback before cycling artworks, manage package pricing

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
