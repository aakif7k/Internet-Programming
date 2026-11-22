# Exp-19-Animal-Healthcare-VetCare: VetCare - Animal Healthcare Consultation

## 1. Experiment Overview
- **Experiment No:** 19
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Tele-veterinary platform where farmers upload animal illness symptoms (text, images, audio/video links) for diagnosis. Features free Govt CVH vs paid private clinic consultations with payment integration and disease analytics.

## 3. Key Actors & System Roles
- **Farmer / Pet Owner**
- **Veterinary Doctor**

## 4. Implemented Features
- Farmer registration and profile management
- Post animal medical case: select livestock type (Cattle, Sheep, Poultry, Pets), describe symptoms, and attach images or media links
- Choose consultation tier: Free Govt. CVH clinic or Private specialist with payment gateway (Bank Transfer / EasyPaisa simulation)
- Doctor portal: review patient complaints, inspect symptom photos, and issue clinical prescriptions and diet instructions
- Farmer prescription viewer & treatment history
- Epidemiological analytics dashboard: regional heat-map of prevalent animal diseases based on submitted cases
- Doctor directory, veterinary news & disease prevention guides

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
