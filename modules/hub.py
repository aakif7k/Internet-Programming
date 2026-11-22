# modules/hub.py - Generates LAB/index.html, LAB/README.md, and root README.md
import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generator_metadata import EXPERIMENTS

def generate_hub_html(base_dir="LAB"):
    cards_html = []
    for exp in EXPERIMENTS:
        num_str = f"{exp['num']:02d}"
        folder = exp['folder']
        title = exp['title']
        cat = exp['category']
        desc = exp['desc']
        roles = ", ".join(exp['roles'])
        
        card = f"""
        <div class="exp-card" data-category="{cat}" data-search="exp {exp['num']} {num_str} {title.lower()} {cat.lower()} {desc.lower()}">
          <div class="exp-card-header">
            <span class="exp-badge">Experiment {num_str}</span>
            <span class="badge badge-secondary">{cat}</span>
          </div>
          <div class="exp-card-body">
            <h3 class="exp-title">{title}</h3>
            <p class="exp-desc">{desc[:130]}...</p>
            <div class="exp-roles">
              <strong>Roles:</strong> {roles}
            </div>
          </div>
          <div class="exp-card-footer">
            <a href="./{folder}/index.html" class="btn btn-primary btn-sm btn-block">Launch Web App &rarr;</a>
            <a href="./{folder}/README.md" class="btn btn-outline btn-sm btn-block" style="margin-top:0.35rem;">Documentation</a>
          </div>
        </div>
        """
        cards_html.append(card)

    hub_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Internet Programming Lab Experiments Hub (46 Experiments)</title>
  <link rel="stylesheet" href="./assets/common.css">
  <style>
    .hub-hero {
      background: linear-gradient(135deg, #1e1b4b, #312e81, #1e293b);
      color: #fff;
      border-radius: var(--radius-lg);
      padding: 3rem 2rem;
      margin-bottom: 2.5rem;
      box-shadow: var(--shadow-lg);
      position: relative;
      overflow: hidden;
    }
    .hub-hero h1 {
      font-size: 2.4rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      margin-bottom: 0.75rem;
    }
    .hub-hero p {
      color: #cbd5e1;
      font-size: 1.1rem;
      max-width: 850px;
      line-height: 1.6;
    }
    .search-bar-container {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 1rem 1.5rem;
      margin-bottom: 2rem;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .filter-pills {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .filter-pill {
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: var(--radius-full);
      padding: 0.4rem 1rem;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: var(--transition);
    }
    .filter-pill:hover, .filter-pill.active {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }
    .exp-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.5rem;
    }
    .exp-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow-sm);
      transition: var(--transition);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .exp-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
      border-color: var(--border-focus);
    }
    .exp-card-header {
      padding: 1rem 1.25rem;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .exp-badge {
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--primary);
      background: var(--primary-light);
      padding: 0.25rem 0.6rem;
      border-radius: var(--radius-full);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .exp-card-body {
      padding: 1.25rem;
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    .exp-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.5rem;
      line-height: 1.35;
    }
    .exp-desc {
      font-size: 0.875rem;
      color: var(--text-muted);
      margin-bottom: 1rem;
      line-height: 1.5;
      flex: 1;
    }
    .exp-roles {
      font-size: 0.8rem;
      color: var(--text-light);
      background: var(--surface-2);
      padding: 0.5rem 0.75rem;
      border-radius: var(--radius-sm);
      margin-bottom: 0.5rem;
    }
    .exp-card-footer {
      padding: 0.85rem 1.25rem;
      border-top: 1px solid var(--border);
      background: #fafafa;
    }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <div class="lab-brand">
        <div class="lab-brand-icon">IP</div>
        <span>Internet Programming Laboratory</span>
      </div>
      <div class="lab-nav-actions">
        <span class="badge badge-success">46 Experiments Completed</span>
        <a href="../README.md" class="btn btn-outline btn-sm">Repo Readme</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="hub-hero">
        <h1>Internet Programming Lab Experiments</h1>
        <p>A comprehensive repository containing complete, production-grade interactive implementations of all 46 laboratory experiments from the engineering syllabus. Each project features dedicated role-based dashboards, realistic workflows, mathematical calculations, responsive layouts, and thorough documentation.</p>
        <div style="display:flex; gap:1.5rem; margin-top:1.5rem; flex-wrap:wrap;">
          <div><span style="font-size:1.6rem; font-weight:800;">46</span> <span style="font-size:0.9rem; color:#94a3b8;">Total Experiments</span></div>
          <div><span style="font-size:1.6rem; font-weight:800;">100%</span> <span style="font-size:0.9rem; color:#94a3b8;">Interactive Web Apps</span></div>
          <div><span style="font-size:1.6rem; font-weight:800;">0</span> <span style="font-size:0.9rem; color:#94a3b8;">External Dependencies</span></div>
        </div>
      </div>

      <!-- Search & Filters -->
      <div class="search-bar-container">
        <input type="text" id="hubSearchInput" class="form-control" style="font-size:1rem; padding:0.75rem 1rem;" placeholder="Search 46 experiments by title, category, keywords, or experiment number..." onkeyup="filterHub()">
        <div class="filter-pills" id="categoryFilterPills">
          <button class="filter-pill active" onclick="setCategoryFilter('All', this)">All (46)</button>
          <button class="filter-pill" onclick="setCategoryFilter('Booking & Reservations', this)">Booking & Reservations (9)</button>
          <button class="filter-pill" onclick="setCategoryFilter('E-Commerce & Marketplaces', this)">E-Commerce & Marketplaces (10)</button>
          <button class="filter-pill" onclick="setCategoryFilter('Portals & Management', this)">Portals & Management (12)</button>
          <button class="filter-pill" onclick="setCategoryFilter('Utilities & Calculations', this)">Utilities & Calculations (9)</button>
          <button class="filter-pill" onclick="setCategoryFilter('Portfolios, Blogs & Content', this)">Portfolios, Blogs & Content (6)</button>
        </div>
      </div>

      <!-- Experiments Grid -->
      <div class="exp-grid" id="experimentsGrid">
        {{CARDS_PLACEHOLDER}}
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab Experiments Hub &bull; Designed & Built for Academic Excellence</p>
    </div>
  </footer>

  <script src="./assets/common.js"></script>
  <script>
    let activeCategory = 'All';

    function setCategoryFilter(cat, btn) {
      activeCategory = cat;
      document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      filterHub();
    }

    function filterHub() {
      const q = document.getElementById('hubSearchInput').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.exp-card');
      let visibleCount = 0;

      cards.forEach(card => {
        const cardCat = card.getAttribute('data-category');
        const cardSearch = card.getAttribute('data-search');

        const matchesCat = activeCategory === 'All' || cardCat === activeCategory;
        const matchesQuery = !q || cardSearch.includes(q);

        if (matchesCat && matchesQuery) {
          card.style.display = 'flex';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });
    }
  </script>
</body>
</html>
"""
    hub_html = hub_template.replace("{{CARDS_PLACEHOLDER}}", "".join(cards_html))
    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)
    print("Generated LAB/index.html")

def generate_lab_readme(base_dir="LAB"):
    table_rows = []
    for exp in EXPERIMENTS:
        num_str = f"{exp['num']:02d}"
        folder = exp['folder']
        title = exp['title']
        cat = exp['category']
        roles = ", ".join(exp['roles'])
        row = f"| **{num_str}** | [{title}](./{folder}/) | {cat} | {roles} | [Launch App](./{folder}/index.html) &bull; [Manual](./{folder}/README.md) |"
        table_rows.append(row)

    lab_readme_content = f"""# Internet Programming - Laboratory Experiments Manual

Comprehensive academic laboratory portfolio comprising **46 complete, interactive web applications** designed for the **Internet Programming** (or Web Technology) Engineering curriculum.

---

## Laboratory Index & Table of Contents

| Exp # | Experiment Title | Category | Actors / Roles | Direct Links |
|:-----:|:-----------------|:---------|:---------------|:-------------|
{chr(10).join(table_rows)}

---

## Technical Highlights
1. **Zero Setup Overhead:** Pure vanilla HTML5, CSS3, and JavaScript (ES6+). Runs directly in any web browser (`file://`) or via local web server without requiring external build pipelines or `npm install`.
2. **Standard Modern Design System:** Built with consistent responsive CSS Grid, Flexbox, custom design tokens, dark accents, badges, tabs, and toast notifications (`LAB/assets/common.css` & `LAB/assets/common.js`).
3. **Strict Formula Compliance:**
   - **Exp 42 (Electricity Bill):** Strictly computes both Domestic and Commercial multi-tier slab charges and bi-monthly late penalty of Rs. 10 per day.
   - **Exp 45 (Income Tax):** Strictly implements exact Net Taxable Income deduction rules (HRA, standard deduction Rs. 50,000, pension cap Rs. 1,50,000, 80D health insurance) and exact 4-tier slab rates with Nil tax below Rs. 5,00,000.
   - **Exp 02 (Hotel Booking):** Strict 3-day arrival policy check for cancellations/modifications.
   - **Exp 04 (Train Reservation):** Unique 10-digit PNR generation algorithm, PNR status tracking (CNF/RAC/WL), and tiered refund calculations.
4. **Interactive Laboratory Hub:** Explore and filter all 46 projects visually via [`LAB/index.html`](./index.html).
"""
    with open(os.path.join(base_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(lab_readme_content)
    print("Generated LAB/README.md")

def update_root_readme():
    root_content = f"""# Internet Programming - Complete Laboratory Repository

Welcome to the **Internet Programming** laboratory experiments repository. This repository houses **46 fully developed, interactive web applications** mapped directly to the engineering lab curriculum.

---

## Quick Navigation
- **Interactive Lab Experiments Hub:** Launch [`LAB/index.html`](./LAB/index.html) to interactively explore, search, and run all 46 applications.
- **Detailed Laboratory Manual:** Read [`LAB/README.md`](./LAB/README.md) for individual problem statements, objectives, and test case documentation.

---

## 46 Experiments Overview

| # | Title | Category | Launch Link |
|:-:|:------|:---------|:------------|
| 01 | Local Library Management System | Portals & Management | [Exp-01](./LAB/Exp-01-Library-Management/index.html) |
| 02 | Online Hotel Room Booking System | Booking & Reservations | [Exp-02](./LAB/Exp-02-Hotel-Room-Booking/index.html) |
| 03 | Online Bus Ticket Booking System | Booking & Reservations | [Exp-03](./LAB/Exp-03-Bus-Ticket-Booking/index.html) |
| 04 | Online Train Reservation System | Booking & Reservations | [Exp-04](./LAB/Exp-04-Train-Reservation/index.html) |
| 05 | Online Flight Reservation System | Booking & Reservations | [Exp-05](./LAB/Exp-05-Flight-Reservation/index.html) |
| 06 | Online Cake Ordering System | E-Commerce & Marketplaces | [Exp-06](./LAB/Exp-06-Cake-Ordering/index.html) |
| 07 | Beauty Parlour Appointment Booking System | Booking & Reservations | [Exp-07](./LAB/Exp-07-Beauty-Parlour-Booking/index.html) |
| 08 | MedCare Hospital Online Appointment Booking | Booking & Reservations | [Exp-08](./LAB/Exp-08-Hospital-Appointment-Booking/index.html) |
| 09 | TechSavvy - Electronics Shopping Platform | E-Commerce & Marketplaces | [Exp-09](./LAB/Exp-09-Electronic-Gadgets-Shopping/index.html) |
| 10 | StyleHub - Online Fashion Retailer | E-Commerce & Marketplaces | [Exp-10](./LAB/Exp-10-Fashion-Store-StyleHub/index.html) |
| 11 | Home Finder - Real Estate Platform | Portals & Management | [Exp-11](./LAB/Exp-11-Real-Estate-HomeFinder/index.html) |
| 12 | InsureEasy - Online Insurance Platform | Portals & Management | [Exp-12](./LAB/Exp-12-Insurance-Management-InsureEasy/index.html) |
| 13 | BlossomGifts - Flowers & Gifts Ordering | E-Commerce & Marketplaces | [Exp-13](./LAB/Exp-13-Flowers-Gifts-BlossomGifts/index.html) |
| 14 | ReNewMarket - Second-Hand Goods Marketplace | E-Commerce & Marketplaces | [Exp-14](./LAB/Exp-14-Second-Hand-Market-ReNewMarket/index.html) |
| 15 | EasyToll - Online Toll Payment System | Utilities & Calculations | [Exp-15](./LAB/Exp-15-Toll-Payment-EasyToll/index.html) |
| 16 | ComplainEase - Grievance Redressal System | Portals & Management | [Exp-16](./LAB/Exp-16-Grievance-Redressal-ComplainEase/index.html) |
| 17 | VoteOnline - Secure E-Voting Platform | Utilities & Calculations | [Exp-17](./LAB/Exp-17-E-Voting-VoteOnline/index.html) |
| 18 | AgriMart - Farmer Supplies Marketplace | E-Commerce & Marketplaces | [Exp-18](./LAB/Exp-18-AgriMart-Farmer-Market/index.html) |
| 19 | VetCare - Animal Healthcare Consultation | Utilities & Calculations | [Exp-19](./LAB/Exp-19-Animal-Healthcare-VetCare/index.html) |
| 20 | RentRide - Modern Vehicle Rental Platform | Booking & Reservations | [Exp-20](./LAB/Exp-20-Vehicle-Rental-RentRide/index.html) |
| 21 | JobPortal - Vacancy & Recruitment Platform | Portals & Management | [Exp-21](./LAB/Exp-21-Job-Portal-Vacancy/index.html) |
| 22 | Smart Solid Waste Management System | Portals & Management | [Exp-22](./LAB/Exp-22-Solid-Waste-Management/index.html) |
| 23 | Blood Management Information System | Portals & Management | [Exp-23](./LAB/Exp-23-Blood-Bank-Management/index.html) |
| 24 | Wanderlust Travels - Online Travel Agency | Booking & Reservations | [Exp-24](./LAB/Exp-24-Travel-Agency-Wanderlust/index.html) |
| 25 | On-Road Breakdown Assistance System | Utilities & Calculations | [Exp-25](./LAB/Exp-25-Breakdown-Assistance/index.html) |
| 26 | Traffic Squad - E-Challan & Penalty Management | Portals & Management | [Exp-26](./LAB/Exp-26-Traffic-Challan-Management/index.html) |
| 27 | Bus Pass Management System with QR Code | Portals & Management | [Exp-27](./LAB/Exp-27-Bus-Pass-Management/index.html) |
| 28 | ArtistryHub - Emily Harris Artist Portfolio | Portfolios, Blogs & Content | [Exp-28](./LAB/Exp-28-Artist-Portfolio-ArtistryHub/index.html) |
| 29 | TechCon - Event Landing & Registration Page | Portfolios, Blogs & Content | [Exp-29](./LAB/Exp-29-Event-Registration-Page/index.html) |
| 30 | IJSSE - Academic Journal Publishing Portal | Portals & Management | [Exp-30](./LAB/Exp-30-Academic-Journal-IJSSE/index.html) |
| 31 | Ko-Matha Smart Dairy Farm Management | E-Commerce & Marketplaces | [Exp-31](./LAB/Exp-31-Dairy-Farm-KoMatha/index.html) |
| 32 | Ram Infotech - Laptop Sales & Service Portal | E-Commerce & Marketplaces | [Exp-32](./LAB/Exp-32-Laptop-Sales-Service-RamInfotech/index.html) |
| 33 | KodaikanalEats - Restaurant & Resort Booking | Booking & Reservations | [Exp-33](./LAB/Exp-33-Restaurant-Booking-KodaikanalEats/index.html) |
| 34 | LearnWell Tuition Centre Management System | Portals & Management | [Exp-34](./LAB/Exp-34-Tuition-Centre-LearnWell/index.html) |
| 35 | EduConnect - Interactive Teaching Platform | Portals & Management | [Exp-35](./LAB/Exp-35-Online-Teaching-EduConnect/index.html) |
| 36 | BookHaven - Online Bookstore | E-Commerce & Marketplaces | [Exp-36](./LAB/Exp-36-Bookstore-BookHaven/index.html) |
| 37 | MyProfessionalShowcase - Portfolio & Resume | Portfolios, Blogs & Content | [Exp-37](./LAB/Exp-37-Professional-Showcase-Portfolio/index.html) |
| 38 | Gourmet Haven - Fine Dining Restaurant | Portfolios, Blogs & Content | [Exp-38](./LAB/Exp-38-Fine-Dining-GourmetHaven/index.html) |
| 39 | TechStore - Clean Product Catalog & Cart | E-Commerce & Marketplaces | [Exp-39](./LAB/Exp-39-Product-Catalog-Cart/index.html) |
| 40 | Travel Explorer - Interactive Travel Blog | Portfolios, Blogs & Content | [Exp-40](./LAB/Exp-40-Travel-Blog-Interactive-Map/index.html) |
| 41 | CulinaryDelight - Digital Recipe Book | Portfolios, Blogs & Content | [Exp-41](./LAB/Exp-41-Digital-Recipe-Book/index.html) |
| 42 | Online Electricity Bill Payment System | Utilities & Calculations | [Exp-42](./LAB/Exp-42-Electricity-Bill-Payment/index.html) |
| 43 | Online Placement Examination System | Utilities & Calculations | [Exp-43](./LAB/Exp-43-Online-Placement-Exam/index.html) |
| 44 | Painting Rating and Review Web Application | Portfolios, Blogs & Content | [Exp-44](./LAB/Exp-44-Painting-Rating-Review/index.html) |
| 45 | Income Tax Calculation Web Application | Utilities & Calculations | [Exp-45](./LAB/Exp-45-Income-Tax-Calculation/index.html) |
| 46 | Online Phone Bill Payment System | Utilities & Calculations | [Exp-46](./LAB/Exp-46-Phone-Bill-Payment/index.html) |

---

## How to Run
Simply open any experiment's `index.html` file or launch [`LAB/index.html`](./LAB/index.html) directly in your favorite browser (Chrome, Edge, Firefox, Safari) or serve via any static HTTP server (e.g. `python -m http.server 8000`).
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(root_content)
    print("Updated root README.md")

if __name__ == "__main__":
    generate_hub_html("LAB")
    generate_lab_readme("LAB")
    update_root_readme()
