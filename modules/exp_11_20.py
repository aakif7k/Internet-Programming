# modules/exp_11_20.py
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generator_metadata import EXPERIMENTS

def write_exp_readme(exp_dir, exp):
    content = f"""# {exp['folder']}: {exp['title']}

## 1. Experiment Overview
- **Experiment No:** {exp['num']}
- **Course Title:** Internet Programming Lab
- **Category:** {exp['category']}
- **Status:** Completed & Fully Functional

## 2. Problem Statement
{exp['desc']}

## 3. Key Actors & System Roles
{chr(10).join(f"- **{role}**" for role in exp['roles'])}

## 4. Implemented Features
{chr(10).join(f"- {feat}" for feat in exp['features'])}

## 5. Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Design System:** Responsive CSS Grid & Flexbox, Custom Design Tokens (`../assets/common.css`)
- **Interactive Logic:** Vanilla JavaScript (`../assets/common.js`), LocalStorage persistence, Dynamic DOM manipulation
- **Compatibility:** Standard modern browsers (Chrome, Firefox, Safari, Edge)

## 6. How to Run & Test
1. Open `index.html` in any web browser.
2. Toggle between system roles using the tabbed navigation.
3. Perform end-to-end interactions (searches, bookings, calculations, and administrative actions).
"""
    with open(os.path.join(exp_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)

def generate_exp_11(base_dir):
    exp = EXPERIMENTS[10]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 11: Home Finder - Real Estate Platform</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .prop-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .prop-img { height:160px; background:linear-gradient(135deg, #059669, #10b981); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127969;</div>
        <span>Home Finder Real Estate</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 11</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Home Finder - Real Estate Platform</h1>
        <p class="lab-hero-desc">Discover residential & commercial properties with saved search criteria, interactive neighborhood map view, built-in mortgage EMI calculator, and viewing scheduler.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="searchTab">&#128269; Property Search</button>
        <button class="tab-btn" data-tab="emiTab">&#128200; Mortgage EMI Calculator</button>
        <button class="tab-btn" data-tab="scheduleTab">&#128197; Schedule Viewing</button>
        <button class="tab-btn" data-tab="agentTab">&#128188; Agent & Admin Portal</button>
      </div>

      <!-- Search Tab -->
      <div id="searchTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-4">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Location / City</label>
                <input type="text" id="propLoc" class="form-control" value="Chennai">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Property Type</label>
                <select id="propType" class="form-select" onchange="renderProps()">
                  <option value="All">All Types</option>
                  <option value="Apartment">Apartment / Flat</option>
                  <option value="Villa">Luxury Villa</option>
                  <option value="Commercial">Commercial Office</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Bedrooms (BHK)</label>
                <select id="propBhk" class="form-select" onchange="renderProps()">
                  <option value="All">Any BHK</option>
                  <option value="2 BHK">2 BHK</option>
                  <option value="3 BHK">3 BHK</option>
                  <option value="4 BHK">4 BHK</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Max Price ($)</label>
                <input type="number" id="propMaxPrice" class="form-control" value="600000" oninput="renderProps()">
              </div>
            </div>
            <div style="margin-top:1rem; display:flex; justify-content:space-between; align-items:center;">
              <button class="btn btn-sm btn-outline" onclick="saveSearchCriteria()">&#128190; Save Search Criteria</button>
              <span id="savedCritLabel" style="font-size:0.85rem; color:var(--text-muted);">No criteria saved yet.</span>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="propGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- EMI Calculator Tab -->
      <div id="emiTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Mortgage & Home Loan EMI Calculator</div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">Home Loan Amount ($)</label>
              <input type="number" id="emiLoan" class="form-control" value="300000" oninput="calculateEMI()">
            </div>
            <div class="grid grid-2">
              <div class="form-group">
                <label class="form-label">Annual Interest Rate (%)</label>
                <input type="number" id="emiRate" class="form-control" value="8.5" step="0.1" oninput="calculateEMI()">
              </div>
              <div class="form-group">
                <label class="form-label">Tenure (Years)</label>
                <input type="number" id="emiTenure" class="form-control" value="20" oninput="calculateEMI()">
              </div>
            </div>
            <div style="padding:1.5rem; background:var(--surface-2); border-radius:var(--radius); text-align:center;">
              <div style="font-size:0.9rem; color:var(--text-muted);">Monthly Mortgage Payment (EMI):</div>
              <div style="font-size:2.2rem; font-weight:800; color:var(--primary);" id="emiResult">$2,603 / mo</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Schedule Viewing Tab -->
      <div id="scheduleTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Schedule an In-Person Property Tour</div>
          <div class="card-body">
            <form onsubmit="handleSchedule(event)">
              <div class="form-group">
                <label class="form-label">Select Property</label>
                <select id="schProp" class="form-select">
                  <option>Emerald Heights 3 BHK - $280,000</option>
                  <option>Palazio Lakefront Villa 4 BHK - $540,000</option>
                  <option>CyberTech Business Park Office - $450,000</option>
                </select>
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Preferred Date</label>
                  <input type="date" id="schDate" class="form-control" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Preferred Time Slot</label>
                  <select id="schTime" class="form-select">
                    <option>10:00 AM - 11:30 AM</option>
                    <option>02:00 PM - 03:30 PM</option>
                    <option>05:00 PM - 06:30 PM</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Your Contact Phone / Email</label>
                <input type="text" id="schContact" class="form-control" value="+91 9876543210" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Confirm Appointment</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Agent Tab -->
      <div id="agentTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Real Estate Agent Directory & Listing Admin</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">Verified real estate brokers and listings database.</p>
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Agent Name</th>
                    <th>Agency</th>
                    <th>Verified Phone</th>
                    <th>Active Listings</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Rajesh Kumar</td>
                    <td>Prime Properties</td>
                    <td>+91 98401 23456</td>
                    <td><span class="badge badge-success">14 Active</span></td>
                  </tr>
                  <tr>
                    <td>Pooja Sundaram</td>
                    <td>Metro Real Estate</td>
                    <td>+91 97910 87654</td>
                    <td><span class="badge badge-success">8 Active</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-11: Home Finder Real Estate Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let properties = [
      { id: 1, title: "Emerald Heights Apartment", type: "Apartment", bhk: "3 BHK", loc: "OMR, Chennai", price: 280000, size: "1,650 sq.ft", icon: "&#127970;" },
      { id: 2, title: "Palazio Lakefront Villa", type: "Villa", bhk: "4 BHK", loc: "ECR, Chennai", price: 540000, size: "3,200 sq.ft", icon: "&#127969;" },
      { id: 3, title: "Greenfield Cozy Flat", type: "Apartment", bhk: "2 BHK", loc: "Velachery, Chennai", price: 160000, size: "1,050 sq.ft", icon: "&#127970;" },
      { id: 4, title: "CyberTech Business Hub", type: "Commercial", bhk: "Any BHK", loc: "Guindy, Chennai", price: 450000, size: "2,800 sq.ft", icon: "&#127970;" }
    ];

    function renderProps() {
      const grid = document.getElementById('propGrid');
      const t = document.getElementById('propType').value;
      const b = document.getElementById('propBhk').value;
      const maxP = parseFloat(document.getElementById('propMaxPrice').value) || 9999999;
      grid.innerHTML = '';

      const filtered = properties.filter(p => {
        return (t === 'All' || p.type === t) &&
               (b === 'All' || p.bhk === b) &&
               p.price <= maxP;
      });

      filtered.forEach(p => {
        const c = document.createElement('div');
        c.className = 'prop-card';
        c.innerHTML = `
          <div class="prop-img">${p.icon}</div>
          <div style="padding:1.25rem; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <h4 style="margin:0;">${p.title}</h4>
                <span class="badge badge-primary">${p.bhk}</span>
              </div>
              <div style="font-size:0.85rem; color:var(--text-muted); margin:0.35rem 0;">&#128205; ${p.loc} &bull; ${p.size}</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1rem;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${p.price.toLocaleString()}</span>
              <button class="btn btn-sm btn-primary" onclick="alertSchedule('${p.title}')">Tour Property</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function calculateEMI() {
      const P = parseFloat(document.getElementById('emiLoan').value);
      const r = (parseFloat(document.getElementById('emiRate').value) / 12) / 100;
      const n = parseFloat(document.getElementById('emiTenure').value) * 12;
      const emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
      document.getElementById('emiResult').textContent = '$' + Math.round(emi).toLocaleString() + ' / mo';
    }

    function saveSearchCriteria() {
      const t = document.getElementById('propType').value;
      const b = document.getElementById('propBhk').value;
      const p = document.getElementById('propMaxPrice').value;
      document.getElementById('savedCritLabel').innerHTML = `<strong>Saved:</strong> ${t}, ${b}, < $${p}`;
      showToast('Search criteria saved for future visits!', 'success');
    }

    function alertSchedule(name) {
      showToast(`Selected "${name}" for viewing! Head to Schedule tab.`, 'info');
    }

    function handleSchedule(e) {
      e.preventDefault();
      showToast('Viewing appointment scheduled successfully with prime agent!', 'success');
      e.target.reset();
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('schDate').value = new Date(Date.now() + 3*24*60*60*1000).toISOString().split('T')[0];
      renderProps();
      calculateEMI();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-11")

def generate_exp_12(base_dir):
    exp = EXPERIMENTS[11]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 12: InsureEasy - Insurance Management Platform</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128737;</div>
        <span>InsureEasy Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 12</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">InsureEasy - Online Insurance Platform</h1>
        <p class="lab-hero-desc">Compare Health, Auto, and Home policies. Buy online, calculate premiums, file claims, manage customer accounts, and dispatch automated SMS renewal alerts via agents.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="compareTab">&#128269; Compare Policies</button>
        <button class="tab-btn" data-tab="claimsTab">&#128221; File a Claim</button>
        <button class="tab-btn" data-tab="agentTab">&#128188; Agent Dashboard & SMS Alert</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; System Admin</button>
      </div>

      <!-- Compare Tab -->
      <div id="compareTab" class="tab-pane active">
        <div class="grid grid-3" id="policyCards">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Claims Tab -->
      <div id="claimsTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Online Insurance Claim Submission</div>
          <div class="card-body">
            <form onsubmit="handleClaim(event)">
              <div class="form-group">
                <label class="form-label">Policy Number</label>
                <input type="text" id="clmPolicy" class="form-control" value="POL-HLTH-891" required>
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Incident Date</label>
                  <input type="date" id="clmDate" class="form-control" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Claim Amount ($)</label>
                  <input type="number" id="clmAmount" class="form-control" value="3500" required>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Incident Description & Proof Documents</label>
                <textarea class="form-control" rows="3" required placeholder="Describe accident/medical diagnosis details..."></textarea>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Submit Insurance Claim</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Agent Tab -->
      <div id="agentTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Manage Policyholders & Commissions</div>
            <div class="card-body" style="padding:0;">
              <div class="table-responsive" style="border:none;">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th>Customer</th>
                      <th>Policy</th>
                      <th>Due Date</th>
                      <th>Commission</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Aakif (Self)</td>
                      <td>Comprehensive Health Shield</td>
                      <td>2026-12-10</td>
                      <td>$45.00</td>
                    </tr>
                    <tr>
                      <td>Vikram R.</td>
                      <td>Zero-Dep Auto Protection</td>
                      <td>2026-11-28</td>
                      <td>$32.50</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Send Renewal SMS Alert to Customers</div>
            <div class="card-body">
              <div class="form-group">
                <label class="form-label">Customer Mobile Number</label>
                <input type="text" id="smsPhone" class="form-control" value="+91 9876543210">
              </div>
              <div class="form-group">
                <label class="form-label">SMS Alert Message</label>
                <textarea id="smsText" class="form-control" rows="3">Dear customer, your health policy POL-HLTH-891 premium of $350 is due on 2026-12-10. Pay before due date to avoid policy lapse.</textarea>
              </div>
              <button class="btn btn-secondary btn-block" onclick="sendSmsAlert()">Dispatch Automated SMS Alert</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Administrator: Agent Approvals & Performance</div>
          <div class="card-body">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Agent Name</th>
                    <th>Agency License</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Karthik Srinivasan</td>
                    <td>IRDA-AG-4902</td>
                    <td><span class="badge badge-success">Approved</span></td>
                    <td><button class="btn btn-sm btn-outline">Review Details</button></td>
                  </tr>
                  <tr>
                    <td>Deepa Narayanan</td>
                    <td>IRDA-AG-5104</td>
                    <td><span class="badge badge-warning">Pending Approval</span></td>
                    <td><button class="btn btn-sm btn-success" onclick="approveAgent(this)">Approve Agent</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-12: InsureEasy Insurance Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let policies = [
      { id: 1, name: "Comprehensive Health Shield", type: "Health", coverage: "$500,000", premium: 350, icon: "&#127973;" },
      { id: 2, name: "Zero-Dep Auto Protection", type: "Auto", coverage: "$40,000", premium: 240, icon: "&#128663;" },
      { id: 3, name: "Home Structure & Content Guard", type: "Home", coverage: "$300,000", premium: 180, icon: "&#127969;" }
    ];

    function renderPolicies() {
      const container = document.getElementById('policyCards');
      container.innerHTML = '';
      policies.forEach(p => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-header">
            <span>${p.name}</span>
            <span class="badge badge-primary">${p.type}</span>
          </div>
          <div class="card-body">
            <div style="font-size:2.5rem; text-align:center; margin-bottom:0.75rem;">${p.icon}</div>
            <div style="font-size:0.9rem; color:var(--text-muted); text-align:center; margin-bottom:0.75rem;">Total Sum Insured: <strong>${p.coverage}</strong></div>
            <div style="text-align:center; margin-bottom:1rem;">
              <span style="font-size:1.5rem; font-weight:800; color:var(--primary);">$${p.premium}</span>
              <span style="font-size:0.8rem; color:var(--text-muted);">/ year</span>
            </div>
            <button class="btn btn-sm btn-primary btn-block" onclick="buyPolicy('${p.name}', ${p.premium})">Buy Policy Online</button>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function buyPolicy(name, premium) {
      const polId = 'POL-' + Math.floor(1000 + Math.random() * 9000);
      showToast(`Policy ${polId} purchased for "${name}"! Premium: $${premium}/yr`, 'success');
    }

    function handleClaim(e) {
      e.preventDefault();
      showToast('Claim ticket logged! Case officer assigned for inspection.', 'success');
      e.target.reset();
    }

    function sendSmsAlert() {
      const phone = document.getElementById('smsPhone').value;
      showToast(`SMS alert successfully dispatched to ${phone}!`, 'success');
    }

    function approveAgent(btn) {
      btn.parentElement.previousElementSibling.innerHTML = '<span class="badge badge-success">Approved</span>';
      btn.remove();
      showToast('Agent approved successfully!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('clmDate').value = new Date().toISOString().split('T')[0];
      renderPolicies();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-12")

def generate_exp_13(base_dir):
    exp = EXPERIMENTS[12]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 13: BlossomGifts - Flowers & Gifts Ordering</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .flower-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .flower-img { height:150px; background:linear-gradient(135deg, #f43f5e, #fb7185); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127801;</div>
        <span>BlossomGifts Online Florist</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 13</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">BlossomGifts - Flowers & Gifts Ordering</h1>
        <p class="lab-hero-desc">Curated floral arrangements, gift hampers, and custom greeting messages. Multi-occasion catalog, delivery scheduling, cart, and florist admin inventory control.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="catalogTab">&#127801; Gifts Catalog</button>
        <button class="tab-btn" data-tab="cartTab">&#128722; Cart & Delivery Date</button>
        <button class="tab-btn" data-tab="adminTab">&#128188; Florist Admin</button>
      </div>

      <!-- Catalog Tab -->
      <div id="catalogTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Occasion</label>
                <select id="occSelect" class="form-select" onchange="renderGifts()">
                  <option value="All">All Occasions</option>
                  <option value="Birthday">Birthday Wishes</option>
                  <option value="Anniversary">Anniversary Romance</option>
                  <option value="Congratulations">Congratulations</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Recipient</label>
                <select id="recipSelect" class="form-select" onchange="renderGifts()">
                  <option value="All">Anyone</option>
                  <option value="Her">For Her</option>
                  <option value="Him">For Him</option>
                  <option value="Parents">For Parents</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Max Price (Rs.)</label>
                <input type="number" id="giftMaxPrice" class="form-control" value="2500" oninput="renderGifts()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="giftsGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Cart Tab -->
      <div id="cartTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Selected Hampers & Flowers</div>
            <div class="card-body" id="giftCartList">
              <!-- Populated by JS -->
            </div>
          </div>

          <div class="card">
            <div class="card-header">Custom Delivery & Greeting Message</div>
            <div class="card-body">
              <form onsubmit="handleGiftOrder(event)">
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Delivery Date</label>
                    <input type="date" id="giftDelDate" class="form-control" required>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Delivery Slot</label>
                    <select class="form-select">
                      <option>Morning (08:00 - 11:00 AM)</option>
                      <option>Afternoon (01:00 - 04:00 PM)</option>
                      <option>Evening (06:00 - 09:00 PM)</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Custom Greeting Card Message</label>
                  <textarea class="form-control" rows="3" placeholder="Write your heartfelt note here..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Send Gift Now</button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Florist Stock Inventory</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Manage fresh seasonal blooms, update bouquet prices, and track pending dispatches.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-13: BlossomGifts Flowers & Gifts Ordering</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let giftItems = [
      { id: 1, name: "Crimson Velvet 20-Rose Bouquet", occ: "Anniversary", recip: "Her", price: 1200, icon: "&#127801;" },
      { id: 2, name: "Sunshine Yellow Lilies & Ferrero", occ: "Birthday", recip: "Her", price: 1650, icon: "&#127803;" },
      { id: 3, name: "Gourmet Artisan Fruit & Nut Hamper", occ: "Congratulations", recip: "Parents", price: 1950, icon: "&#127873;" }
    ];

    let giftCart = [];

    function renderGifts() {
      const grid = document.getElementById('giftsGrid');
      const occ = document.getElementById('occSelect').value;
      const recip = document.getElementById('recipSelect').value;
      const maxP = parseFloat(document.getElementById('giftMaxPrice').value) || 99999;
      grid.innerHTML = '';

      const filtered = giftItems.filter(g => {
        return (occ === 'All' || g.occ === occ) &&
               (recip === 'All' || g.recip === recip) &&
               g.price <= maxP;
      });

      filtered.forEach(g => {
        const card = document.createElement('div');
        card.className = 'flower-card';
        card.innerHTML = `
          <div class="flower-img">${g.icon}</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <h4 style="margin:0;">${g.name}</h4>
              <span class="badge badge-primary">${g.occ}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Recipient: ${g.recip}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">Rs. ${g.price}</span>
              <button class="btn btn-sm btn-primary" onclick="addGiftToCart(${g.id})">Add Gift</button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function addGiftToCart(id) {
      const g = giftItems.find(item => item.id === id);
      giftCart.push(g);
      renderGiftCart();
      showToast(`Added ${g.name} to cart!`, 'success');
    }

    function renderGiftCart() {
      const list = document.getElementById('giftCartList');
      list.innerHTML = '';
      if (giftCart.length === 0) {
        list.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:1.5rem;">Cart is empty.</p>';
        return;
      }
      giftCart.forEach((item, idx) => {
        const div = document.createElement('div');
        div.style.padding = '0.75rem';
        div.style.borderBottom = '1px solid var(--border)';
        div.style.display = 'flex';
        div.style.justifyContent = 'space-between';
        div.style.alignItems = 'center';
        div.innerHTML = `
          <div>
            <strong>${item.name}</strong>
            <div style="font-size:0.8rem; color:var(--text-muted);">Rs. ${item.price}</div>
          </div>
          <button class="btn btn-sm btn-danger" onclick="removeGift(${idx})">&times;</button>
        `;
        list.appendChild(div);
      });
    }

    function removeGift(idx) {
      giftCart.splice(idx, 1);
      renderGiftCart();
    }

    function handleGiftOrder(e) {
      e.preventDefault();
      if (giftCart.length === 0) {
        showToast('Please add gifts to cart first!', 'danger');
        return;
      }
      showToast('Gift order scheduled with custom greetings!', 'success');
      giftCart = [];
      renderGiftCart();
      e.target.reset();
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('giftDelDate').value = new Date(Date.now() + 2*24*60*60*1000).toISOString().split('T')[0];
      renderGifts();
      renderGiftCart();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-13")

def generate_exp_14(base_dir):
    exp = EXPERIMENTS[13]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 14: ReNewMarket - Second-Hand Goods Marketplace</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .market-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .market-img { height:150px; background:linear-gradient(135deg, #6366f1, #8b5cf6); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#9851;</div>
        <span>ReNewMarket</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 14</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">ReNewMarket - Second-Hand Goods Marketplace</h1>
        <p class="lab-hero-desc">Sustainable peer-to-peer commerce for pre-loved Electronics, Furniture, and Books. List items, simulate direct price negotiations, and track shipment status (Shipped / Received).</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="browseTab">&#128717; Browse Pre-loved Items</button>
        <button class="tab-btn" data-tab="sellTab">&#128227; List an Item for Sale</button>
        <button class="tab-btn" data-tab="ordersTab">&#128230; Orders & Logistics</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Market Admin</button>
      </div>

      <!-- Browse Tab -->
      <div id="browseTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Category</label>
                <select id="mkCat" class="form-select" onchange="renderMarket()">
                  <option value="All">All Categories</option>
                  <option value="Electronics">Electronics</option>
                  <option value="Furniture">Furniture</option>
                  <option value="Books">Books</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Condition</label>
                <select id="mkCond" class="form-select" onchange="renderMarket()">
                  <option value="All">Any Condition</option>
                  <option value="Like New">Like New</option>
                  <option value="Good">Good</option>
                  <option value="Fair">Fair</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Search</label>
                <input type="text" id="mkSearch" class="form-control" placeholder="Search keywords..." onkeyup="renderMarket()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="marketGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Sell Tab -->
      <div id="sellTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Post a Pre-Loved Item for Sale</div>
          <div class="card-body">
            <form onsubmit="handlePostItem(event)">
              <div class="form-group">
                <label class="form-label">Item Title</label>
                <input type="text" id="postTitle" class="form-control" required placeholder="e.g. Ergonomic Office Mesh Chair">
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Category</label>
                  <select id="postCat" class="form-select">
                    <option>Electronics</option>
                    <option>Furniture</option>
                    <option>Books</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Condition</label>
                  <select id="postCond" class="form-select">
                    <option>Like New</option>
                    <option>Good</option>
                    <option>Fair</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Asking Price ($)</label>
                <input type="number" id="postPrice" class="form-control" value="85" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Publish Listing</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Orders Tab -->
      <div id="ordersTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Order Logistics Status (Shipped / Received)</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Order Ref</th>
                    <th>Item</th>
                    <th>Agreed Price</th>
                    <th>Logistics Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="marketOrdersTbody">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Admin User & Commodity Management</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Manage platform users, verify genuine pre-loved listings, and moderate category taxations.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-14: ReNewMarket Second-Hand Marketplace</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let marketItems = [
      { id: 1, title: "Kindle Paperwhite 10th Gen", cat: "Electronics", cond: "Like New", price: 65, icon: "&#128214;" },
      { id: 2, title: "Solid Wood Study Desk", cat: "Furniture", cond: "Good", price: 110, icon: "&#129681;" },
      { id: 3, title: "Complete Algorithm Design Manual", cat: "Books", cond: "Fair", price: 25, icon: "&#128218;" }
    ];

    let orders = [
      { id: "RNM-401", item: "Kindle Paperwhite 10th Gen", price: "$60", status: "Shipped" }
    ];

    function renderMarket() {
      const grid = document.getElementById('marketGrid');
      const cat = document.getElementById('mkCat').value;
      const cond = document.getElementById('mkCond').value;
      const q = document.getElementById('mkSearch').value.toLowerCase();
      grid.innerHTML = '';

      const filtered = marketItems.filter(m => {
        return (cat === 'All' || m.cat === cat) &&
               (cond === 'All' || m.cond === cond) &&
               m.title.toLowerCase().includes(q);
      });

      filtered.forEach(m => {
        const card = document.createElement('div');
        card.className = 'market-card';
        card.innerHTML = `
          <div class="market-img">${m.icon}</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <h4 style="margin:0;">${m.title}</h4>
              <span class="badge badge-primary">${m.cond}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Category: ${m.cat}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${m.price}</span>
              <div>
                <button class="btn btn-sm btn-outline" onclick="makeOffer('${m.title}', ${m.price})">Negotiate</button>
                <button class="btn btn-sm btn-primary" onclick="buyMarketItem(${m.id})">Buy</button>
              </div>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function makeOffer(title, currentPrice) {
      const offer = prompt(`Enter your counter-offer price for "${title}" (Listed: $${currentPrice}):`, currentPrice - 10);
      if (offer) {
        showToast(`Counter offer of $${offer} sent to seller for review!`, 'info');
      }
    }

    function buyMarketItem(id) {
      const m = marketItems.find(item => item.id === id);
      orders.push({
        id: 'RNM-' + Math.floor(100 + Math.random() * 900),
        item: m.title,
        price: '$' + m.price,
        status: "Processing"
      });
      renderOrders();
      showToast(`Purchase initiated for ${m.title}!`, 'success');
    }

    function renderOrders() {
      const tbody = document.getElementById('marketOrdersTbody');
      tbody.innerHTML = '';
      orders.forEach(o => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${o.id}</strong></td>
          <td>${o.item}</td>
          <td>${o.price}</td>
          <td><span class="badge ${o.status === 'Received' ? 'badge-success' : 'badge-primary'}">${o.status}</span></td>
          <td>
            <button class="btn btn-sm btn-outline" onclick="markReceived('${o.id}')" ${o.status === 'Received' ? 'disabled' : ''}>Mark Received</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function markReceived(id) {
      const o = orders.find(item => item.id === id);
      if (o) {
        o.status = "Received";
        renderOrders();
        showToast(`Order ${id} marked as Received!`, 'success');
      }
    }

    function handlePostItem(e) {
      e.preventDefault();
      const title = document.getElementById('postTitle').value;
      const cat = document.getElementById('postCat').value;
      const cond = document.getElementById('postCond').value;
      const price = parseFloat(document.getElementById('postPrice').value);
      marketItems.push({ id: Date.now(), title, cat, cond, price, icon: "&#9851;" });
      renderMarket();
      e.target.reset();
      showToast('Pre-loved item published to marketplace!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderMarket();
      renderOrders();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-14")

def generate_exp_15(base_dir):
    exp = EXPERIMENTS[14]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 15: EasyToll - Online Toll Payment System</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .qr-box { width:160px; height:160px; border:2px dashed var(--primary); border-radius:var(--radius); display:flex; flex-direction:column; align-items:center; justify-content:center; margin:0 auto; background:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128663;</div>
        <span>EasyToll FastPass</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 15</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">EasyToll - Online Toll Payment System</h1>
        <p class="lab-hero-desc">Skip toll booth queues: recharge your e-Wallet, buy advance toll e-Tickets, apply for QR-enabled monthly passes, and verify passes via Toll Gate Scanner interface.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="driverTab">&#128663; Driver e-Wallet & Passes</button>
        <button class="tab-btn" data-tab="boothTab">&#128247; Toll Gate Scanner</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Toll Administrator</button>
      </div>

      <!-- Driver Tab -->
      <div id="driverTab" class="tab-pane active">
        <div class="grid grid-3" style="margin-bottom:1.5rem;">
          <div class="stat-card">
            <div class="stat-icon">&#128179;</div>
            <div>
              <div class="stat-value" id="walletBalance">Rs. 850</div>
              <div class="stat-label">e-Wallet Balance</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#127915;</div>
            <div>
              <div class="stat-value">1 Active</div>
              <div class="stat-label">Monthly FastPass</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#9989;</div>
            <div>
              <div class="stat-value">TN-09-CB-4210</div>
              <div class="stat-label">Registered Vehicle Plate</div>
            </div>
          </div>
        </div>

        <div class="grid grid-2">
          <!-- Buy eTicket / Top up -->
          <div class="card">
            <div class="card-header">Buy Advance Toll e-Ticket / Top Up Wallet</div>
            <div class="card-body">
              <form onsubmit="handleBuyTicket(event)">
                <div class="form-group">
                  <label class="form-label">Select Toll Plaza</label>
                  <select id="tollPlaza" class="form-select">
                    <option value="85">Paranur Toll Plaza (Chengalpattu) - Rs. 85</option>
                    <option value="60">Athur Toll Plaza (Tindivanam) - Rs. 60</option>
                    <option value="110">Nemili Toll Plaza (Sriperumbudur) - Rs. 110</option>
                  </select>
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Journey Type</label>
                    <select id="tripType" class="form-select">
                      <option value="1">Single Journey</option>
                      <option value="1.5">Return (Within 24 Hours)</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Add Money to Wallet (Rs.)</label>
                    <input type="number" id="topupVal" class="form-control" value="500">
                  </div>
                </div>
                <div style="display:flex; gap:0.75rem;">
                  <button type="submit" class="btn btn-primary btn-block">Buy Advance e-Ticket</button>
                  <button type="button" class="btn btn-secondary" onclick="addMoney()">Add Funds</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Dynamic QR Pass -->
          <div class="card">
            <div class="card-header">Your Active Toll Pass QR Code</div>
            <div class="card-body" style="text-align:center;">
              <div class="qr-box">
                &#9638;&#9638;&#9638;
                <span style="font-size:0.8rem; font-weight:bold; color:var(--primary); margin-top:0.35rem;">SCAN PASS</span>
              </div>
              <div style="margin-top:1rem;">
                <h4>Pass ID: TOLL-TN-4210</h4>
                <div style="font-size:0.85rem; color:var(--text-muted);">Vehicle: Car / Jeep &bull; Valid till: 2026-12-31</div>
                <button class="btn btn-sm btn-outline" style="margin-top:0.75rem;" onclick="showToast('Pass renewed for 30 more days via wallet!', 'success')">Renew Monthly Pass (Rs. 1,200)</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Booth Scanner Tab -->
      <div id="boothTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Toll Gate Operator Scanner & Barrier Control</div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">Scan / Enter Toll Pass ID or Ticket Number</label>
              <div style="display:flex; gap:0.5rem;">
                <input type="text" id="scanInput" class="form-control" value="TOLL-TN-4210">
                <button class="btn btn-primary" onclick="verifyTollScan()">Verify</button>
              </div>
            </div>
            <div id="scanResult" style="margin-top:1.5rem; display:none; padding:1.25rem; background:var(--surface-2); border-radius:var(--radius);">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Toll Authority Management</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Configure toll rate slabs, inspect plaza daily collections, and monitor automated fast-tag lane clearances.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-15: EasyToll Online Toll Payment System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let balance = 850;

    function handleBuyTicket(e) {
      e.preventDefault();
      const base = parseFloat(document.getElementById('tollPlaza').value);
      const mult = parseFloat(document.getElementById('tripType').value);
      const cost = Math.round(base * mult);

      if (balance < cost) {
        showToast('Insufficient wallet balance! Please add funds.', 'danger');
        return;
      }
      balance -= cost;
      document.getElementById('walletBalance').textContent = 'Rs. ' + balance;
      const tNo = 'TKT-' + Math.floor(1000 + Math.random() * 9000);
      showToast(`e-Ticket ${tNo} purchased! Paid Rs. ${cost} from e-Wallet.`, 'success');
    }

    function addMoney() {
      const amt = parseFloat(document.getElementById('topupVal').value) || 0;
      if (amt <= 0) return;
      balance += amt;
      document.getElementById('walletBalance').textContent = 'Rs. ' + balance;
      showToast(`Rs. ${amt} added to e-Wallet successfully!`, 'success');
    }

    function verifyTollScan() {
      const q = document.getElementById('scanInput').value.trim();
      const res = document.getElementById('scanResult');
      res.style.display = 'block';
      if (q === "TOLL-TN-4210") {
        res.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <h4 style="margin:0; color:var(--success);">&#9989; VALID PASS VERIFIED</h4>
            <span class="badge badge-success">GATE OPEN</span>
          </div>
          <div style="font-size:0.9rem;">
            <strong>Vehicle Number:</strong> TN-09-CB-4210<br>
            <strong>Category:</strong> Non-Commercial Light Motor Vehicle (LMV)<br>
            <strong>Plaza Clearance:</strong> Green Lane Auto-Cleared
          </div>
        `;
      } else {
        res.innerHTML = `
          <div style="color:var(--danger); font-weight:bold;">&#9888; UNREGISTERED / EXPIRED TOLL ID</div>
          <p style="font-size:0.85rem; margin-top:0.35rem;">Collect manual toll fee at booth.</p>
        `;
      }
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-15")

def generate_exp_16(base_dir):
    exp = EXPERIMENTS[15]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 16: ComplainEase - Grievance Redressal System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128221;</div>
        <span>ComplainEase Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 16</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">ComplainEase - Grievance Redressal System</h1>
        <p class="lab-hero-desc">Submit citizen grievances with interactive location marking, real-time resolution timeline tracking, officer proof-of-work status updates, and administrative governance.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="postTab">&#128221; Post Grievance</button>
        <button class="tab-btn" data-tab="statusTab">&#128203; Track My Complaints</button>
        <button class="tab-btn" data-tab="officerTab">&#128110; Officer Action & Proof</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; System Admin</button>
      </div>

      <!-- Post Tab -->
      <div id="postTab" class="tab-pane active">
        <div class="card" style="max-width:750px; margin:0 auto;">
          <div class="card-header">Register Public Grievance / Complaint</div>
          <div class="card-body">
            <form onsubmit="handlePostComplaint(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Category</label>
                  <select id="cmpCat" class="form-select">
                    <option>Roads & Potholes</option>
                    <option>Sanitation & Garbage Overflow</option>
                    <option>Street Lighting & Electrical</option>
                    <option>Water Supply & Drainage</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Ward / Zone</label>
                  <input type="text" id="cmpWard" class="form-control" value="Ward 14 - Adyar Zone" required>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Complaint Title / Summary</label>
                <input type="text" id="cmpTitle" class="form-control" placeholder="e.g. Deep pothole causing traffic obstruction on Main Street" required>
              </div>
              <div class="form-group">
                <label class="form-label">Detailed Description</label>
                <textarea id="cmpDesc" class="form-control" rows="3" placeholder="Provide exact landmark, severity details..." required></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">Location Pin Coordinates (Simulated Map Marker)</label>
                <div style="display:flex; gap:0.5rem;">
                  <input type="text" id="cmpCoords" class="form-control" value="13.0012° N, 80.2565° E (Marked on Map)" readonly>
                  <button type="button" class="btn btn-outline" onclick="pinMap()">Update Map Pin</button>
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Submit Grievance to Municipal Board</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Track Tab -->
      <div id="statusTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Grievance Tracking & Status Timeline</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Complaint ID</th>
                    <th>Category</th>
                    <th>Title</th>
                    <th>Date Filed</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="complaintsTbody">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Officer Tab -->
      <div id="officerTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Field Officer Proof-of-Work Verification</div>
          <div class="card-body" id="officerWorkList">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">System Administration & Officer Accounts</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Manage municipal officer IDs, reassign pending complaints across departments, and view audit metrics.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-16: ComplainEase Grievance Redressal</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let complaints = [
      { id: "CMP-8012", cat: "Roads & Potholes", title: "Pothole near Adyar Signal", date: "2026-11-20", status: "In Progress", proof: "Site inspected by Engineer" }
    ];

    function handlePostComplaint(e) {
      e.preventDefault();
      const cat = document.getElementById('cmpCat').value;
      const title = document.getElementById('cmpTitle').value;
      const cmpId = 'CMP-' + Math.floor(1000 + Math.random() * 9000);

      complaints.push({
        id: cmpId,
        cat: cat,
        title: title,
        date: new Date().toISOString().split('T')[0],
        status: "Submitted",
        proof: "Pending inspection"
      });

      renderComplaints();
      showToast(`Complaint registered successfully! Token: ${cmpId}`, 'success');
      e.target.reset();
    }

    function renderComplaints() {
      const tbody = document.getElementById('complaintsTbody');
      const offList = document.getElementById('officerWorkList');
      tbody.innerHTML = '';
      offList.innerHTML = '';

      complaints.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${c.id}</strong></td>
          <td>${c.cat}</td>
          <td>${c.title}</td>
          <td>${c.date}</td>
          <td><span class="badge ${c.status === 'Resolved' ? 'badge-success' : 'badge-warning'}">${c.status}</span></td>
          <td><button class="btn btn-sm btn-outline" onclick="showFeedback('${c.id}')">Feedback</button></td>
        `;
        tbody.appendChild(tr);

        const card = document.createElement('div');
        card.style.padding = '0.75rem';
        card.style.border = '1px solid var(--border)';
        card.style.borderRadius = 'var(--radius)';
        card.style.marginBottom = '0.75rem';
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between;">
            <strong>${c.id}: ${c.title}</strong>
            <span class="badge badge-primary">${c.status}</span>
          </div>
          <div style="font-size:0.85rem; color:var(--text-muted); margin:0.35rem 0;">Proof of Work: ${c.proof}</div>
          <button class="btn btn-sm btn-success" onclick="resolveComplaint('${c.id}')" ${c.status === 'Resolved' ? 'disabled' : ''}>Upload Proof & Mark Resolved</button>
        `;
        offList.appendChild(card);
      });
    }

    function resolveComplaint(id) {
      const c = complaints.find(item => item.id === id);
      if (c) {
        c.status = "Resolved";
        c.proof = "Pothole filled with bitumen asphalt (Photo Verified)";
        renderComplaints();
        showToast(`Complaint ${id} marked as Resolved with proof of work!`, 'success');
      }
    }

    function pinMap() {
      showToast('GPS Pin updated to current live device location!', 'info');
    }

    function showFeedback(id) {
      prompt("Submit feedback for resolution of " + id + ":", "Quick response, great job!");
      showToast('Feedback submitted to commissioner desk!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderComplaints();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-16")

def generate_exp_17(base_dir):
    exp = EXPERIMENTS[16]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 17: VoteOnline - Secure E-Voting Platform</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .candidate-card { border:1px solid var(--border); border-radius:var(--radius); padding:1.25rem; background:#fff; display:flex; justify-content:space-between; align-items:center; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128077;</div>
        <span>VoteOnline E-Ballot</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 17</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">VoteOnline - Secure E-Voting Platform</h1>
        <p class="lab-hero-desc">Voter ID authentication, simulated 2-factor OTP verification, candidate manifestos, secure single-ballot casting, and real-time live election results for election administrators.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="voteTab">&#128077; Cast Ballot</button>
        <button class="tab-btn" data-tab="resultsTab">&#128202; Live Election Results</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Election Commission Admin</button>
      </div>

      <!-- Vote Tab -->
      <div id="voteTab" class="tab-pane active">
        <div class="card" style="max-width:700px; margin:0 auto 1.5rem auto;">
          <div class="card-header">Step 1: Voter Authentication & 2-Factor OTP</div>
          <div class="card-body">
            <div class="grid grid-2">
              <div class="form-group">
                <label class="form-label">Voter ID Card Number (EPIC)</label>
                <input type="text" id="voterEpic" class="form-control" value="TN/04/092/104921">
              </div>
              <div class="form-group">
                <label class="form-label">2-Factor OTP Code</label>
                <div style="display:flex; gap:0.5rem;">
                  <input type="text" id="voterOtp" class="form-control" placeholder="Enter 6-digit OTP" value="582910">
                  <button class="btn btn-secondary" onclick="showToast('OTP sent to registered phone: 582910', 'info')">Get OTP</button>
                </div>
              </div>
            </div>
            <button class="btn btn-primary btn-block" onclick="verifyVoter()">Verify & Unlock Ballot</button>
          </div>
        </div>

        <div id="ballotSection" style="display:none;">
          <h3 style="margin-bottom:1rem;">Official Ballot - Constituency Ward 12</h3>
          <div style="display:flex; flex-direction:column; gap:1rem;" id="candidatesList">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- Results Tab -->
      <div id="resultsTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Real-Time Certified Election Tally</div>
          <div class="card-body" id="resultsBoard">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Admin Voter Roll & Candidate Allocation</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Manage registered electors roll, verify ballot integrity, and declare election outcomes.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-17: VoteOnline Secure E-Voting Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let candidates = [
      { id: 1, name: "Arun Prakash", party: "Progressive Citizens Party", symbol: "&#127775;", votes: 342 },
      { id: 2, name: "Meenakshi Sundaram", party: "Democratic People Alliance", symbol: "&#127807;", votes: 418 },
      { id: 3, name: "Dr. Ronald George", party: "Clean Governance Forum", symbol: "&#9878;", votes: 295 }
    ];

    let hasVoted = false;

    function verifyVoter() {
      const otp = document.getElementById('voterOtp').value;
      if (otp.length < 4) {
        showToast('Please enter valid OTP!', 'danger');
        return;
      }
      document.getElementById('ballotSection').style.display = 'block';
      renderCandidates();
      showToast('Voter identity verified! Electronic ballot unlocked.', 'success');
    }

    function renderCandidates() {
      const container = document.getElementById('candidatesList');
      container.innerHTML = '';
      candidates.forEach(c => {
        const div = document.createElement('div');
        div.className = 'candidate-card';
        div.innerHTML = `
          <div style="display:flex; align-items:center; gap:1rem;">
            <div style="font-size:2.5rem;">${c.symbol}</div>
            <div>
              <h4 style="margin:0;">${c.name}</h4>
              <div style="font-size:0.85rem; color:var(--text-muted);">${c.party}</div>
            </div>
          </div>
          <button class="btn btn-primary" onclick="castVote(${c.id})" ${hasVoted ? 'disabled' : ''}>Vote For Candidate</button>
        `;
        container.appendChild(div);
      });
    }

    function castVote(id) {
      if (hasVoted) {
        showToast('You have already cast your ballot!', 'danger');
        return;
      }
      const c = candidates.find(item => item.id === id);
      c.votes++;
      hasVoted = true;
      renderCandidates();
      renderResults();
      showToast(`Vote cast successfully for ${c.name}! Encrypted token issued.`, 'success');
    }

    function renderResults() {
      const board = document.getElementById('resultsBoard');
      board.innerHTML = '';
      const totalVotes = candidates.reduce((a, c) => a + c.votes, 0);

      candidates.forEach(c => {
        const pct = Math.round((c.votes / totalVotes) * 100);
        const row = document.createElement('div');
        row.style.marginBottom = '1rem';
        row.innerHTML = `
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <strong>${c.symbol} ${c.name} (${c.party})</strong>
            <span>${c.votes} Votes (${pct}%)</span>
          </div>
          <div style="width:100%; height:12px; background:var(--surface-2); border-radius:6px; overflow:hidden;">
            <div style="width:${pct}%; height:100%; background:var(--primary); transition:width 0.5s ease;"></div>
          </div>
        `;
        board.appendChild(row);
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderResults();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-17")

def generate_exp_18(base_dir):
    exp = EXPERIMENTS[17]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 18: AgriMart - Farmer & Agriculture Supplies</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .agri-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .agri-img { height:150px; background:linear-gradient(135deg, #15803d, #22c55e); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127806;</div>
        <span>AgriMart Agro Supplies</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 18</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">AgriMart - Farmer Supplies Marketplace</h1>
        <p class="lab-hero-desc">Connecting farmers and buyers: Farmer portal for listing seeds, fertilizers & farm tools and tracking sales earnings, and Public buyer portal with wallet balance and order tracking.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="buyerTab">&#128722; Public Buyer Portal</button>
        <button class="tab-btn" data-tab="farmerTab">&#129312; Farmer / Seller Dashboard</button>
      </div>

      <!-- Buyer Tab -->
      <div id="buyerTab" class="tab-pane active">
        <div class="grid grid-3" style="margin-bottom:1.5rem;">
          <div class="stat-card">
            <div class="stat-icon">&#128179;</div>
            <div>
              <div class="stat-value">Rs. 4,500</div>
              <div class="stat-label">Agri-Wallet Balance</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#127806;</div>
            <div>
              <div class="stat-value">100% Organic</div>
              <div class="stat-label">Certified Seeds & Bio-Fertilizers</div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="agriGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Farmer Tab -->
      <div id="farmerTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Post Agricultural Product for Sale</div>
            <div class="card-body">
              <form onsubmit="handleFarmerPost(event)">
                <div class="form-group">
                  <label class="form-label">Product Name</label>
                  <input type="text" id="agName" class="form-control" placeholder="e.g. High-Yield Hybrid Paddy Seeds (10kg)" required>
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Category</label>
                    <select id="agCat" class="form-select">
                      <option>Certified Seeds</option>
                      <option>Bio-Fertilizers</option>
                      <option>Pest Management</option>
                      <option>Farming Tools</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Price (Rs.)</label>
                    <input type="number" id="agPrice" class="form-control" value="850" required>
                  </div>
                </div>
                <button type="submit" class="btn btn-primary btn-block">List Product on AgriMart</button>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">My Sales & Dispatch Status</div>
            <div class="card-body">
              <div class="stat-card" style="margin-bottom:1rem;">
                <div class="stat-icon">&#128176;</div>
                <div>
                  <div class="stat-value">Rs. 18,400</div>
                  <div class="stat-label">Total Farmer Revenue Earned</div>
                </div>
              </div>
              <p style="font-size:0.85rem; color:var(--text-muted);">Direct farm gate delivery network with subsidized shipping.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-18: AgriMart Farmer Supplies Marketplace</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let agroItems = [
      { id: 1, name: "Hybrid Basmati Rice Seeds (5kg)", cat: "Certified Seeds", price: 650, icon: "&#127806;" },
      { id: 2, name: "Organic Vermicompost Enricher (25kg)", cat: "Bio-Fertilizers", price: 450, icon: "&#127793;" },
      { id: 3, name: "Manual Knapsack Crop Sprayer 16L", cat: "Farming Tools", price: 1400, icon: "&#9881;" }
    ];

    function renderAgro() {
      const grid = document.getElementById('agriGrid');
      grid.innerHTML = '';
      agroItems.forEach(item => {
        const c = document.createElement('div');
        c.className = 'agri-card';
        c.innerHTML = `
          <div class="agri-img">${item.icon}</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between;">
              <h4 style="margin:0;">${item.name}</h4>
              <span class="badge badge-success">${item.cat}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1rem;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">Rs. ${item.price}</span>
              <button class="btn btn-sm btn-primary" onclick="buyAgroItem('${item.name}', ${item.price})">Order Product</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function buyAgroItem(name, price) {
      showToast(`Order confirmed for "${name}" (Rs. ${price})!`, 'success');
    }

    function handleFarmerPost(e) {
      e.preventDefault();
      const name = document.getElementById('agName').value;
      const cat = document.getElementById('agCat').value;
      const price = parseInt(document.getElementById('agPrice').value);
      agroItems.push({ id: Date.now(), name, cat, price, icon: "&#127806;" });
      renderAgro();
      e.target.reset();
      showToast('New agro product listed successfully!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderAgro();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-18")

def generate_exp_19(base_dir):
    exp = EXPERIMENTS[18]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 19: VetCare - Animal Healthcare Consultation</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128046;</div>
        <span>VetCare Tele-Clinic</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 19</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">VetCare - Animal Healthcare & Tele-Consultation</h1>
        <p class="lab-hero-desc">Farmers report livestock symptoms (audio, video, photos & text) for veterinary diagnosis. Features free Govt CVH vs paid private clinic consultations, prescriptions, and regional disease analytics.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="farmerPost">&#128046; Report Animal Symptoms</button>
        <button class="tab-btn" data-tab="doctorPortal">&#129658; Veterinarian Doctor</button>
        <button class="tab-btn" data-tab="analyticsTab">&#128202; Regional Disease Analytics</button>
      </div>

      <!-- Farmer Post Tab -->
      <div id="farmerPost" class="tab-pane active">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Post Livestock Medical Symptoms to Veterinarian</div>
          <div class="card-body">
            <form onsubmit="handleVetPost(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Animal Type</label>
                  <select id="vetAnimal" class="form-select">
                    <option>Dairy Cow / Cattle</option>
                    <option>Sheep / Goat</option>
                    <option>Poultry / Chicken</option>
                    <option>Pet Dog / Cat</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Consultation Tier</label>
                  <select id="vetTier" class="form-select" onchange="updateTierFee()">
                    <option value="0">Govt. CVH (Free Public Service)</option>
                    <option value="250">Private Specialist (Rs. 250 fee)</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Observable Symptoms</label>
                <textarea id="vetSymptoms" class="form-control" rows="3" placeholder="e.g. High fever, reduced milk yield, limping on front right leg..." required></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">Attach Image / Video Link Proof</label>
                <input type="text" id="vetProof" class="form-control" value="https://vetcare.org/cases/cow_hoof_photo.jpg">
              </div>
              <div id="feeNote" style="margin-bottom:1rem; font-size:0.9rem; color:var(--text-muted);">
                Fee: <strong>Free (Govt Supported)</strong>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Submit Animal Case</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Doctor Tab -->
      <div id="doctorPortal" class="tab-pane">
        <div class="card">
          <div class="card-header">Assigned Animal Complaints & Clinical Remedies</div>
          <div class="card-body" id="docCasesList">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- Analytics Tab -->
      <div id="analyticsTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Epidemiological Analysis - Prevalent Livestock Diseases</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">Regional disease frequency derived from reported veterinary complaints:</p>
            <div style="margin-bottom:0.75rem;">
              <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
                <strong>Foot and Mouth Disease (FMD)</strong>
                <span>42% of cases in District</span>
              </div>
              <div style="height:10px; background:var(--surface-2); border-radius:5px;"><div style="width:42%; height:100%; background:var(--danger);"></div></div>
            </div>
            <div style="margin-bottom:0.75rem;">
              <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
                <strong>Bovine Mastitis (Udder Infection)</strong>
                <span>35% of cases</span>
              </div>
              <div style="height:10px; background:var(--surface-2); border-radius:5px;"><div style="width:35%; height:100%; background:var(--warning);"></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-19: VetCare Animal Healthcare Consultation</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let vetCases = [
      { id: "VET-102", animal: "Dairy Cow", symptoms: "Fever and blisters around mouth and hooves", tier: "Govt CVH", status: "Prescribed", remedy: "Isolate cow. Administer Antiseptic Footbath + Oxytetracycline 20ml." }
    ];

    function updateTierFee() {
      const val = document.getElementById('vetTier').value;
      document.getElementById('feeNote').innerHTML = val === "0" ? "Fee: <strong>Free (Govt Supported)</strong>" : "Fee: <strong>Rs. 250 (Payable via Bank Transfer or EasyPaisa)</strong>";
    }

    function handleVetPost(e) {
      e.preventDefault();
      const animal = document.getElementById('vetAnimal').value;
      const symptoms = document.getElementById('vetSymptoms').value;
      const tierVal = document.getElementById('vetTier').value;
      const tier = tierVal === "0" ? "Govt CVH" : "Private (Rs. 250 Paid)";
      const cId = 'VET-' + Math.floor(100 + Math.random() * 900);

      vetCases.push({
        id: cId,
        animal: animal,
        symptoms: symptoms,
        tier: tier,
        status: "Under Review",
        remedy: "Doctor diagnosing case..."
      });

      renderCases();
      showToast(`Case ${cId} lodged! Dr. Vet assigned.`, 'success');
      e.target.reset();
    }

    function renderCases() {
      const container = document.getElementById('docCasesList');
      container.innerHTML = '';
      vetCases.forEach(v => {
        const div = document.createElement('div');
        div.style.padding = '1rem';
        div.style.border = '1px solid var(--border)';
        div.style.borderRadius = 'var(--radius)';
        div.style.marginBottom = '1rem';
        div.innerHTML = `
          <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
            <strong>${v.id}: ${v.animal} (${v.tier})</strong>
            <span class="badge ${v.status === 'Prescribed' ? 'badge-success' : 'badge-warning'}">${v.status}</span>
          </div>
          <p style="font-size:0.9rem; margin-bottom:0.5rem;"><strong>Symptoms:</strong> ${v.symptoms}</p>
          <div style="background:var(--surface-2); padding:0.75rem; border-radius:6px; font-size:0.85rem;">
            <strong>Doctor Prescription:</strong> ${v.remedy}
          </div>
        `;
        container.appendChild(div);
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderCases();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-19")

def generate_exp_20(base_dir):
    exp = EXPERIMENTS[19]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 20: RentRide - Modern Vehicle Rental Platform</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .ride-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .ride-img { height:150px; background:linear-gradient(135deg, #0284c7, #38bdf8); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3.5rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128663;</div>
        <span>RentRide Fleet</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 20</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">RentRide - Modern Vehicle Rental Platform</h1>
        <p class="lab-hero-desc">Fleet of sedans, SUVs, and trucks. Date-range rental booking, customer driving license check-in verification, booking history, and admin fleet management.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="fleetTab">&#128663; Vehicle Fleet</button>
        <button class="tab-btn" data-tab="checkinTab">&#128221; Check-in & License Form</button>
        <button class="tab-btn" data-tab="myRidesTab">&#128203; My Rental Bookings</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Fleet Admin</button>
      </div>

      <!-- Fleet Tab -->
      <div id="fleetTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Vehicle Type</label>
                <select id="vTypeFilter" class="form-select" onchange="renderFleet()">
                  <option value="All">All Vehicles</option>
                  <option value="Sedan">Sedan</option>
                  <option value="SUV">SUV (7-Seater)</option>
                  <option value="Truck">Pickup Truck</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Pickup Date</label>
                <input type="date" id="rentStart" class="form-control">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Drop-off Date</label>
                <input type="date" id="rentEnd" class="form-control">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="fleetGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Checkin Tab -->
      <div id="checkinTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Driver's License & Check-in Verification Form</div>
          <div class="card-body">
            <form onsubmit="handleCheckin(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Driver Full Name</label>
                  <input type="text" id="chkDriver" class="form-control" value="Aakif" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Driving License Number</label>
                  <input type="text" id="chkDl" class="form-control" value="DL-04-2022-00941" required>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Permanent Address</label>
                <input type="text" class="form-control" value="No. 45, Anna Nagar, Chennai" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Verify Driver Credentials</button>
            </form>
          </div>
        </div>
      </div>

      <!-- My Rides Tab -->
      <div id="myRidesTab" class="tab-pane">
        <div class="card">
          <div class="card-header">My Vehicle Reservations</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Booking Ref</th>
                    <th>Vehicle Model</th>
                    <th>Dates</th>
                    <th>Total Fare</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody id="ridesTbody">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Admin Fleet Maintenance & Approvals</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Approve user bookings, set vehicle maintenance schedules, and configure peak holiday rental rates.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-20: RentRide Vehicle Rental Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let fleet = [
      { id: 1, name: "Honda City V-Tech", type: "Sedan", daily: 45, seats: "5 Seats", icon: "&#128663;" },
      { id: 2, name: "Toyota Fortuner 4x4", type: "SUV", daily: 95, seats: "7 Seats", icon: "&#128665;" },
      { id: 3, name: "Ford Ranger Heavy", type: "Truck", daily: 80, seats: "4 Seats + Cargo", icon: "&#128667;" }
    ];

    let rentals = [
      { id: "RNT-901", vehicle: "Toyota Fortuner 4x4", dates: "2026-11-28 to 2026-11-30", total: "$190", status: "Approved" }
    ];

    function renderFleet() {
      const grid = document.getElementById('fleetGrid');
      const t = document.getElementById('vTypeFilter').value;
      grid.innerHTML = '';

      const filtered = t === 'All' ? fleet : fleet.filter(f => f.type === t);
      filtered.forEach(f => {
        const c = document.createElement('div');
        c.className = 'ride-card';
        c.innerHTML = `
          <div class="ride-img">${f.icon}</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between;">
              <h4 style="margin:0;">${f.name}</h4>
              <span class="badge badge-primary">${f.type}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin:0.35rem 0;">${f.seats} &bull; Unlimited Mileage</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1rem;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${f.daily} <small style="font-size:0.8rem; color:var(--text-muted);">/ day</small></span>
              <button class="btn btn-sm btn-primary" onclick="bookVehicle('${f.name}', ${f.daily})">Rent Car</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function bookVehicle(name, daily) {
      const bId = 'RNT-' + Math.floor(100 + Math.random() * 900);
      rentals.push({
        id: bId,
        vehicle: name,
        dates: "2026-12-01 to 2026-12-03",
        total: '$' + (daily * 2),
        status: "Pending Approval"
      });
      renderRentals();
      showToast(`Vehicle ${name} reserved! Booking ID: ${bId}`, 'success');
    }

    function renderRentals() {
      const tbody = document.getElementById('ridesTbody');
      tbody.innerHTML = '';
      rentals.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${r.id}</strong></td>
          <td>${r.vehicle}</td>
          <td>${r.dates}</td>
          <td>${r.total}</td>
          <td><span class="badge ${r.status === 'Approved' ? 'badge-success' : 'badge-warning'}">${r.status}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    function handleCheckin(e) {
      e.preventDefault();
      showToast('Driver license verified and stored on secure cloud record!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('rentStart').value = new Date(Date.now() + 2*24*60*60*1000).toISOString().split('T')[0];
      document.getElementById('rentEnd').value = new Date(Date.now() + 5*24*60*60*1000).toISOString().split('T')[0];
      renderFleet();
      renderRentals();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-20")

def run_all(base_dir="LAB"):
    generate_exp_11(base_dir)
    generate_exp_12(base_dir)
    generate_exp_13(base_dir)
    generate_exp_14(base_dir)
    generate_exp_15(base_dir)
    generate_exp_16(base_dir)
    generate_exp_17(base_dir)
    generate_exp_18(base_dir)
    generate_exp_19(base_dir)
    generate_exp_20(base_dir)
    print("Batch 2 completed (Exp 11 to 20).")

if __name__ == "__main__":
    run_all()
