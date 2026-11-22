# modules/exp_31_40.py
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

def generate_exp_31(base_dir):
    exp = EXPERIMENTS[30]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 31: Ko-Matha Smart Dairy Farm Management</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .dairy-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .dairy-img { height:150px; background:linear-gradient(135deg, #10b981, #059669); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#059669;">&#128004;</div>
        <span>Ko-Matha Smart Dairy</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 31</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Ko-Matha Smart Dairy Farm Management</h1>
        <p class="lab-hero-desc">Pioneering Indian A1 cow milk products: Fresh milk, curd, cova-sweet, butter & ghee. Customer online order scheduling, daily/monthly stock entry reports, and milk vendor & cow health management.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="productsTab">&#129371; Dairy Products</button>
        <button class="tab-btn" data-tab="stockTab">&#128202; Stock Entry & Reports</button>
        <button class="tab-btn" data-tab="vendorsTab">&#128104;&#8205;&#127806; Milk Vendors & Cow Care</button>
      </div>

      <!-- Products Tab -->
      <div id="productsTab" class="tab-pane active">
        <div class="grid grid-3" id="dairyGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Stock Tab -->
      <div id="stockTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Daily Milk Yield & Stock Entry</div>
            <div class="card-body">
              <form onsubmit="handleStockEntry(event)">
                <div class="form-group">
                  <label class="form-label">Date</label>
                  <input type="date" id="stkDate" class="form-control" required>
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Morning Collection (Liters)</label>
                    <input type="number" id="stkMorn" class="form-control" value="450" required>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Evening Collection (Liters)</label>
                    <input type="number" id="stkEve" class="form-control" value="380" required>
                  </div>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Log Daily Production</button>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Monthly Yield Performance Summary</div>
            <div class="card-body">
              <div class="stat-card" style="margin-bottom:1rem;">
                <div class="stat-icon">&#129371;</div>
                <div>
                  <div class="stat-value">24,900 Liters</div>
                  <div class="stat-label">Total Monthly Production</div>
                </div>
              </div>
              <p style="font-size:0.85rem; color:var(--text-muted);">Fat content avg: 4.8% &bull; SNF avg: 8.9% (A1 Standard Certified)</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Vendors Tab -->
      <div id="vendorsTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Milk Vendors & Cow Health Records</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Vendor Name</th>
                    <th>Cows Enlisted</th>
                    <th>Breed</th>
                    <th>Health Check Status</th>
                    <th>Daily Supply</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Murugan Dairy Farms</td>
                    <td>14 Cows</td>
                    <td>Gir / Sahiwal A1</td>
                    <td><span class="badge badge-success">Vaccinated & Healthy</span></td>
                    <td>160 Liters</td>
                  </tr>
                  <tr>
                    <td>Kannan Cattle Ranch</td>
                    <td>22 Cows</td>
                    <td>Tharparkar A1</td>
                    <td><span class="badge badge-success">Vaccinated & Healthy</span></td>
                    <td>240 Liters</td>
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
      <p>Internet Programming Lab &bull; Exp-31: Ko-Matha Smart Dairy Farm Management</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let dairyItems = [
      { id: 1, name: "Pure Indian A1 Cow Milk", size: "1 Liter Bottle", price: 65, icon: "&#129371;" },
      { id: 2, name: "Traditional Farm Curd / Dahi", size: "500g Container", price: 40, icon: "&#129371;" },
      { id: 3, name: "Desi Churned White Butter", size: "250g Pack", price: 120, icon: "&#129479;" },
      { id: 4, name: "Traditional Cova Sweet (Palkova)", size: "500g Box", price: 220, icon: "&#127852;" },
      { id: 5, name: "Pure Bilona Vedic Cow Ghee", size: "1 Liter Jar", price: 850, icon: "&#127854;" }
    ];

    function renderDairy() {
      const grid = document.getElementById('dairyGrid');
      grid.innerHTML = '';
      dairyItems.forEach(item => {
        const c = document.createElement('div');
        c.className = 'dairy-card';
        c.innerHTML = `
          <div class="dairy-img">${item.icon}</div>
          <div style="padding:1.25rem;">
            <h4 style="margin:0 0 0.25rem 0;">${item.name}</h4>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">${item.size}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">Rs. ${item.price}</span>
              <button class="btn btn-sm btn-primary" onclick="orderDairy('${item.name}', ${item.price})">Order Online</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function orderDairy(name, price) {
      showToast(`Order confirmed for "${name}" (Rs. ${price})! Scheduled for morning delivery.`, 'success');
    }

    function handleStockEntry(e) {
      e.preventDefault();
      const morn = parseInt(document.getElementById('stkMorn').value);
      const eve = parseInt(document.getElementById('stkEve').value);
      showToast(`Daily yield recorded: ${morn + eve} Liters!`, 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('stkDate').value = new Date().toISOString().split('T')[0];
      renderDairy();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-31")

def generate_exp_32(base_dir):
    exp = EXPERIMENTS[31]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 32: Ram Infotech - Laptop Sales & Service Portal</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128187;</div>
        <span>Ram Infotech Laptop Solutions</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 32</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Ram Infotech - Laptop Sales & Service Portal</h1>
        <p class="lab-hero-desc">Complete computer store: laptop sales catalog with full technical specifications, service center repair scheduling & ticket tracker, laptop rental agreement generator, and stock maintenance.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="salesTab">&#128187; Laptop Sales Store</button>
        <button class="tab-btn" data-tab="serviceTab">&#128295; Service & Repairs</button>
        <button class="tab-btn" data-tab="rentalTab">&#128196; Laptop Rental Agreement</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Stock Maintenance</button>
      </div>

      <!-- Sales Tab -->
      <div id="salesTab" class="tab-pane active">
        <div class="grid grid-3" id="laptopsGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Service Tab -->
      <div id="serviceTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Book Laptop Service / Repair</div>
            <div class="card-body">
              <form onsubmit="handleBookService(event)">
                <div class="form-group">
                  <label class="form-label">Laptop Brand & Model</label>
                  <input type="text" id="srvModel" class="form-control" placeholder="e.g. Dell XPS 15 9520" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Issue Symptom</label>
                  <select id="srvIssue" class="form-select">
                    <option>Screen Replacement / Display Flicker</option>
                    <option>Motherboard Chip-Level Repair</option>
                    <option>Battery Replacement</option>
                    <option>OS Installation & SSD Upgrade</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Generate Service Job Ticket</button>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Service Ticket Status Check</div>
            <div class="card-body">
              <div class="form-group">
                <label class="form-label">Service Ticket ID</label>
                <div style="display:flex; gap:0.5rem;">
                  <input type="text" id="srvTicketSearch" class="form-control" value="SRV-2026-891">
                  <button class="btn btn-primary" onclick="trackService()">Track</button>
                </div>
              </div>
              <div id="srvTrackResult" style="padding:1rem; background:var(--surface-2); border-radius:var(--radius); margin-top:1rem;">
                <strong>Ticket: SRV-2026-891</strong><br>
                Status: <span class="badge badge-primary">Chip-level Diagnosis in Progress</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Rental Tab -->
      <div id="rentalTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Generate Laptop Rental Agreement</div>
          <div class="card-body">
            <form onsubmit="handleRental(event)">
              <div class="form-group">
                <label class="form-label">Customer / Company Name</label>
                <input type="text" class="form-control" value="Aakif (Tech Solutions)" required>
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Rental Duration</label>
                  <select class="form-select">
                    <option>1 Month (Rs. 2,500)</option>
                    <option>3 Months (Rs. 6,800)</option>
                    <option>6 Months (Rs. 12,000)</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Configuration</label>
                  <select class="form-select">
                    <option>Intel Core i7, 16GB RAM, 512GB SSD</option>
                    <option>Intel Core i5, 8GB RAM, 256GB SSD</option>
                  </select>
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Generate Printable Lease Contract</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Shop Inventory Stock Status</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Stock balance across laptops, replacement display panels, NVMe SSDs, and RAM modules.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-32: Ram Infotech Laptop Sales & Service Portal</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let laptops = [
      { id: 1, name: "Dell Inspiron 15 Pro", cpu: "Intel Core i7 13th Gen", ram: "16GB DDR5", ssd: "512GB SSD", price: 68000 },
      { id: 2, name: "Lenovo ThinkPad E14", cpu: "AMD Ryzen 7 7730U", ram: "16GB RAM", ssd: "1TB SSD", price: 74000 },
      { id: 3, name: "HP Pavilion Aero 13", cpu: "AMD Ryzen 5", ram: "16GB RAM", ssd: "512GB SSD", price: 59000 }
    ];

    function renderLaptops() {
      const grid = document.getElementById('laptopsGrid');
      grid.innerHTML = '';
      laptops.forEach(l => {
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span><strong>${l.name}</strong></span>
            <span class="badge badge-primary">New</span>
          </div>
          <div class="card-body">
            <div style="font-size:0.85rem; color:var(--text-muted); line-height:1.6; margin-bottom:1rem;">
              &bull; <strong>Processor:</strong> ${l.cpu}<br>
              &bull; <strong>Memory:</strong> ${l.ram}<br>
              &bull; <strong>Storage:</strong> ${l.ssd}
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">Rs. ${l.price.toLocaleString()}</span>
              <button class="btn btn-sm btn-primary" onclick="showToast('Invoice generated for ${l.name}!', 'success')">Purchase</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function handleBookService(e) {
      e.preventDefault();
      const model = document.getElementById('srvModel').value;
      const tId = 'SRV-2026-' + Math.floor(100 + Math.random() * 900);
      showToast(`Service ticket ${tId} generated for ${model}!`, 'success');
      e.target.reset();
    }

    function trackService() {
      showToast('Status: Repair in progress. Estimated turnaround 24 hours.', 'info');
    }

    function handleRental(e) {
      e.preventDefault();
      showToast('Rental agreement contract generated and ready for digital signing!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderLaptops();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-32")

def generate_exp_33(base_dir):
    exp = EXPERIMENTS[32]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 33: KodaikanalEats - Restaurant & Resort Booking</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127860;</div>
        <span>KodaikanalEats Hospitality</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 33</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">KodaikanalEats - Dining & Resort Booking</h1>
        <p class="lab-hero-desc">Hill station dining table reservations and resort room bookings (Single, Double, Deluxe rooms) with seasonal vs non-seasonal pricing and room boy availability status.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="roomsTab">&#128716; Resort Rooms Booking</button>
        <button class="tab-btn" data-tab="tableTab">&#127860; Restaurant Table Reservation</button>
        <button class="tab-btn" data-tab="boysTab">&#128104;&#8205;&#128188; Room Boy Service Availability</button>
      </div>

      <!-- Rooms Tab -->
      <div id="roomsTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div>
                <strong>Season Pricing Mode:</strong> Select active tourist season tier
              </div>
              <div style="display:flex; gap:1rem;">
                <label><input type="radio" name="season" value="normal" checked onchange="updateRoomRates()"> Non-Seasonal (Standard)</label>
                <label><input type="radio" name="season" value="peak" onchange="updateRoomRates()"> Peak Hill Station Season (+30%)</label>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="roomsList">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Table Tab -->
      <div id="tableTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Reserve Dining Table with Valley View</div>
          <div class="card-body">
            <form onsubmit="handleReserveTable(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Guests Count</label>
                  <select class="form-select">
                    <option>Table for 2 Guests</option>
                    <option>Table for 4 Guests</option>
                    <option>Family Table (6-8 Guests)</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Dining Slot</label>
                  <select class="form-select">
                    <option>Lunch (01:00 PM)</option>
                    <option>Sunset High Tea (05:00 PM)</option>
                    <option>Candlelight Dinner (08:00 PM)</option>
                  </select>
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Confirm Table Reservation</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Room Boys Tab -->
      <div id="boysTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Room Boy & Housekeeping Staff Availability Status</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Staff Name</th>
                    <th>Duty Shift</th>
                    <th>Assigned Wing</th>
                    <th>Current Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Muthu K.</td>
                    <td>Morning (08:00 - 16:00)</td>
                    <td>Pine Valley Wing</td>
                    <td><span class="badge badge-success">Available for Service</span></td>
                  </tr>
                  <tr>
                    <td>Selvam R.</td>
                    <td>Evening (16:00 - 00:00)</td>
                    <td>Lake View Deluxe Suites</td>
                    <td><span class="badge badge-primary">On Active Room Call</span></td>
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
      <p>Internet Programming Lab &bull; Exp-33: KodaikanalEats Hospitality Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let roomTypes = [
      { id: 1, name: "Single Cozy Room", baseRate: 1800, desc: "Queen bed, mountain view, hot water geyser" },
      { id: 2, name: "Double Valley View Room", baseRate: 2800, desc: "King bed, private balcony overlooking Kodai lake" },
      { id: 3, name: "Grand Deluxe Suite", baseRate: 4500, desc: "Fireplace, living room, panoramic mist views" }
    ];

    function updateRoomRates() {
      const isPeak = document.querySelector('input[name="season"]:checked').value === 'peak';
      const grid = document.getElementById('roomsList');
      grid.innerHTML = '';

      roomTypes.forEach(r => {
        const rate = isPeak ? Math.round(r.baseRate * 1.3) : r.baseRate;
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span><strong>${r.name}</strong></span>
            <span class="badge badge-primary">Available</span>
          </div>
          <div class="card-body">
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">${r.desc}</p>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">Rs. ${rate} <small style="font-size:0.8rem; color:var(--text-muted);">/ night</small></span>
              <button class="btn btn-sm btn-primary" onclick="showToast('Room booked at Rs. ${rate}/night!', 'success')">Book Room</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function handleReserveTable(e) {
      e.preventDefault();
      showToast('Valley view dining table reserved!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      updateRoomRates();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-33")

def generate_exp_34(base_dir):
    exp = EXPERIMENTS[33]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 34: LearnWell Tuition Centre Management System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128218;</div>
        <span>LearnWell Tuition Centre</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 34</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">LearnWell Tuition Centre Management System</h1>
        <p class="lab-hero-desc">Course offerings with fees, duration & online/offline availability, student enrollment and fee payment tracking, teacher allocations, progress reports, and maintenance request desk.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="coursesTab">&#128214; Course Offerings</button>
        <button class="tab-btn" data-tab="studentTab">&#128104;&#8205;&#127891; Student Enrollment & Fees</button>
        <button class="tab-btn" data-tab="teacherTab">&#128104;&#8205;&#127979; Teacher Allocations</button>
      </div>

      <!-- Courses Tab -->
      <div id="coursesTab" class="tab-pane active">
        <div class="grid grid-3" id="coursesGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Student Tab -->
      <div id="studentTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Enrolled Students & Fee Payment Ledger</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Student Name</th>
                    <th>Enrolled Subject</th>
                    <th>Mode</th>
                    <th>Monthly Fee</th>
                    <th>Fee Payment Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Aakif (Grade 12)</td>
                    <td>Advanced Physics & Calculus</td>
                    <td>Offline Classroom</td>
                    <td>Rs. 2,000</td>
                    <td><span class="badge badge-success">Paid (November)</span></td>
                  </tr>
                  <tr>
                    <td>Kavya S. (Grade 10)</td>
                    <td>Mathematics & Science</td>
                    <td>Online Interactive</td>
                    <td>Rs. 1,500</td>
                    <td><span class="badge badge-success">Paid (November)</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Teacher Tab -->
      <div id="teacherTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Faculty Subject Allocations & Schedule</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Prof. Srinivasan &bull; Advanced Calculus &bull; Mon/Wed/Fri (17:30 - 19:00)</p>
            <p style="font-size:0.9rem; color:var(--text-muted);">Dr. Meera &bull; Quantum Physics &bull; Tue/Thu/Sat (17:30 - 19:00)</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-34: LearnWell Tuition Centre System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let subjects = [
      { id: 1, name: "Mathematics & Calculus", duration: "6 Months", fee: 1800, mode: "Online & Offline Available" },
      { id: 2, name: "Physics: Mechanics & Waves", duration: "6 Months", fee: 1600, mode: "Online & Offline Available" },
      { id: 3, name: "Computer Science & Python", duration: "4 Months", fee: 2000, mode: "Online Interactive" }
    ];

    function renderCourses() {
      const grid = document.getElementById('coursesGrid');
      grid.innerHTML = '';
      subjects.forEach(s => {
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span><strong>${s.name}</strong></span>
            <span class="badge badge-primary">${s.duration}</span>
          </div>
          <div class="card-body">
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">Mode: ${s.mode}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">Rs. ${s.fee} <small style="font-size:0.8rem; color:var(--text-muted);">/ mo</small></span>
              <button class="btn btn-sm btn-primary" onclick="showToast('Enrolled in ${s.name}!', 'success')">Enroll Now</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderCourses();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-34")

def generate_exp_35(base_dir):
    exp = EXPERIMENTS[34]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 35: EduConnect - Interactive Online Teaching Platform</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#4f46e5;">&#127891;</div>
        <span>EduConnect Learning</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 35</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">EduConnect - Interactive Teaching Platform</h1>
        <p class="lab-hero-desc">Interactive virtual classroom: Course catalog, student & instructor registration, subject allocation, video lecture streaming, and knowledge check quizzes.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="catalogTab">&#128214; Course Catalog</button>
        <button class="tab-btn" data-tab="classTab">&#128250; Virtual Classroom & Lecture</button>
        <button class="tab-btn" data-tab="quizTab">&#9997; Practice Quiz</button>
      </div>

      <!-- Catalog Tab -->
      <div id="catalogTab" class="tab-pane active">
        <div class="grid grid-3" id="eduCoursesGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Classroom Tab -->
      <div id="classTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Lecture: Modern Internet Programming & Web Architecture</div>
          <div class="card-body">
            <div style="height:260px; background:#1e293b; border-radius:var(--radius); display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.5rem; margin-bottom:1rem;">
              &#9658; Click to Play Live Stream / Recorded Session
            </div>
            <button class="btn btn-outline" onclick="showToast('Downloading Lecture_Notes_Module1.pdf...', 'info')">&#128229; Download Lecture Slides</button>
          </div>
        </div>
      </div>

      <!-- Quiz Tab -->
      <div id="quizTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Quiz: HTTP Protocols & DOM Manipulation</div>
          <div class="card-body">
            <p><strong>Q1. Which HTTP method is idempotent and used to retrieve resources without state change?</strong></p>
            <div style="display:flex; flex-direction:column; gap:0.5rem; margin:1rem 0;">
              <label><input type="radio" name="q1" value="A"> POST</label>
              <label><input type="radio" name="q1" value="B" id="correctOpt"> GET</label>
              <label><input type="radio" name="q1" value="C"> PATCH</label>
            </div>
            <button class="btn btn-primary" onclick="submitQuiz()">Submit Answers</button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-35: EduConnect Online Teaching Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let eduCourses = [
      { id: 1, title: "Internet Programming & Web Apps", instructor: "Prof. Arvind K.", lessons: 24, progress: "65%" },
      { id: 2, title: "Full-Stack Python & Django", instructor: "Dr. Rachel Green", lessons: 32, progress: "10%" },
      { id: 3, title: "Database Systems & SQL Optimization", instructor: "Prof. Narayanan", lessons: 18, progress: "80%" }
    ];

    function renderEduCourses() {
      const grid = document.getElementById('eduCoursesGrid');
      grid.innerHTML = '';
      eduCourses.forEach(c => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-header">
            <span><strong>${c.title}</strong></span>
          </div>
          <div class="card-body">
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Instructor: ${c.instructor} &bull; ${c.lessons} Lessons</div>
            <div style="margin-bottom:0.5rem; font-size:0.85rem;">Progress: <strong>${c.progress}</strong></div>
            <button class="btn btn-sm btn-primary btn-block" onclick="showToast('Resuming course: ${c.title}...', 'info')">Resume Learning</button>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function submitQuiz() {
      if (document.getElementById('correctOpt').checked) {
        showToast('Correct! GET is an idempotent HTTP retrieval method.', 'success');
      } else {
        showToast('Incorrect option selected. Review HTTP methods.', 'danger');
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderEduCourses();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-35")

def generate_exp_36(base_dir):
    exp = EXPERIMENTS[35]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 36: BookHaven - Online Bookstore</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .bh-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .bh-cover { height:180px; background:linear-gradient(135deg, #b45309, #d97706); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3.5rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#b45309;">&#128214;</div>
        <span>BookHaven Bookstore</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 36</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">BookHaven - Online Bookstore</h1>
        <p class="lab-hero-desc">Curated books with genre filters (Fiction, Non-fiction, Academic), cover previews, synopsis, shopping cart, customer FAQ accordion, and literary blog.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="catalogTab">&#128214; Book Catalog</button>
        <button class="tab-btn" data-tab="cartTab">&#128722; Cart (<span id="bhCartCount">0</span>)</button>
        <button class="tab-btn" data-tab="faqTab">&#10067; FAQs & Privacy Policy</button>
      </div>

      <!-- Catalog Tab -->
      <div id="catalogTab" class="tab-pane active">
        <div class="grid grid-3" id="booksGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Cart Tab -->
      <div id="cartTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Your Books Cart</div>
          <div class="card-body" id="bhCartItems">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- FAQ Tab -->
      <div id="faqTab" class="tab-pane">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Frequently Asked Questions</div>
          <div class="card-body">
            <h4 style="margin:0 0 0.25rem 0;">What is the standard shipping turnaround?</h4>
            <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">Orders are dispatched within 24 hours. Express delivery takes 2-3 business days.</p>
            <h4 style="margin:0 0 0.25rem 0;">Can I return a purchased book?</h4>
            <p style="font-size:0.9rem; color:var(--text-muted);">Unused books with original spine condition are eligible for full refund within 14 days.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-36: BookHaven Online Bookstore</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let bookCatalog = [
      { id: 1, title: "The Pragmatic Programmer", author: "David Thomas", genre: "Academic", price: 38 },
      { id: 2, title: "Atomic Habits", author: "James Clear", genre: "Non-fiction", price: 22 },
      { id: 3, title: "The Midnight Library", author: "Matt Haig", genre: "Fiction", price: 18 }
    ];

    let bhCart = [];

    function renderBooks() {
      const grid = document.getElementById('booksGrid');
      grid.innerHTML = '';
      bookCatalog.forEach(b => {
        const c = document.createElement('div');
        c.className = 'bh-card';
        c.innerHTML = `
          <div class="bh-cover">&#128214;</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
              <h4 style="margin:0;">${b.title}</h4>
              <span class="badge badge-primary">${b.genre}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">By ${b.author}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${b.price}</span>
              <button class="btn btn-sm btn-primary" onclick="addBook(${b.id})">Add to Cart</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function addBook(id) {
      const b = bookCatalog.find(item => item.id === id);
      bhCart.push(b);
      document.getElementById('bhCartCount').textContent = bhCart.length;
      renderBhCart();
      showToast(`Added "${b.title}" to cart!`, 'success');
    }

    function renderBhCart() {
      const list = document.getElementById('bhCartItems');
      list.innerHTML = '';
      if (bhCart.length === 0) {
        list.innerHTML = '<p style="color:var(--text-muted); text-align:center;">Your cart is empty.</p>';
        return;
      }
      bhCart.forEach(item => {
        const div = document.createElement('div');
        div.style.padding = '0.75rem 0';
        div.style.borderBottom = '1px solid var(--border)';
        div.style.display = 'flex';
        div.style.justifyContent = 'space-between';
        div.innerHTML = `<span>${item.title}</span><strong>$${item.price}</strong>`;
        list.appendChild(div);
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderBooks();
      renderBhCart();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-36")

def generate_exp_37(base_dir):
    exp = EXPERIMENTS[36]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 37: MyProfessionalShowcase - Portfolio & Resume</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128188;</div>
        <span>MyProfessionalShowcase</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 37</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Aakif - Full Stack Software Engineer</h1>
        <p class="lab-hero-desc">Interactive portfolio showcase: technical skill matrices, featured engineering projects, career milestone timeline, and downloadable formatted resume.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="aboutTab">&#128100; About Me & Skills</button>
        <button class="tab-btn" data-tab="projectsTab">&#128187; Featured Projects</button>
        <button class="tab-btn" data-tab="resumeTab">&#128196; Interactive Resume</button>
      </div>

      <!-- About Tab -->
      <div id="aboutTab" class="tab-pane active">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Engineering Background</div>
            <div class="card-body">
              <p style="font-size:0.95rem; line-height:1.7; color:var(--text-main);">Passionate Computer Science student and web technologist specializing in distributed web applications, modern responsive UI design, and scalable backend services.</p>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Technical Competencies</div>
            <div class="card-body">
              <div style="margin-bottom:0.75rem;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:0.25rem;">
                  <span>HTML5 / CSS3 / JavaScript (ES6+)</span>
                  <strong>95%</strong>
                </div>
                <div style="height:8px; background:var(--surface-2); border-radius:4px;"><div style="width:95%; height:100%; background:var(--primary);"></div></div>
              </div>
              <div style="margin-bottom:0.75rem;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:0.25rem;">
                  <span>React.js / Node.js</span>
                  <strong>90%</strong>
                </div>
                <div style="height:8px; background:var(--surface-2); border-radius:4px;"><div style="width:90%; height:100%; background:var(--secondary);"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:0.25rem;">
                  <span>Database Engineering (SQL & NoSQL)</span>
                  <strong>85%</strong>
                </div>
                <div style="height:8px; background:var(--surface-2); border-radius:4px;"><div style="width:85%; height:100%; background:var(--success);"></div></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Projects Tab -->
      <div id="projectsTab" class="tab-pane">
        <div class="grid grid-3">
          <div class="card">
            <div class="card-header">Sportix Analytics Platform</div>
            <div class="card-body">
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">Real-time football performance analytics, automated event metrics, and match intelligence dashboard.</p>
              <button class="btn btn-sm btn-outline btn-block" onclick="showToast('Opening repository...', 'info')">View GitHub Repository</button>
            </div>
          </div>
          <div class="card">
            <div class="card-header">Internet Programming Lab Hub</div>
            <div class="card-body">
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">46 comprehensive full-stack laboratory experiments covering university engineering curriculum.</p>
              <button class="btn btn-sm btn-outline btn-block" onclick="showToast('Already exploring Lab Hub!', 'info')">Explore Projects</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Resume Tab -->
      <div id="resumeTab" class="tab-pane">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Curriculum Vitae</div>
          <div class="card-body">
            <p><strong>Education:</strong> B.E. Computer Science & Engineering (2022 - 2026)</p>
            <p><strong>Honors:</strong> First Class with Distinction, Dean's Merit List</p>
            <button class="btn btn-primary" style="margin-top:1rem;" onclick="showToast('Downloading Aakif_Resume.pdf...', 'success')">&#128229; Download PDF Resume</button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-37: MyProfessionalShowcase Portfolio</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-37")

def generate_exp_38(base_dir):
    exp = EXPERIMENTS[37]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 38: Gourmet Haven - Fine Dining Restaurant</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .carousel-box { height:220px; background:linear-gradient(135deg, #1c1917, #44403c); border-radius:var(--radius); display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.8rem; margin-bottom:1.5rem; text-align:center; padding:1.5rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#78350f;">&#127860;</div>
        <span>Gourmet Haven Fine Dining</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 38</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="carousel-box" id="ambianceCarousel">
        <div>
          <h3>Candlelit Ambiance & Sommelier Wine Pairing</h3>
          <p style="font-size:0.9rem; color:#d6d3d1; margin-top:0.35rem;">Crafted by Michelin-Starred Executive Chef Antoine Laurent</p>
        </div>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="menuTab">&#127860; A La Carte Menu</button>
        <button class="tab-btn" data-tab="resTab">&#128197; Table Reservation</button>
        <button class="tab-btn" data-tab="chefTab">&#128104;&#8205;&#127859; About Our Culinary Team</button>
      </div>

      <!-- Menu Tab -->
      <div id="menuTab" class="tab-pane active">
        <div class="grid grid-3">
          <div class="card">
            <div class="card-header">Truffle Infused Wild Mushroom Risotto</div>
            <div class="card-body">
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Carnaroli rice, black winter truffle shavings, aged Parmigiano Reggiano.</p>
              <strong style="font-size:1.25rem; color:var(--primary);">$38.00</strong>
            </div>
          </div>
          <div class="card">
            <div class="card-header">Pan-Seared Chilean Sea Bass</div>
            <div class="card-body">
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Saffron velouté, glazed baby carrots, heirloom microgreens.</p>
              <strong style="font-size:1.25rem; color:var(--primary);">$52.00</strong>
            </div>
          </div>
          <div class="card">
            <div class="card-header">Valrhona Dark Chocolate Soufflé</div>
            <div class="card-body">
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Grand Marnier anglaise, Madagascar vanilla bean gelato.</p>
              <strong style="font-size:1.25rem; color:var(--primary);">$24.00</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Reservation Tab -->
      <div id="resTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Book a Fine Dining Table</div>
          <div class="card-body">
            <form onsubmit="handleReserve(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Reservation Date</label>
                  <input type="date" id="resDate" class="form-control" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Seating Area</label>
                  <select class="form-select">
                    <option>Main Dining Room</option>
                    <option>Wine Cellar Table</option>
                    <option>Private Terrace</option>
                  </select>
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Confirm Table Reservation</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Chef Tab -->
      <div id="chefTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Culinary Philosophy</div>
          <div class="card-body">
            <p style="line-height:1.7;">At Gourmet Haven, every dish is an artful union of farm-to-table organic produce and classical French techniques, elevated with modern gastronomy.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-38: Gourmet Haven Fine Dining Restaurant</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function handleReserve(e) {
      e.preventDefault();
      showToast('Table reserved successfully! Confirmation sent.', 'success');
    }
    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('resDate').value = new Date(Date.now() + 2*24*60*60*1000).toISOString().split('T')[0];
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-38")

def generate_exp_39(base_dir):
    exp = EXPERIMENTS[38]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 39: TechStore - Clean Product Catalog & Cart</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128717;</div>
        <span>Minimal E-Store</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 39</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Clean E-Commerce Product Catalog & Cart</h1>
        <p class="lab-hero-desc">Straightforward product catalog, fast search, multi-category filters, dynamic quantity modifications in cart, and simulated order confirmation.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="catalogTab">&#128717; Catalog</button>
        <button class="tab-btn" data-tab="cartTab">&#128722; Shopping Cart (<span id="cartBadge">0</span>)</button>
      </div>

      <div id="catalogTab" class="tab-pane active">
        <div class="grid grid-3" id="catalogGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <div id="cartTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Checkout Shopping Cart</div>
          <div class="card-body" id="cartItems">
            <!-- Populated by JS -->
          </div>
          <div class="card-footer" style="display:flex; justify-content:space-between; align-items:center;">
            <div>Total: <strong id="totalPriceLabel">$0</strong></div>
            <button class="btn btn-primary" onclick="checkout()">Proceed to Checkout</button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-39: Clean Product Catalog & Cart</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let products = [
      { id: 1, name: "Wireless Mechanical Keyboard", cat: "Accessories", price: 89 },
      { id: 2, name: "Ergonomic Precision Mouse", cat: "Accessories", price: 49 },
      { id: 3, name: "27-inch 4K HDR Monitor", cat: "Displays", price: 340 }
    ];

    let cart = [];

    function renderCatalog() {
      const grid = document.getElementById('catalogGrid');
      grid.innerHTML = '';
      products.forEach(p => {
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span><strong>${p.name}</strong></span>
            <span class="badge badge-primary">${p.cat}</span>
          </div>
          <div class="card-body">
            <div style="font-size:1.3rem; font-weight:800; color:var(--primary); margin-bottom:1rem;">$${p.price}</div>
            <button class="btn btn-sm btn-primary btn-block" onclick="addToCart(${p.id})">Add to Cart</button>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function addToCart(id) {
      const p = products.find(item => item.id === id);
      cart.push(p);
      document.getElementById('cartBadge').textContent = cart.length;
      renderCart();
      showToast(`Added ${p.name} to cart!`, 'success');
    }

    function renderCart() {
      const container = document.getElementById('cartItems');
      container.innerHTML = '';
      if (cart.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center;">Cart is empty.</p>';
        document.getElementById('totalPriceLabel').textContent = '$0';
        return;
      }
      let sum = 0;
      cart.forEach((item, idx) => {
        sum += item.price;
        const row = document.createElement('div');
        row.style.padding = '0.5rem 0';
        row.style.borderBottom = '1px solid var(--border)';
        row.style.display = 'flex';
        row.style.justifyContent = 'space-between';
        row.innerHTML = `<span>${item.name}</span><strong>$${item.price}</strong>`;
        container.appendChild(row);
      });
      document.getElementById('totalPriceLabel').textContent = '$' + sum;
    }

    function checkout() {
      if (cart.length === 0) {
        showToast('Cart is empty!', 'danger');
        return;
      }
      showToast('Order confirmed! Receipt emailed.', 'success');
      cart = [];
      document.getElementById('cartBadge').textContent = '0';
      renderCart();
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderCatalog();
      renderCart();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-39")

def generate_exp_40(base_dir):
    exp = EXPERIMENTS[39]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 40: Travel Explorer - Interactive Travel Blog</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .map-box { height:220px; background:linear-gradient(135deg, #0284c7, #0369a1); border-radius:var(--radius); display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.5rem; margin-bottom:1.5rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127758;</div>
        <span>Travel Explorer Journal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 40</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="map-box">
        &#127757; Interactive Visited Destinations: 14 Countries Marked Across 4 Continents
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="storiesTab">&#128214; Travel Stories</button>
        <button class="tab-btn" data-tab="aboutTab">&#128100; About the Traveler</button>
      </div>

      <!-- Stories Tab -->
      <div id="storiesTab" class="tab-pane active">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Solo Trekking Across the Norwegian Fjords</div>
            <div class="card-body">
              <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">Navigating the steep cliffs of Preikestolen under the midnight sun with lightweight bivouac gear.</p>
              <div style="border-top:1px solid var(--border); padding-top:0.75rem;">
                <strong>Reader Comments:</strong>
                <p style="font-size:0.85rem; color:var(--text-muted); margin-top:0.25rem;">"Incredible photography! Did you encounter heavy winds near the summit?" &mdash; Maya</p>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Kyoto's Hidden Bamboo Forests & Teahouses</div>
            <div class="card-body">
              <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">An intimate morning walk through Arashiyama and savoring traditional matcha ceremonies in Uji.</p>
              <div style="border-top:1px solid var(--border); padding-top:0.75rem;">
                <strong>Reader Comments:</strong>
                <p style="font-size:0.85rem; color:var(--text-muted); margin-top:0.25rem;">"Saved this for my spring travel list. Beautiful advice!" &mdash; David</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- About Tab -->
      <div id="aboutTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">About the Traveler</div>
          <div class="card-body">
            <p style="line-height:1.7;">Documenting slow travel, mountain expeditions, and authentic culinary encounters worldwide.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-40: Travel Explorer Interactive Blog</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-40")

def run_all(base_dir="LAB"):
    generate_exp_31(base_dir)
    generate_exp_32(base_dir)
    generate_exp_33(base_dir)
    generate_exp_34(base_dir)
    generate_exp_35(base_dir)
    generate_exp_36(base_dir)
    generate_exp_37(base_dir)
    generate_exp_38(base_dir)
    generate_exp_39(base_dir)
    generate_exp_40(base_dir)
    print("Batch 4 completed (Exp 31 to 40).")

if __name__ == "__main__":
    run_all()
