# Exp-43-Online-Placement-Exam: Online Placement Examination System

## 1. Experiment Overview
- **Experiment No:** 43
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Online placement examination platform featuring admin exam scheduling & question bank, candidate timed test interface with countdown timer, automatic evaluation, scorecard generation, and merit rank list.

## 3. Key Actors & System Roles
- **Candidate Student**
- **Placement Exam Admin**

## 4. Implemented Features
- Candidate login with allotted roll number and exam schedule verification
- Admin portal: exam scheduling (date, time, duration), question bank upload (MCQs covering Quantitative Aptitude, Logical Reasoning, and Technical Coding)
- Candidate Examination Interface: real-time countdown timer, question navigator palette (Answered, Marked for Review, Not Visited)
- Automatic instant answer evaluation and scoring upon test submission or timer expiry
- Comprehensive Candidate Scorecard: sectional breakdown, accuracy percentage, time taken, and pass/fail outcome
- Placement Merit List & Ranking: dynamic leaderboard showing passed candidates ranked by highest score
- Online Re-evaluation / Review request submission module

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
