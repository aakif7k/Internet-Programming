# Exp-45-Income-Tax-Calculation: Income Tax Calculation Web Application

## 1. Experiment Overview
- **Experiment No:** 45
- **Course Title:** Internet Programming Lab
- **Category:** Utilities & Calculations
- **Status:** Completed & Fully Functional

## 2. Problem Statement
Income tax calculation system implementing exact government tax formulas and slabs: Gross Pay, HRA, Standard Deduction (Rs. 50,000), Pension (capped at Rs. 150,000), Health Insurance, with slab tax rates and report download.

## 3. Key Actors & System Roles
- **Salaried Employee**
- **Tax Admin**

## 4. Implemented Features
- Employee authenticated login (simulated Google / Corporate credentials)
- Financial Details Input Form: Monthly Gross Pay, Monthly House Rent Allowance (HRA), Annual Pension contribution, Annual Health Insurance premium (Sec 80D)
- Exact Net Taxable Income Calculation Formula strictly implemented:
-   Net Taxable Income = (Gross Pay * 12) - (HRA * 12) - 50,000 [Standard Deduction] - min(Pension * 12, 150,000) - (Health Insurance * 12)
- Exact Government Tax Slabs Computation strictly implemented:
-   * If Net Taxable Income <= Rs. 500,000: Tax = Rs. 0 (Nil)
-   * If Net Taxable Income > Rs. 500,000:
-       - Up to Rs. 250,000: Rs. 0
-       - Rs. 250,001 to Rs. 500,000: 5% of (Net - 250,000)
-       - Rs. 500,001 to Rs. 1,000,000: Rs. 12,500 + 20% of (Net - 500,000)
-       - Above Rs. 1,000,000: Rs. 112,500 + 30% of (Net - 1,000,000)
- Itemized tax breakdown display: Total Gross, Total Deductions, Net Taxable Income, Slab-wise Tax Liability, Net Take-Home Salary
- Personalized Tax-Saving Recommendations and Printable Tax Computation Statement
- Admin portal: configure statutory deduction limits and tax slab threshold parameters

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
