# Exp-17-E-Voting-VoteOnline: VoteOnline - Secure E-Voting Platform

## 1. Experiment Overview
- **Experiment No:** 17
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Secure and transparent e-voting platform featuring Voter ID authentication, 2-factor OTP verification, candidate manifestos, one-person-one-vote cryptographic ballot casting, and real-time election results.

## 3. Key Actors & System Roles
- **Registered Voter**
- **Election Administrator**

## 4. Implemented Features
- Voter login using official Voter ID number
- Simulated Multi-Factor OTP verification sent to registered phone/email
- Interactive ballot interface: view candidate profiles, political party, and election manifestos
- Secure one-click vote casting with anti-double-voting prevention checks
- Instant digital voter confirmation receipt with encrypted vote token
- Admin dashboard: create election candidates, assign candidates to wards, import/manage voter roll
- Live election analytics: real-time vote count tallies, percentage turnout charts, and winning candidate declarations

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
