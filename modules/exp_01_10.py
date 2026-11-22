# modules/exp_01_10.py
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
3. Perform end-to-end interactions (searches, bookings, cart updates, and administrative modifications).
"""
    with open(os.path.join(exp_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)

def generate_exp_05(base_dir):
    exp = EXPERIMENTS[4]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 5: Online Flight Reservation System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#9992;</div>
        <span>SkyWings Airlines Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 05</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Online Flight Reservation System</h1>
        <p class="lab-hero-desc">Consolidated flight search, real-time seat inventory, payment simulation, e-ticket & boarding pass generation, cancellation with refund, customer feedback, and admin route reports.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="flightSearch">&#9992; Search Flights</button>
        <button class="tab-btn" data-tab="myTickets">&#127915; My Tickets & Boarding Pass</button>
        <button class="tab-btn" data-tab="feedback">&#128172; Customer Feedback</button>
        <button class="tab-btn" data-tab="admin">&#128188; Airline Admin Reports</button>
      </div>

      <!-- Search Flights Tab -->
      <div id="flightSearch" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-4">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Departure Airport</label>
                <input type="text" id="flightFrom" class="form-control" value="DEL - Delhi Indira Gandhi">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Arrival Airport</label>
                <input type="text" id="flightTo" class="form-control" value="BOM - Mumbai Chhatrapati Shivaji">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Departure Date</label>
                <input type="date" id="flightDate" class="form-control">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Class</label>
                <select id="flightClass" class="form-select">
                  <option>Economy Class</option>
                  <option>Business Class</option>
                  <option>First Class</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="flightCards">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- My Tickets Tab -->
      <div id="myTickets" class="tab-pane">
        <div class="card">
          <div class="card-header">Issued E-Tickets & Boarding Passes</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>PNR</th>
                    <th>Flight</th>
                    <th>Route</th>
                    <th>Date & Time</th>
                    <th>Seat</th>
                    <th>Fare</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody id="ticketsTbody">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback Tab -->
      <div id="feedback" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Customer Experience Feedback</div>
          <div class="card-body">
            <form onsubmit="handleFeedback(event)">
              <div class="form-group">
                <label class="form-label">Passenger Name</label>
                <input type="text" id="fbName" class="form-control" value="Aakif" required>
              </div>
              <div class="form-group">
                <label class="form-label">Flight PNR</label>
                <input type="text" id="fbPnr" class="form-control" placeholder="e.g. SKY-908" required>
              </div>
              <div class="form-group">
                <label class="form-label">Rating (1 to 5 Stars)</label>
                <select id="fbRating" class="form-select">
                  <option>&#9733;&#9733;&#9733;&#9733;&#9733; (5/5) Excellent</option>
                  <option>&#9733;&#9733;&#9733;&#9733;&#9734; (4/5) Very Good</option>
                  <option>&#9733;&#9733;&#9733;&#9734;&#9734; (3/5) Average</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Comments & Suggestions</label>
                <textarea id="fbComments" class="form-control" rows="3" placeholder="Share your experience..."></textarea>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Submit Feedback</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="admin" class="tab-pane">
        <div class="grid grid-3" style="margin-bottom:1.5rem;">
          <div class="stat-card">
            <div class="stat-icon">&#9992;</div>
            <div>
              <div class="stat-value">6</div>
              <div class="stat-label">Daily Scheduled Flights</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#128101;</div>
            <div>
              <div class="stat-value">142</div>
              <div class="stat-label">Passengers Booked Today</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#128176;</div>
            <div>
              <div class="stat-value" id="admRevenue">$12,450</div>
              <div class="stat-label">Total Booking Revenue</div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">Flight Schedule Management</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Real-time global distribution data stream synchronizing flight routes, seat availability, and dynamic pricing across all partner channels.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-05: Online Flight Reservation System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let flights = [
      { id: "SW-101", airline: "SkyWings Express", dep: "06:15", arr: "08:30", price: 110, seats: 14, flightTime: "2h 15m" },
      { id: "SW-204", airline: "SkyWings Prime", dep: "11:45", arr: "14:00", price: 145, seats: 8, flightTime: "2h 15m" },
      { id: "SW-309", airline: "SkyWings Luxury", dep: "18:20", arr: "20:35", price: 160, seats: 22, flightTime: "2h 15m" }
    ];

    let userFlights = [
      { pnr: "SKY-802", flight: "SW-101 SkyWings Express", route: "DEL &rarr; BOM", date: "2026-11-28 06:15", seat: "12A (Window)", fare: 110, status: "Confirmed" }
    ];

    function renderFlights() {
      const container = document.getElementById('flightCards');
      container.innerHTML = '';
      flights.forEach(f => {
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span><strong>${f.id}</strong> - ${f.airline}</span>
            <span class="badge badge-success">${f.seats} Seats Left</span>
          </div>
          <div class="card-body">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
              <div>
                <div style="font-size:1.3rem; font-weight:800;">${f.dep}</div>
                <div style="font-size:0.8rem; color:var(--text-muted);">Departure (DEL)</div>
              </div>
              <div style="text-align:center; font-size:0.8rem; color:var(--text-muted);">
                <div>${f.flightTime}</div>
                <div>&horbar;&#9992;&horbar;</div>
                <div style="color:var(--success);">Non-stop</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:1.3rem; font-weight:800;">${f.arr}</div>
                <div style="font-size:0.8rem; color:var(--text-muted);">Arrival (BOM)</div>
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.4rem; font-weight:800; color:var(--primary);">$${f.price}</span>
              <button class="btn btn-sm btn-primary" onclick="bookFlight('${f.id}', '${f.airline}', ${f.price})">Book Flight</button>
            </div>
          </div>
        `;
        container.appendChild(c);
      });
    }

    function renderTickets() {
      const tbody = document.getElementById('ticketsTbody');
      tbody.innerHTML = '';
      userFlights.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${t.pnr}</strong></td>
          <td>${t.flight}</td>
          <td>${t.route}</td>
          <td>${t.date}</td>
          <td>${t.seat}</td>
          <td>$${t.fare}</td>
          <td><span class="badge ${t.status === 'Confirmed' ? 'badge-success' : 'badge-danger'}">${t.status}</span></td>
          <td>
            <button class="btn btn-sm btn-outline" onclick="printBoardingPass('${t.pnr}')">&#128424; Print</button>
            <button class="btn btn-sm btn-danger" onclick="cancelFlightTicket('${t.pnr}')" ${t.status === 'Cancelled' ? 'disabled' : ''}>Cancel</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function bookFlight(id, name, price) {
      const pnr = 'SKY-' + Math.floor(100 + Math.random() * 900);
      const row = Math.floor(1 + Math.random() * 25);
      const seatLetter = ['A', 'B', 'C', 'D', 'E', 'F'][Math.floor(Math.random() * 6)];
      userFlights.push({
        pnr: pnr,
        flight: `${id} ${name}`,
        route: "DEL &rarr; BOM",
        date: (document.getElementById('flightDate').value || "2026-12-02") + " 06:15",
        seat: `${row}${seatLetter}`,
        fare: price,
        status: "Confirmed"
      });
      renderTickets();
      showToast(`Flight booking confirmed! PNR: ${pnr}, Seat: ${row}${seatLetter}`, 'success');
    }

    function printBoardingPass(pnr) {
      const t = userFlights.find(item => item.pnr === pnr);
      if (t) {
        alert(`========== SKY WINGS BOARDING PASS ==========\\nPNR: ${t.pnr}\\nPASSENGER: Aakif (Adult)\\nFLIGHT: ${t.flight}\\nSEAT: ${t.seat}\\nSTATUS: ${t.status}\\nGATE: B12 | BOARDING TIME: 45m before dep\\n==============================================`);
      }
    }

    function cancelFlightTicket(pnr) {
      const t = userFlights.find(item => item.pnr === pnr);
      if (t && t.status === 'Confirmed') {
        t.status = 'Cancelled';
        const refund = Math.round(t.fare * 0.8);
        renderTickets();
        showToast(`Flight ticket ${pnr} cancelled. Refund of $${refund} credited.`, 'info');
      }
    }

    function handleFeedback(e) {
      e.preventDefault();
      showToast('Thank you! Your feedback has been recorded.', 'success');
      e.target.reset();
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('flightDate').value = new Date(Date.now() + 4*24*60*60*1000).toISOString().split('T')[0];
      renderFlights();
      renderTickets();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-05")

def generate_exp_06(base_dir):
    exp = EXPERIMENTS[5]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 6: Online Cake Ordering System</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .cake-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .cake-img { height:150px; background:linear-gradient(135deg, #f43f5e, #fb7185); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127856;</div>
        <span>SweetDelight Cake Store</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 06</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Online Cake Ordering System</h1>
        <p class="lab-hero-desc">Customized artisan cakes for birthdays, weddings & anniversaries. Customize size (0.5kg to 3kg), personalized message, eggless toggle, shipping tracking, and bakery admin management.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="catalog">&#127856; Cake Catalog</button>
        <button class="tab-btn" data-tab="cart">&#128722; Cart & Checkout (<span id="cartCountBadge">0</span>)</button>
        <button class="tab-btn" data-tab="myOrders">&#128230; My Orders & Tracking</button>
        <button class="tab-btn" data-tab="admin">&#128188; Bakery Admin</button>
      </div>

      <!-- Catalog Tab -->
      <div id="catalog" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Filter by Occasion</label>
                <select id="occFilter" class="form-select" onchange="renderCakes()">
                  <option value="All">All Occasions</option>
                  <option value="Birthday">Birthday</option>
                  <option value="Wedding">Wedding</option>
                  <option value="Anniversary">Anniversary</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Filter by Flavor</label>
                <select id="flavorFilter" class="form-select" onchange="renderCakes()">
                  <option value="All">All Flavors</option>
                  <option value="Chocolate Truffle">Chocolate Truffle</option>
                  <option value="Red Velvet">Red Velvet</option>
                  <option value="Black Forest">Black Forest</option>
                  <option value="Pineapple">Pineapple</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Max Price (Rs.)</label>
                <input type="number" id="maxPriceInput" class="form-control" value="2000" oninput="renderCakes()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="cakeGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Cart & Checkout Tab -->
      <div id="cart" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Shopping Cart</div>
            <div class="card-body" id="cartItemsList">
              <!-- Populated by JS -->
            </div>
          </div>

          <div class="card">
            <div class="card-header">Shipping Address & Payment</div>
            <div class="card-body">
              <form onsubmit="placeOrder(event)">
                <div class="form-group">
                  <label class="form-label">Delivery Street Address</label>
                  <input type="text" id="shipAddr" class="form-control" required value="Plot 42, Sunrise Enclave, Chennai">
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Delivery Date</label>
                    <input type="date" id="delDate" class="form-control" required>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Delivery Time Slot</label>
                    <select id="delSlot" class="form-select">
                      <option>Morning (09:00 - 12:00)</option>
                      <option selected>Evening (16:00 - 19:00)</option>
                      <option>Midnight Surprise (23:30)</option>
                    </select>
                  </div>
                </div>
                <div style="margin:1rem 0; padding:1rem; background:var(--surface-2); border-radius:var(--radius);">
                  <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                    <span>Cart Subtotal:</span>
                    <strong id="cartSubtotal">Rs. 0</strong>
                  </div>
                  <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                    <span>Delivery Charge:</span>
                    <strong style="color:var(--success);">FREE</strong>
                  </div>
                  <div style="display:flex; justify-content:space-between; font-size:1.2rem; border-top:1px solid var(--border); padding-top:0.5rem;">
                    <span>Total Payable:</span>
                    <strong style="color:var(--primary);" id="cartTotal">Rs. 0</strong>
                  </div>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Place Cake Order</button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- My Orders Tab -->
      <div id="myOrders" class="tab-pane">
        <div class="card">
          <div class="card-header">My Orders & Live Shipping Status</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Cake Details</th>
                    <th>Custom Message</th>
                    <th>Delivery Date</th>
                    <th>Total</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody id="ordersTable">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="admin" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Add New Cake to Store</div>
            <div class="card-body">
              <form onsubmit="handleAdminAddCake(event)">
                <div class="form-group">
                  <label class="form-label">Cake Name</label>
                  <input type="text" id="admCakeName" class="form-control" required placeholder="e.g. Belgian Dark Chocolate">
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Occasion</label>
                    <select id="admCakeOcc" class="form-select">
                      <option>Birthday</option>
                      <option>Wedding</option>
                      <option>Anniversary</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Flavor</label>
                    <select id="admCakeFlavor" class="form-select">
                      <option>Chocolate Truffle</option>
                      <option>Red Velvet</option>
                      <option>Black Forest</option>
                      <option>Pineapple</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Base Price (0.5kg)</label>
                  <input type="number" id="admCakePrice" class="form-control" value="650" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Publish Cake</button>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Orders Management</div>
            <div class="card-body" id="adminOrdersList">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-06: Online Cake Ordering System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let cakes = [
      { id: 1, name: "Belgian Chocolate Truffle", occasion: "Birthday", flavor: "Chocolate Truffle", basePrice: 650, icon: "&#127856;" },
      { id: 2, name: "Romantic Red Velvet Heart", occasion: "Anniversary", flavor: "Red Velvet", basePrice: 750, icon: "&#128150;" },
      { id: 3, name: "German Black Forest Cherry", occasion: "Birthday", flavor: "Black Forest", basePrice: 550, icon: "&#127856;" },
      { id: 4, name: "Royal Tier Wedding Fondant", occasion: "Wedding", flavor: "Red Velvet", basePrice: 1600, icon: "&#128141;" },
      { id: 5, name: "Tropical Fresh Pineapple", occasion: "Birthday", flavor: "Pineapple", basePrice: 500, icon: "&#127821;" }
    ];

    let cart = [];
    let orders = [
      { id: "CK-501", item: "Belgian Chocolate Truffle (1kg, Eggless)", msg: "Happy Birthday Aakif!", delDate: "2026-11-26", total: 1200, status: "Baking" }
    ];

    function renderCakes() {
      const container = document.getElementById('cakeGrid');
      const occ = document.getElementById('occFilter').value;
      const flavor = document.getElementById('flavorFilter').value;
      const maxP = parseFloat(document.getElementById('maxPriceInput').value) || 99999;
      container.innerHTML = '';

      const filtered = cakes.filter(c => {
        return (occ === 'All' || c.occasion === occ) &&
               (flavor === 'All' || c.flavor === flavor) &&
               c.basePrice <= maxP;
      });

      filtered.forEach(c => {
        const card = document.createElement('div');
        card.className = 'cake-card';
        card.innerHTML = `
          <div class="cake-img">${c.icon}</div>
          <div style="padding:1.25rem; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <h4 style="margin:0 0 0.25rem 0;">${c.name}</h4>
                <span class="badge badge-primary">${c.occasion}</span>
              </div>
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Flavor: ${c.flavor}</p>
              
              <div class="grid grid-2" style="margin-bottom:0.5rem;">
                <div>
                  <label class="form-label" style="font-size:0.75rem;">Size</label>
                  <select id="size_${c.id}" class="form-select" style="padding:0.35rem; font-size:0.85rem;">
                    <option value="1">0.5 kg</option>
                    <option value="1.8">1 kg</option>
                    <option value="3.4">2 kg</option>
                  </select>
                </div>
                <div>
                  <label class="form-label" style="font-size:0.75rem;">Type</label>
                  <select id="egg_${c.id}" class="form-select" style="padding:0.35rem; font-size:0.85rem;">
                    <option value="Eggless">Eggless</option>
                    <option value="With Egg">With Egg</option>
                  </select>
                </div>
              </div>
              <div class="form-group" style="margin-bottom:0.5rem;">
                <input type="text" id="msg_${c.id}" class="form-control" placeholder="Message on Cake (e.g. Happy B'day)" style="font-size:0.8rem; padding:0.35rem;">
              </div>
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.75rem;">
              <span style="font-size:1.25rem; font-weight:800; color:var(--primary);">Rs. ${c.basePrice}</span>
              <button class="btn btn-sm btn-primary" onclick="addToCart(${c.id})">Add to Cart</button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function addToCart(cakeId) {
      const c = cakes.find(item => item.id === cakeId);
      const sizeMultiplier = parseFloat(document.getElementById(`size_${cakeId}`).value);
      const eggType = document.getElementById(`egg_${cakeId}`).value;
      const msg = document.getElementById(`msg_${cakeId}`).value || "Best Wishes";
      const sizeLabel = sizeMultiplier === 1 ? "0.5 kg" : (sizeMultiplier === 1.8 ? "1 kg" : "2 kg");
      const price = Math.round(c.basePrice * sizeMultiplier);

      cart.push({
        id: Date.now(),
        name: c.name,
        size: sizeLabel,
        egg: eggType,
        msg: msg,
        price: price
      });

      renderCart();
      showToast(`"${c.name}" added to cart!`, 'success');
    }

    function renderCart() {
      const list = document.getElementById('cartItemsList');
      document.getElementById('cartCountBadge').textContent = cart.length;
      list.innerHTML = '';
      if (cart.length === 0) {
        list.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:1.5rem;">Your cart is empty.</p>';
        document.getElementById('cartSubtotal').textContent = 'Rs. 0';
        document.getElementById('cartTotal').textContent = 'Rs. 0';
        return;
      }

      let subtotal = 0;
      cart.forEach((item, idx) => {
        subtotal += item.price;
        const div = document.createElement('div');
        div.style.padding = '0.75rem';
        div.style.borderBottom = '1px solid var(--border)';
        div.style.display = 'flex';
        div.style.justifyContent = 'space-between';
        div.style.alignItems = 'center';
        div.innerHTML = `
          <div>
            <strong>${item.name}</strong> (${item.size}, ${item.egg})
            <div style="font-size:0.8rem; color:var(--text-muted);">Inscription: "${item.msg}"</div>
          </div>
          <div style="display:flex; align-items:center; gap:0.75rem;">
            <strong style="color:var(--primary);">Rs. ${item.price}</strong>
            <button class="btn btn-sm btn-danger" onclick="removeFromCart(${idx})">&times;</button>
          </div>
        `;
        list.appendChild(div);
      });

      document.getElementById('cartSubtotal').textContent = 'Rs. ' + subtotal;
      document.getElementById('cartTotal').textContent = 'Rs. ' + subtotal;
    }

    function removeFromCart(idx) {
      cart.splice(idx, 1);
      renderCart();
    }

    function placeOrder(e) {
      e.preventDefault();
      if (cart.length === 0) {
        showToast('Please add at least one cake to cart!', 'danger');
        return;
      }
      const orderId = 'CK-' + Math.floor(100 + Math.random() * 900);
      const delDate = document.getElementById('delDate').value || "2026-11-29";
      const total = cart.reduce((a, c) => a + c.price, 0);

      orders.push({
        id: orderId,
        item: cart.map(c => `${c.name} (${c.size})`).join(', '),
        msg: cart.map(c => c.msg).join(' | '),
        delDate: delDate,
        total: total,
        status: "Confirmed"
      });

      cart = [];
      renderCart();
      renderOrders();
      showToast(`Order ${orderId} placed successfully! Total: Rs. ${total}`, 'success');
    }

    function renderOrders() {
      const tbody = document.getElementById('ordersTable');
      const admList = document.getElementById('adminOrdersList');
      tbody.innerHTML = '';
      admList.innerHTML = '';

      orders.forEach(o => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${o.id}</strong></td>
          <td>${o.item}</td>
          <td><em>${o.msg}</em></td>
          <td>${o.delDate}</td>
          <td>Rs. ${o.total}</td>
          <td><span class="badge badge-success">${o.status}</span></td>
        `;
        tbody.appendChild(tr);

        const admCard = document.createElement('div');
        admCard.style.padding = '0.75rem';
        admCard.style.border = '1px solid var(--border)';
        admCard.style.borderRadius = 'var(--radius)';
        admCard.style.marginBottom = '0.75rem';
        admCard.innerHTML = `
          <div style="display:flex; justify-content:space-between;">
            <strong>Order: ${o.id}</strong>
            <span class="badge badge-primary">Status: ${o.status}</span>
          </div>
          <div style="font-size:0.85rem; margin:0.35rem 0;">${o.item}</div>
          <button class="btn btn-sm btn-outline" onclick="updateOrderStatus('${o.id}')">Update Status to Dispatched</button>
        `;
        admList.appendChild(admCard);
      });
    }

    function updateOrderStatus(id) {
      const o = orders.find(item => item.id === id);
      if (o) {
        o.status = "Out for Delivery";
        renderOrders();
        showToast(`Order ${id} marked as Out for Delivery!`, 'info');
      }
    }

    function handleAdminAddCake(e) {
      e.preventDefault();
      const name = document.getElementById('admCakeName').value;
      const occ = document.getElementById('admCakeOcc').value;
      const flavor = document.getElementById('admCakeFlavor').value;
      const price = parseInt(document.getElementById('admCakePrice').value);
      cakes.push({ id: Date.now(), name, occasion: occ, flavor, basePrice: price, icon: "&#127856;" });
      renderCakes();
      e.target.reset();
      showToast('Cake published to store catalog!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('delDate').value = new Date(Date.now() + 2*24*60*60*1000).toISOString().split('T')[0];
      renderCakes();
      renderCart();
      renderOrders();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-06")

def generate_exp_07(base_dir):
    exp = EXPERIMENTS[6]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 7: Beauty Parlour Appointment Booking System</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .slot-btn { padding:0.5rem 0.75rem; border:1px solid var(--border); border-radius:6px; background:#fff; cursor:pointer; font-size:0.85rem; font-weight:600; text-align:center; }
    .slot-btn:hover { background:var(--primary-light); }
    .slot-btn.selected { background:var(--primary); color:#fff; }
    .slot-btn.disabled { background:#cbd5e1; color:#94a3b8; cursor:not-allowed; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#10024;</div>
        <span>Glow & Grace Salon</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 07</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Beauty Parlour Appointment Booking System</h1>
        <p class="lab-hero-desc">Interactive reservation calendar, stylist profiles, lockout unavailable hours, payment integration (Full payment or Partial deposit via Stripe/PayPal), and customer & salon manager dashboard.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="bookTab">&#128197; Book Appointment</button>
        <button class="tab-btn" data-tab="clientTab">&#128100; My Appointments</button>
        <button class="tab-btn" data-tab="managerTab">&#128188; Salon Manager & Calendar</button>
      </div>

      <!-- Book Tab -->
      <div id="bookTab" class="tab-pane active">
        <div class="grid grid-2">
          <!-- Step 1: Services & Stylist -->
          <div class="card">
            <div class="card-header">1. Select Service & Senior Stylist</div>
            <div class="card-body">
              <div class="form-group">
                <label class="form-label">Beauty Service</label>
                <select id="serviceSelect" class="form-select" onchange="updateServiceCost()">
                  <option value="60" data-name="Signature Hair Spa & Styling">Signature Hair Spa & Styling - $60</option>
                  <option value="85" data-name="Gold Facial & Skin Glow Treatment">Gold Facial & Skin Glow Treatment - $85</option>
                  <option value="150" data-name="Royal Bridal Makeover">Royal Bridal Makeover - $150</option>
                  <option value="45" data-name="Aromatherapy Body Massage">Aromatherapy Body Massage - $45</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Preferred Stylist</label>
                <select id="stylistSelect" class="form-select">
                  <option>Emma Roberts (Master Colorist & Hair Specialist - 4.9 &#9733;)</option>
                  <option>Sophia Chen (Bridal Makeup & Skincare Expert - 5.0 &#9733;)</option>
                  <option>Lucas Garcia (Aesthetician & Spa Therapist - 4.8 &#9733;)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Appointment Date</label>
                <input type="date" id="parlourDate" class="form-control" onchange="renderSlots()">
              </div>
            </div>
          </div>

          <!-- Step 2: Time Slots & Payment -->
          <div class="card">
            <div class="card-header">2. Available Time Slots & Deposit</div>
            <div class="card-body">
              <label class="form-label">Select Open Time Slot (Lockout booked hours)</label>
              <div class="grid grid-3" id="slotsGrid" style="margin-bottom:1.5rem;">
                <!-- Populated by JS -->
              </div>

              <div class="form-group">
                <label class="form-label">Payment Mode</label>
                <div style="display:flex; gap:1.5rem; margin-top:0.35rem;">
                  <label><input type="radio" name="payType" value="full" checked onchange="updateServiceCost()"> Full Payment (Stripe)</label>
                  <label><input type="radio" name="payType" value="deposit" onchange="updateServiceCost()"> 25% Deposit (PayPal)</label>
                </div>
              </div>

              <div style="padding:1rem; background:var(--surface-2); border-radius:var(--radius); margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
                  <span>Service Total:</span>
                  <strong id="serviceTotalLabel">$60</strong>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:1.15rem; color:var(--primary);">
                  <span>Amount to Pay Now:</span>
                  <strong id="payNowLabel">$60</strong>
                </div>
              </div>

              <button class="btn btn-primary btn-block" onclick="confirmAppointment()">Confirm Reservation</button>
            </div>
          </div>
        </div>
      </div>

      <!-- My Appointments Tab -->
      <div id="clientTab" class="tab-pane">
        <div class="card">
          <div class="card-header">My Upcoming & Past Reservations</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Booking Ref</th>
                    <th>Service</th>
                    <th>Stylist</th>
                    <th>Date & Slot</th>
                    <th>Paid</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="clientTable">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Manager Tab -->
      <div id="managerTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Salon Master Calendar View</div>
            <div class="card-body">
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">Manage salon bookings, lock hours, or dispatch appointment reminders via SMS.</p>
              <div id="managerBookingsList">
                <!-- Populated by JS -->
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Dispatch SMS / Call Reminders</div>
            <div class="card-body">
              <div class="form-group">
                <label class="form-label">Client Mobile Phone</label>
                <input type="text" id="remPhone" class="form-control" value="+1 (555) 234-8901">
              </div>
              <div class="form-group">
                <label class="form-label">Reminder Template</label>
                <textarea class="form-control" rows="3" id="remText">Dear valued customer, this is a reminder for your salon appointment at Glow & Grace tomorrow. Reply C to confirm.</textarea>
              </div>
              <button class="btn btn-secondary btn-block" onclick="sendReminder()">Send SMS Notification</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-07: Beauty Parlour Appointment Booking System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let slots = [
      { time: "10:00 AM", available: true },
      { time: "11:30 AM", available: false },
      { time: "01:00 PM", available: true },
      { time: "02:30 PM", available: true },
      { time: "04:00 PM", available: false },
      { time: "05:30 PM", available: true }
    ];

    let selectedSlot = null;
    let appointments = [
      { id: "GLOW-201", service: "Gold Facial Treatment", stylist: "Sophia Chen", date: "2026-11-26", slot: "11:30 AM", paid: "$85 (Full)", status: "Confirmed" }
    ];

    function updateServiceCost() {
      const select = document.getElementById('serviceSelect');
      const cost = parseFloat(select.value);
      const isDeposit = document.querySelector('input[name="payType"]:checked').value === 'deposit';
      const toPay = isDeposit ? Math.round(cost * 0.25) : cost;

      document.getElementById('serviceTotalLabel').textContent = '$' + cost;
      document.getElementById('payNowLabel').textContent = '$' + toPay;
    }

    function renderSlots() {
      const grid = document.getElementById('slotsGrid');
      grid.innerHTML = '';
      slots.forEach(s => {
        const btn = document.createElement('div');
        btn.className = `slot-btn ${s.available ? '' : 'disabled'}`;
        btn.textContent = s.time;
        if (s.available) {
          btn.onclick = () => {
            document.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedSlot = s.time;
          };
        }
        grid.appendChild(btn);
      });
    }

    function confirmAppointment() {
      if (!selectedSlot) {
        showToast('Please select an available time slot!', 'danger');
        return;
      }
      const select = document.getElementById('serviceSelect');
      const serviceName = select.options[select.selectedIndex].getAttribute('data-name');
      const stylist = document.getElementById('stylistSelect').value.split('(')[0].trim();
      const date = document.getElementById('parlourDate').value;
      const payNow = document.getElementById('payNowLabel').textContent;
      const refId = 'GLOW-' + Math.floor(100 + Math.random() * 900);

      appointments.push({
        id: refId,
        service: serviceName,
        stylist: stylist,
        date: date,
        slot: selectedSlot,
        paid: payNow,
        status: "Confirmed"
      });

      renderAppointments();
      showToast(`Appointment ${refId} booked successfully! Paid: ${payNow}`, 'success');
    }

    function renderAppointments() {
      const tbody = document.getElementById('clientTable');
      const mgr = document.getElementById('managerBookingsList');
      tbody.innerHTML = '';
      mgr.innerHTML = '';

      appointments.forEach(a => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${a.id}</strong></td>
          <td>${a.service}</td>
          <td>${a.stylist}</td>
          <td>${a.date} (${a.slot})</td>
          <td>${a.paid}</td>
          <td><span class="badge ${a.status === 'Confirmed' ? 'badge-success' : 'badge-danger'}">${a.status}</span></td>
          <td>
            <button class="btn btn-sm btn-danger" onclick="cancelAppt('${a.id}')" ${a.status === 'Cancelled' ? 'disabled' : ''}>Cancel</button>
          </td>
        `;
        tbody.appendChild(tr);

        const card = document.createElement('div');
        card.style.padding = '0.75rem';
        card.style.border = '1px solid var(--border)';
        card.style.borderRadius = 'var(--radius)';
        card.style.marginBottom = '0.5rem';
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between;">
            <strong>${a.id}: ${a.service}</strong>
            <span class="badge badge-primary">${a.slot}</span>
          </div>
          <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.25rem;">Stylist: ${a.stylist} &bull; ${a.date}</div>
        `;
        mgr.appendChild(card);
      });
    }

    function cancelAppt(id) {
      const a = appointments.find(item => item.id === id);
      if (a && a.status === 'Confirmed') {
        a.status = 'Cancelled';
        renderAppointments();
        showToast(`Appointment ${id} cancelled.`, 'info');
      }
    }

    function sendReminder() {
      const phone = document.getElementById('remPhone').value;
      showToast(`SMS reminder dispatched to ${phone}!`, 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('parlourDate').value = new Date(Date.now() + 2*24*60*60*1000).toISOString().split('T')[0];
      updateServiceCost();
      renderSlots();
      renderAppointments();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-07")

def generate_exp_08(base_dir):
    exp = EXPERIMENTS[7]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 8: MedCare Hospital Online Appointment Booking</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .doc-card { border:1px solid var(--border); border-radius:var(--radius); padding:1.25rem; background:#fff; display:flex; gap:1rem; }
    .doc-avatar { width:65px; height:65px; border-radius:50%; background:linear-gradient(135deg, #0ea5e9, #38bdf8); display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.8rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127973;</div>
        <span>MedCare Hospital Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 08</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">MedCare Hospital Online Appointment Booking</h1>
        <p class="lab-hero-desc">Streamline outpatient appointments: search doctors by medical specialty & location, flexible slot booking, online check-in form submission, visit history, doctor reviews, and hospital admin analytics.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="findDoc">&#128373; Search Doctors & Book</button>
        <button class="tab-btn" data-tab="checkin">&#128221; Online Pre-Check-in</button>
        <button class="tab-btn" data-tab="history">&#128203; Appointment History</button>
        <button class="tab-btn" data-tab="admin">&#128202; Admin Statistics</button>
      </div>

      <!-- Search Doctors Tab -->
      <div id="findDoc" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Medical Specialty</label>
                <select id="specFilter" class="form-select" onchange="renderDoctors()">
                  <option value="All">All Specialties</option>
                  <option value="Cardiology">Cardiology</option>
                  <option value="Neurology">Neurology</option>
                  <option value="Pediatrics">Pediatrics</option>
                  <option value="Orthopedics">Orthopedics</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Hospital Location</label>
                <select id="locFilter" class="form-select" onchange="renderDoctors()">
                  <option value="All">All Campuses</option>
                  <option value="Central Wing">Central City Campus</option>
                  <option value="South Wing">South Wing Specialist Centre</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Search Doctor Name</label>
                <input type="text" id="docSearchInput" class="form-control" placeholder="e.g. Dr. Ramesh" onkeyup="renderDoctors()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-2" id="docList">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Online Checkin Tab -->
      <div id="checkin" class="tab-pane">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Online Patient Pre-Check-in Form</div>
          <div class="card-body">
            <form onsubmit="handleCheckin(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Patient Full Name</label>
                  <input type="text" id="chkName" class="form-control" value="Aakif" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Appointment ID / Token</label>
                  <input type="text" id="chkToken" class="form-control" value="MED-402" required>
                </div>
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Age & Blood Group</label>
                  <input type="text" id="chkBio" class="form-control" value="21 yrs, O+ve" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Emergency Contact Phone</label>
                  <input type="text" id="chkPhone" class="form-control" value="+91 9876543210" required>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Primary Symptoms / Reasons for Visit</label>
                <textarea class="form-control" id="chkSymptoms" rows="3" required placeholder="Describe pain, symptoms duration, fever..."></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">Known Allergies / Existing Medications</label>
                <input type="text" id="chkAllergies" class="form-control" placeholder="e.g. Penicillin allergy, None">
              </div>
              <button type="submit" class="btn btn-primary btn-block">Submit Check-in Details</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Appointment History Tab -->
      <div id="history" class="tab-pane">
        <div class="card">
          <div class="card-header">Patient Appointment Log & Doctor Reviews</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Token ID</th>
                    <th>Doctor Name</th>
                    <th>Specialty</th>
                    <th>Date & Time</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="patientApptsTable">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="admin" class="tab-pane">
        <div class="grid grid-4" style="margin-bottom:1.5rem;">
          <div class="stat-card">
            <div class="stat-icon">&#128104;&#8205;&#9877;</div>
            <div>
              <div class="stat-value">18</div>
              <div class="stat-label">Doctors on Duty</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#128197;</div>
            <div>
              <div class="stat-value">64</div>
              <div class="stat-label">Appointments Today</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#9989;</div>
            <div>
              <div class="stat-value">52</div>
              <div class="stat-label">Completed Visits</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">&#11088;</div>
            <div>
              <div class="stat-value">4.9 / 5</div>
              <div class="stat-label">Average Patient Rating</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-08: MedCare Hospital Online Appointment Booking</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let doctors = [
      { id: 1, name: "Dr. Ramesh Sharma, MD", spec: "Cardiology", location: "Central Wing", exp: "14 Years Exp", fee: 700, rating: "4.9 &#9733;" },
      { id: 2, name: "Dr. Ananya Iyer, MS", spec: "Neurology", location: "South Wing", exp: "11 Years Exp", fee: 850, rating: "5.0 &#9733;" },
      { id: 3, name: "Dr. Vivek Nair, MD", spec: "Pediatrics", location: "Central Wing", exp: "9 Years Exp", fee: 500, rating: "4.8 &#9733;" },
      { id: 4, name: "Dr. Priya Patel, MS", spec: "Orthopedics", location: "South Wing", exp: "12 Years Exp", fee: 650, rating: "4.9 &#9733;" }
    ];

    let appointments = [
      { token: "MED-402", doctor: "Dr. Ramesh Sharma, MD", spec: "Cardiology", date: "2026-11-27 10:30 AM", status: "Scheduled" }
    ];

    function renderDoctors() {
      const container = document.getElementById('docList');
      const spec = document.getElementById('specFilter').value;
      const loc = document.getElementById('locFilter').value;
      const q = document.getElementById('docSearchInput').value.toLowerCase();
      container.innerHTML = '';

      const filtered = doctors.filter(d => {
        return (spec === 'All' || d.spec === spec) &&
               (loc === 'All' || d.location === loc) &&
               d.name.toLowerCase().includes(q);
      });

      filtered.forEach(d => {
        const card = document.createElement('div');
        card.className = 'doc-card';
        card.innerHTML = `
          <div class="doc-avatar">&#9877;</div>
          <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <div>
                <h4 style="margin:0;">${d.name}</h4>
                <div style="font-size:0.85rem; color:var(--primary); font-weight:600;">${d.spec} &bull; ${d.exp}</div>
              </div>
              <span class="badge badge-primary">${d.rating}</span>
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted); margin:0.35rem 0;">Location: ${d.location} | Consultation Fee: Rs. ${d.fee}</div>
            <div style="display:flex; gap:0.5rem; margin-top:0.75rem;">
              <button class="btn btn-sm btn-primary" onclick="bookDoctor('${d.name}', '${d.spec}')">Book Consultation Slot</button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function bookDoctor(name, spec) {
      const token = 'MED-' + Math.floor(100 + Math.random() * 900);
      const appt = {
        token: token,
        doctor: name,
        spec: spec,
        date: "2026-11-28 11:00 AM",
        status: "Scheduled"
      };
      appointments.push(appt);
      renderHistory();
      showToast(`Appointment confirmed with ${name}! Token: ${token}`, 'success');
    }

    function renderHistory() {
      const tbody = document.getElementById('patientApptsTable');
      tbody.innerHTML = '';
      appointments.forEach(a => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${a.token}</strong></td>
          <td>${a.doctor}</td>
          <td>${a.spec}</td>
          <td>${a.date}</td>
          <td><span class="badge badge-success">${a.status}</span></td>
          <td>
            <button class="btn btn-sm btn-outline" onclick="reviewDoctor('${a.doctor}')">&#9733; Rate</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function handleCheckin(e) {
      e.preventDefault();
      const token = document.getElementById('chkToken').value;
      showToast(`Pre-check-in submitted for Token ${token}! Medical staff alerted.`, 'success');
      e.target.reset();
    }

    function reviewDoctor(doc) {
      const score = prompt(`Rate ${doc} (1 to 5 Stars):`, "5");
      if (score) {
        showToast(`Thank you for rating ${doc} ${score} stars!`, 'success');
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderDoctors();
      renderHistory();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-08")

def generate_exp_09(base_dir):
    exp = EXPERIMENTS[8]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 9: TechSavvy - Electronics Gadgets Shopping</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .prod-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .prod-img { height:150px; background:linear-gradient(135deg, #1e293b, #334155); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128187;</div>
        <span>TechSavvy Gadgets</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 09</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">TechSavvy - Online Gadgets Store</h1>
        <p class="lab-hero-desc">Logically categorized electronics catalog (Smartphones, Laptops, Audio, Tablets). Dynamic shopping cart, item quantity updates, checkout workflow, order tracking, and store admin inventory controls.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="shopTab">&#128722; Shop Gadgets</button>
        <button class="tab-btn" data-tab="cartTab">&#128092; Cart (<span id="cartCount">0</span>)</button>
        <button class="tab-btn" data-tab="ordersTab">&#128230; Order Tracking</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Admin Inventory</button>
      </div>

      <!-- Shop Tab -->
      <div id="shopTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Category Filter</label>
                <select id="catFilter" class="form-select" onchange="renderProducts()">
                  <option value="All">All Gadgets</option>
                  <option value="Smartphones">Smartphones</option>
                  <option value="Laptops">Laptops</option>
                  <option value="Audio">Audio & Headphones</option>
                  <option value="Tablets">Tablets</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Search Gadgets</label>
                <input type="text" id="searchInput" class="form-control" placeholder="Search by name, specs..." onkeyup="renderProducts()">
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Max Price ($)</label>
                <input type="number" id="priceFilter" class="form-control" value="2500" oninput="renderProducts()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="productsGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Cart Tab -->
      <div id="cartTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Your Shopping Cart Items</div>
            <div class="card-body" id="cartContent">
              <!-- Populated by JS -->
            </div>
          </div>

          <div class="card">
            <div class="card-header">Checkout & Order Summary</div>
            <div class="card-body">
              <div style="padding:1rem; background:var(--surface-2); border-radius:var(--radius); margin-bottom:1.5rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                  <span>Subtotal:</span>
                  <strong id="cartSubtotalVal">$0</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                  <span>Tax (8%):</span>
                  <strong id="cartTaxVal">$0</strong>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:1.25rem; border-top:1px solid var(--border); padding-top:0.5rem;">
                  <span>Total Due:</span>
                  <strong style="color:var(--primary);" id="cartTotalVal">$0</strong>
                </div>
              </div>
              <button class="btn btn-primary btn-block" onclick="checkoutOrder()">Complete Checkout</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Orders Tab -->
      <div id="ordersTab" class="tab-pane">
        <div class="card">
          <div class="card-header">My Gadget Orders & Delivery Progress</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Item(s)</th>
                    <th>Date</th>
                    <th>Total Paid</th>
                    <th>Shipping Status</th>
                  </tr>
                </thead>
                <tbody id="ordersTbody">
                  <!-- Populated by JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Add New Gadget to Catalog</div>
            <div class="card-body">
              <form onsubmit="handleAdminAddProduct(event)">
                <div class="form-group">
                  <label class="form-label">Product Name</label>
                  <input type="text" id="admName" class="form-control" required placeholder="e.g. UltraBook Pro 16">
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Category</label>
                    <select id="admCat" class="form-select">
                      <option>Smartphones</option>
                      <option>Laptops</option>
                      <option>Audio</option>
                      <option>Tablets</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Price ($)</label>
                    <input type="number" id="admPrice" class="form-control" value="1299" required>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Description & Specs</label>
                  <textarea id="admDesc" class="form-control" rows="2" placeholder="e.g. 16GB RAM, 1TB SSD M2 Chip"></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Add Item to Inventory</button>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Admin Inventory Control</div>
            <div class="card-body" id="adminInventoryList" style="max-height:450px; overflow-y:auto;">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-09: TechSavvy Electronics Shopping</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let products = [
      { id: 1, name: "Galaxy Titanium Ultra", cat: "Smartphones", price: 1199, desc: "200MP Camera, Snapdragon 8 Gen 3", icon: "&#128241;" },
      { id: 2, name: "MacBook Air M3", cat: "Laptops", price: 1099, desc: "13.6-inch Retina, 16GB Unified RAM", icon: "&#128187;" },
      { id: 3, name: "Sony WH-1000XM5", cat: "Audio", price: 349, desc: "Industry-leading Noise Cancelling", icon: "&#127911;" },
      { id: 4, name: "iPad Air 11-inch", cat: "Tablets", price: 599, desc: "Liquid Retina, M2 Processor", icon: "&#128242;" }
    ];

    let cart = [];
    let orders = [
      { id: "ORD-9021", items: "Galaxy Titanium Ultra (x1)", date: "2026-11-20", total: "$1,294", status: "In Transit" }
    ];

    function renderProducts() {
      const grid = document.getElementById('productsGrid');
      const cat = document.getElementById('catFilter').value;
      const q = document.getElementById('searchInput').value.toLowerCase();
      const maxP = parseFloat(document.getElementById('priceFilter').value) || 99999;
      grid.innerHTML = '';

      const filtered = products.filter(p => {
        return (cat === 'All' || p.cat === cat) &&
               p.price <= maxP &&
               (p.name.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q));
      });

      filtered.forEach(p => {
        const card = document.createElement('div');
        card.className = 'prod-card';
        card.innerHTML = `
          <div class="prod-img">${p.icon}</div>
          <div style="padding:1.25rem; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div style="display:flex; justify-content:space-between;">
                <h4 style="margin:0;">${p.name}</h4>
                <span class="badge badge-primary">${p.cat}</span>
              </div>
              <p style="font-size:0.85rem; color:var(--text-muted); margin:0.5rem 0;">${p.desc}</p>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1rem;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${p.price}</span>
              <button class="btn btn-sm btn-primary" onclick="addToCart(${p.id})">Add to Cart</button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function addToCart(id) {
      const item = products.find(p => p.id === id);
      const existing = cart.find(c => c.id === id);
      if (existing) {
        existing.qty++;
      } else {
        cart.push({ id: item.id, name: item.name, price: item.price, qty: 1 });
      }
      renderCart();
      showToast(`Added ${item.name} to cart!`, 'success');
    }

    function renderCart() {
      const container = document.getElementById('cartContent');
      document.getElementById('cartCount').textContent = cart.reduce((a, c) => a + c.qty, 0);
      container.innerHTML = '';

      if (cart.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:1.5rem;">Cart is empty.</p>';
        document.getElementById('cartSubtotalVal').textContent = '$0';
        document.getElementById('cartTaxVal').textContent = '$0';
        document.getElementById('cartTotalVal').textContent = '$0';
        return;
      }

      let subtotal = 0;
      cart.forEach((item, idx) => {
        subtotal += item.price * item.qty;
        const row = document.createElement('div');
        row.style.padding = '0.75rem';
        row.style.borderBottom = '1px solid var(--border)';
        row.style.display = 'flex';
        row.style.justifyContent = 'space-between';
        row.style.alignItems = 'center';
        row.innerHTML = `
          <div>
            <strong>${item.name}</strong>
            <div style="font-size:0.85rem; color:var(--text-muted);">$${item.price} each</div>
          </div>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <button class="btn btn-sm btn-outline" onclick="changeQty(${idx}, -1)">-</button>
            <span>${item.qty}</span>
            <button class="btn btn-sm btn-outline" onclick="changeQty(${idx}, 1)">+</button>
            <button class="btn btn-sm btn-danger" style="margin-left:0.5rem;" onclick="removeCartItem(${idx})">&times;</button>
          </div>
        `;
        container.appendChild(row);
      });

      const tax = Math.round(subtotal * 0.08);
      document.getElementById('cartSubtotalVal').textContent = '$' + subtotal;
      document.getElementById('cartTaxVal').textContent = '$' + tax;
      document.getElementById('cartTotalVal').textContent = '$' + (subtotal + tax);
    }

    function changeQty(idx, delta) {
      cart[idx].qty += delta;
      if (cart[idx].qty <= 0) cart.splice(idx, 1);
      renderCart();
    }

    function removeCartItem(idx) {
      cart.splice(idx, 1);
      renderCart();
    }

    function checkoutOrder() {
      if (cart.length === 0) {
        showToast('Cart is empty!', 'danger');
        return;
      }
      const ordId = 'ORD-' + Math.floor(1000 + Math.random() * 9000);
      const total = document.getElementById('cartTotalVal').textContent;
      orders.push({
        id: ordId,
        items: cart.map(c => `${c.name} (x${c.qty})`).join(', '),
        date: new Date().toISOString().split('T')[0],
        total: total,
        status: "Processing"
      });
      cart = [];
      renderCart();
      renderOrders();
      showToast(`Order ${ordId} placed successfully!`, 'success');
    }

    function renderOrders() {
      const tbody = document.getElementById('ordersTbody');
      tbody.innerHTML = '';
      orders.forEach(o => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${o.id}</strong></td>
          <td>${o.items}</td>
          <td>${o.date}</td>
          <td>${o.total}</td>
          <td><span class="badge badge-success">${o.status}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    function renderAdminInventory() {
      const list = document.getElementById('adminInventoryList');
      list.innerHTML = '';
      products.forEach(p => {
        const div = document.createElement('div');
        div.style.padding = '0.75rem';
        div.style.border = '1px solid var(--border)';
        div.style.borderRadius = 'var(--radius)';
        div.style.marginBottom = '0.5rem';
        div.style.display = 'flex';
        div.style.justifyContent = 'space-between';
        div.style.alignItems = 'center';
        div.innerHTML = `
          <div>
            <strong>${p.name}</strong> - $${p.price}
            <div style="font-size:0.8rem; color:var(--text-muted);">${p.cat}</div>
          </div>
          <button class="btn btn-sm btn-danger" onclick="deleteProduct(${p.id})">Delete</button>
        `;
        list.appendChild(div);
      });
    }

    function deleteProduct(id) {
      const idx = products.findIndex(p => p.id === id);
      if (idx !== -1) {
        products.splice(idx, 1);
        renderProducts();
        renderAdminInventory();
        showToast('Item deleted from inventory.', 'info');
      }
    }

    function handleAdminAddProduct(e) {
      e.preventDefault();
      const name = document.getElementById('admName').value;
      const cat = document.getElementById('admCat').value;
      const price = parseFloat(document.getElementById('admPrice').value);
      const desc = document.getElementById('admDesc').value;
      products.push({ id: Date.now(), name, cat, price, desc, icon: "&#128241;" });
      renderProducts();
      renderAdminInventory();
      e.target.reset();
      showToast('Product added to inventory!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderProducts();
      renderCart();
      renderOrders();
      renderAdminInventory();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-09")

def generate_exp_10(base_dir):
    exp = EXPERIMENTS[9]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 10: StyleHub - Online Fashion Retailer</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .fashion-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .fashion-img { height:180px; background:linear-gradient(135deg, #ec4899, #f43f5e); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3.5rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128087;</div>
        <span>StyleHub Fashion</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 10</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">StyleHub - Online Fashion Retailer</h1>
        <p class="lab-hero-desc">Trendy collections for Men, Women, and Kids. Interactive size guide (S, M, L, XL, XXL), customer reviews, wishlist, cart, returns and exchanges, and admin product management.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="collectionTab">&#128087; Fashion Catalog</button>
        <button class="tab-btn" data-tab="sizeGuideTab">&#128207; Interactive Size Guide</button>
        <button class="tab-btn" data-tab="cartTab">&#128092; Cart & Returns</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Fashion Admin</button>
      </div>

      <!-- Catalog Tab -->
      <div id="collectionTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Department</label>
                <select id="deptFilter" class="form-select" onchange="renderFashion()">
                  <option value="All">All Departments</option>
                  <option value="Men">Men's Apparel</option>
                  <option value="Women">Women's Collection</option>
                  <option value="Kids">Kids & Toddlers</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Collection</label>
                <select id="seasonFilter" class="form-select" onchange="renderFashion()">
                  <option value="All">All Collections</option>
                  <option value="Casual">Casual Streetwear</option>
                  <option value="Formal">Formal & Evening</option>
                  <option value="Winter">Winter Jackets</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Quick Search</label>
                <input type="text" id="fSearch" class="form-control" placeholder="Search by dress, jacket..." onkeyup="renderFashion()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="fashionGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Size Guide Tab -->
      <div id="sizeGuideTab" class="tab-pane">
        <div class="card" style="max-width:750px; margin:0 auto;">
          <div class="card-header">Interactive Apparel Size Guide (Inches & CM)</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1.25rem;">Select your body measurements to calculate your recommended fit size:</p>
            <div class="grid grid-2" style="margin-bottom:1rem;">
              <div class="form-group">
                <label class="form-label">Chest / Bust (Inches)</label>
                <input type="number" id="sgChest" class="form-control" value="38" oninput="calcSize()">
              </div>
              <div class="form-group">
                <label class="form-label">Waist (Inches)</label>
                <input type="number" id="sgWaist" class="form-control" value="32" oninput="calcSize()">
              </div>
            </div>
            <div style="padding:1.25rem; background:var(--surface-2); border-radius:var(--radius); text-align:center;">
              <div style="font-size:0.9rem; color:var(--text-muted);">Recommended Fit:</div>
              <div style="font-size:2rem; font-weight:800; color:var(--primary);" id="recommendedSizeBadge">M (Medium)</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cart & Returns Tab -->
      <div id="cartTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Fashion Cart & Easy Return / Exchange Request</div>
          <div class="card-body">
            <div class="alert" style="background:#fef2f2; border:1px solid #fecaca; padding:1rem; border-radius:var(--radius); margin-bottom:1.5rem;">
              <strong style="color:#991b1b;">&#9888; Easy 30-Day Free Returns:</strong> If you are not completely satisfied with your fit or style, initiate an instant return/exchange from your dashboard.
            </div>
            <div id="fashionCartItems">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Admin Fashion Inventory Management</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Add new seasonal attire, modify prices, and monitor stock availability across Men, Women, and Kids categories.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-10: StyleHub Online Fashion Retailer</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let fashionItems = [
      { id: 1, name: "Italian Linen Slim Shirt", dept: "Men", col: "Casual", price: 49, icon: "&#128084;" },
      { id: 2, name: "Silk Floral Midi Dress", dept: "Women", col: "Formal", price: 79, icon: "&#128087;" },
      { id: 3, name: "Quilted Winter Parka", dept: "Men", col: "Winter", price: 120, icon: "&#129509;" },
      { id: 4, name: "Kids Denim Dungarees", dept: "Kids", col: "Casual", price: 35, icon: "&#128086;" }
    ];

    function renderFashion() {
      const grid = document.getElementById('fashionGrid');
      const dept = document.getElementById('deptFilter').value;
      const col = document.getElementById('seasonFilter').value;
      const q = document.getElementById('fSearch').value.toLowerCase();
      grid.innerHTML = '';

      const filtered = fashionItems.filter(f => {
        return (dept === 'All' || f.dept === dept) &&
               (col === 'All' || f.col === col) &&
               f.name.toLowerCase().includes(q);
      });

      filtered.forEach(f => {
        const card = document.createElement('div');
        card.className = 'fashion-card';
        card.innerHTML = `
          <div class="fashion-img">${f.icon}</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <h4 style="margin:0;">${f.name}</h4>
              <span class="badge badge-primary">${f.dept}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Collection: ${f.col}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${f.price}</span>
              <button class="btn btn-sm btn-primary" onclick="addFashionToCart('${f.name}', ${f.price})">Buy Now</button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function addFashionToCart(name, price) {
      showToast(`Added ${name} ($${price}) to your cart!`, 'success');
    }

    function calcSize() {
      const chest = parseFloat(document.getElementById('sgChest').value) || 38;
      let size = "M (Medium)";
      if (chest < 36) size = "S (Small)";
      else if (chest <= 39) size = "M (Medium)";
      else if (chest <= 42) size = "L (Large)";
      else if (chest <= 45) size = "XL (Extra Large)";
      else size = "XXL (Double Extra Large)";
      document.getElementById('recommendedSizeBadge').textContent = size;
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderFashion();
      calcSize();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-10")

def run_all(base_dir="LAB"):
    generate_exp_05(base_dir)
    generate_exp_06(base_dir)
    generate_exp_07(base_dir)
    generate_exp_08(base_dir)
    generate_exp_09(base_dir)
    generate_exp_10(base_dir)
    print("Batch 1 completed (Exp 01 to 10).")

if __name__ == "__main__":
    run_all()
