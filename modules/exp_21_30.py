# modules/exp_21_30.py
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

def generate_exp_21(base_dir):
    exp = EXPERIMENTS[20]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 21: JobPortal - Vacancy & Recruitment Platform</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128188;</div>
        <span>CareerLink Job Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 21</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">JobPortal - Vacancy & Recruitment Platform</h1>
        <p class="lab-hero-desc">Connecting employers and talent: Company Directors post vacancies and review applied candidate resumes; Job Seekers filter jobs by category & location and apply online.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="jobsTab">&#128188; Browse Vacancies</button>
        <button class="tab-btn" data-tab="directorTab">&#127970; Company Director (Post Jobs)</button>
        <button class="tab-btn" data-tab="applicantTab">&#128203; Review Applicants</button>
      </div>

      <!-- Jobs Tab -->
      <div id="jobsTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Category</label>
                <select id="jCat" class="form-select" onchange="renderJobs()">
                  <option value="All">All Categories</option>
                  <option value="Software Engineering">Software Engineering</option>
                  <option value="Data Science">Data Science</option>
                  <option value="UI/UX Design">UI/UX Design</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Location</label>
                <select id="jLoc" class="form-select" onchange="renderJobs()">
                  <option value="All">All Locations</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Bangalore">Bangalore</option>
                  <option value="Remote">Remote</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Search Keywords</label>
                <input type="text" id="jSearch" class="form-control" placeholder="e.g. React, Python..." onkeyup="renderJobs()">
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-2" id="jobsGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Director Tab -->
      <div id="directorTab" class="tab-pane">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Post New Job Vacancy</div>
          <div class="card-body">
            <form onsubmit="handlePostJob(event)">
              <div class="form-group">
                <label class="form-label">Job Title</label>
                <input type="text" id="postJobTitle" class="form-control" required placeholder="e.g. Full Stack Web Developer">
              </div>
              <div class="grid grid-3">
                <div class="form-group">
                  <label class="form-label">Category</label>
                  <select id="postJobCat" class="form-select">
                    <option>Software Engineering</option>
                    <option>Data Science</option>
                    <option>UI/UX Design</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Location</label>
                  <input type="text" id="postJobLoc" class="form-control" value="Chennai" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Salary Range</label>
                  <input type="text" id="postJobSalary" class="form-control" value="12-16 LPA" required>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Key Requirements & Description</label>
                <textarea id="postJobDesc" class="form-control" rows="3" required placeholder="HTML5, CSS3, JavaScript, Node.js, SQL..."></textarea>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Publish Vacancy</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Applicants Tab -->
      <div id="applicantTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Applied Candidate Resumes</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Candidate</th>
                    <th>Job Role</th>
                    <th>Experience</th>
                    <th>Application Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="applicantsTbody">
                  <!-- Populated by JS -->
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
      <p>Internet Programming Lab &bull; Exp-21: JobPortal Vacancy & Recruitment Platform</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let jobListings = [
      { id: 1, title: "Frontend Web Architect", cat: "Software Engineering", loc: "Chennai", salary: "14-18 LPA", company: "Infosys Labs", desc: "Expertise in React, TypeScript, and modern responsive layouts." },
      { id: 2, title: "Lead AI/ML Research Engineer", cat: "Data Science", loc: "Bangalore", salary: "22-28 LPA", company: "DeepMind Tech", desc: "Python, PyTorch, LLM fine-tuning, and scalable inference." },
      { id: 3, title: "Senior Product Designer", cat: "UI/UX Design", loc: "Remote", salary: "12-15 LPA", company: "Zomato Digital", desc: "Figma design systems, user journey mapping, and usability testing." }
    ];

    let applicants = [
      { id: 101, name: "Aakif (Student)", job: "Frontend Web Architect", exp: "Fresher (B.E. CSE)", status: "Shortlisted" }
    ];

    function renderJobs() {
      const grid = document.getElementById('jobsGrid');
      const cat = document.getElementById('jCat').value;
      const loc = document.getElementById('jLoc').value;
      const q = document.getElementById('jSearch').value.toLowerCase();
      grid.innerHTML = '';

      const filtered = jobListings.filter(j => {
        return (cat === 'All' || j.cat === cat) &&
               (loc === 'All' || j.loc === loc) &&
               (j.title.toLowerCase().includes(q) || j.desc.toLowerCase().includes(q));
      });

      filtered.forEach(j => {
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span><strong>${j.title}</strong></span>
            <span class="badge badge-primary">${j.loc}</span>
          </div>
          <div class="card-body">
            <div style="font-size:0.85rem; color:var(--primary); font-weight:bold; margin-bottom:0.35rem;">${j.company} &bull; ${j.salary}</div>
            <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">${j.desc}</p>
            <button class="btn btn-sm btn-primary" onclick="applyJob('${j.title}')">Submit Application</button>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function applyJob(title) {
      applicants.push({
        id: Date.now(),
        name: "Aakif (Self)",
        job: title,
        exp: "B.E. Computer Science",
        status: "Submitted"
      });
      renderApplicants();
      showToast(`Application submitted for "${title}"!`, 'success');
    }

    function renderApplicants() {
      const tbody = document.getElementById('applicantsTbody');
      tbody.innerHTML = '';
      applicants.forEach(a => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${a.name}</strong></td>
          <td>${a.job}</td>
          <td>${a.exp}</td>
          <td><span class="badge badge-success">${a.status}</span></td>
          <td><button class="btn btn-sm btn-outline" onclick="showToast('Candidate shortlisted for tech interview!', 'success')">Shortlist</button></td>
        `;
        tbody.appendChild(tr);
      });
    }

    function handlePostJob(e) {
      e.preventDefault();
      const title = document.getElementById('postJobTitle').value;
      const cat = document.getElementById('postJobCat').value;
      const loc = document.getElementById('postJobLoc').value;
      const salary = document.getElementById('postJobSalary').value;
      const desc = document.getElementById('postJobDesc').value;

      jobListings.push({ id: Date.now(), title, cat, loc, salary, company: "Direct Tech Corp", desc });
      renderJobs();
      e.target.reset();
      showToast('New vacancy posted successfully!', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderJobs();
      renderApplicants();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-21")

def generate_exp_22(base_dir):
    exp = EXPERIMENTS[21]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 22: Smart Solid Waste Management System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#9851;</div>
        <span>EcoClean Smart Waste</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 22</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Smart Solid Waste Management System</h1>
        <p class="lab-hero-desc">IoT sensor-monitored smart garbage bins (0-100% capacity), automated optimal route generation for collection trucks to the dumping site, driver load logging, and public overflow complaints.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="binsTab">&#128465; Smart Bins Network</button>
        <button class="tab-btn" data-tab="driverTab">&#128667; Truck Driver Optimal Route</button>
        <button class="tab-btn" data-tab="publicTab">&#128104; Public Complaints</button>
      </div>

      <!-- Bins Tab -->
      <div id="binsTab" class="tab-pane active">
        <div class="grid grid-3" id="binsGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Driver Tab -->
      <div id="driverTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Automated Route Optimization for Garbage Truck #04</div>
          <div class="card-body">
            <div class="alert" style="background:#eff6ff; border:1px solid #bfdbfe; padding:1rem; border-radius:var(--radius); margin-bottom:1.5rem;">
              <h4 style="color:#1d4ed8; margin-bottom:0.25rem;">&#128506; Calculated Optimal Collection Route</h4>
              <p style="font-size:0.9rem; color:#1e40af;"><strong>Depot &rarr; Bin #02 (92% Fill) &rarr; Bin #03 (85% Fill) &rarr; Kodungaiyur Dumping Yard</strong><br>Estimated Mileage: 14.2 km &bull; Projected Fuel Savings: 22%</p>
            </div>
            <div class="form-group">
              <label class="form-label">Log Total Collected Load (kg)</label>
              <div style="display:flex; gap:0.5rem; max-width:400px;">
                <input type="number" id="truckLoad" class="form-control" value="840">
                <button class="btn btn-primary" onclick="showToast('Garbage load of 840 kg logged at dumping facility!', 'success')">Submit Load</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Public Tab -->
      <div id="publicTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Report Overflowing Dustbin</div>
          <div class="card-body">
            <form onsubmit="handlePublicReport(event)">
              <div class="form-group">
                <label class="form-label">Street / Area Landmark</label>
                <input type="text" id="binLoc" class="form-control" value="Corner of 4th Cross St, Besant Nagar" required>
              </div>
              <div class="form-group">
                <label class="form-label">Garbage Segregation Type</label>
                <select class="form-select">
                  <option>Mixed Municipal Solid Waste</option>
                  <option>Organic Compostable</option>
                  <option>Plastic / Recyclable</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Dispatch Emergency Cleaning Truck</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-22: Smart Solid Waste Management System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let smartBins = [
      { id: "BIN-01", loc: "Marina Beach Promenade", fill: 35, type: "Recyclable", status: "Normal" },
      { id: "BIN-02", loc: "T. Nagar Ranganathan St", fill: 92, type: "Organic", status: "Critical Overflow" },
      { id: "BIN-03", loc: "Central Railway Station", fill: 85, type: "Mixed", status: "Near Full" }
    ];

    function renderBins() {
      const grid = document.getElementById('binsGrid');
      grid.innerHTML = '';
      smartBins.forEach(b => {
        const isCrit = b.fill >= 80;
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `
          <div class="card-header">
            <span>${b.id}</span>
            <span class="badge ${isCrit ? 'badge-danger' : 'badge-success'}">${b.status}</span>
          </div>
          <div class="card-body">
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">${b.loc} &bull; ${b.type}</div>
            <div style="margin-bottom:0.5rem; display:flex; justify-content:space-between;">
              <strong>Fill Level:</strong>
              <strong>${b.fill}%</strong>
            </div>
            <div style="height:12px; background:var(--surface-2); border-radius:6px; overflow:hidden; margin-bottom:1rem;">
              <div style="width:${b.fill}%; height:100%; background:${isCrit ? 'var(--danger)' : 'var(--primary)'};"></div>
            </div>
            <button class="btn btn-sm btn-outline btn-block" onclick="emptyBin('${b.id}')">Empty & Reset Sensor</button>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function emptyBin(id) {
      const b = smartBins.find(item => item.id === id);
      b.fill = 5;
      b.status = "Normal";
      renderBins();
      showToast(`Bin ${id} emptied and sensor reset!`, 'success');
    }

    function handlePublicReport(e) {
      e.preventDefault();
      showToast('Public grievance logged! Sanitation supervisor alerted.', 'success');
      e.target.reset();
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderBins();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-22")

def generate_exp_23(base_dir):
    exp = EXPERIMENTS[22]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 23: Blood Management Information System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:var(--danger);">&#129656;</div>
        <span>LifeBlood Bank Network</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 23</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Blood Management Information System</h1>
        <p class="lab-hero-desc">National donor registry and hospital inventory: register as a blood donor, search donors by blood group & city, track real-time blood bank stock units, and manage emergency hospital requisitions.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="searchDonor">&#128269; Find Blood Donors</button>
        <button class="tab-btn" data-tab="regDonor">&#129656; Register as Donor</button>
        <button class="tab-btn" data-tab="hospitalTab">&#127973; Hospital Blood Bank Stock</button>
      </div>

      <!-- Search Donor Tab -->
      <div id="searchDonor" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body">
            <div class="grid grid-3">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">Required Blood Group</label>
                <select id="srchGroup" class="form-select" onchange="renderDonors()">
                  <option value="All">All Groups</option>
                  <option value="O+">O Positive (O+)</option>
                  <option value="O-">O Negative (O-) Universal</option>
                  <option value="A+">A Positive (A+)</option>
                  <option value="B+">B Positive (B+)</option>
                  <option value="AB+">AB Positive (AB+)</option>
                </select>
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label">City</label>
                <input type="text" id="srchCity" class="form-control" value="Chennai" onkeyup="renderDonors()">
              </div>
              <div class="form-group" style="margin-bottom:0; display:flex; align-items:flex-end;">
                <button class="btn btn-danger btn-block" onclick="broadcastSos()">&#128680; Emergency SOS Request</button>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-3" id="donorsGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Register Donor Tab -->
      <div id="regDonor" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Register as a Voluntary Blood Donor</div>
          <div class="card-body">
            <form onsubmit="handleRegisterDonor(event)">
              <div class="form-group">
                <label class="form-label">Full Name</label>
                <input type="text" id="dName" class="form-control" required placeholder="e.g. Aakif">
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Blood Group</label>
                  <select id="dGroup" class="form-select">
                    <option>O+</option>
                    <option>O-</option>
                    <option>A+</option>
                    <option>B+</option>
                    <option>AB+</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">City</label>
                  <input type="text" id="dCity" class="form-control" value="Chennai" required>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Mobile Contact Number</label>
                <input type="text" id="dPhone" class="form-control" value="+91 9876543210" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Enlist in National Donor Registry</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Hospital Tab -->
      <div id="hospitalTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Hospital Central Blood Inventory Units</div>
          <div class="card-body">
            <div class="grid grid-4" style="text-align:center;">
              <div class="stat-card" style="justify-content:center;">
                <div>
                  <div class="stat-value" style="color:var(--danger);">24 Units</div>
                  <div class="stat-label">Blood Group O+</div>
                </div>
              </div>
              <div class="stat-card" style="justify-content:center;">
                <div>
                  <div class="stat-value" style="color:var(--danger);">6 Units</div>
                  <div class="stat-label">Blood Group O- (Rare)</div>
                </div>
              </div>
              <div class="stat-card" style="justify-content:center;">
                <div>
                  <div class="stat-value" style="color:var(--danger);">18 Units</div>
                  <div class="stat-label">Blood Group A+</div>
                </div>
              </div>
              <div class="stat-card" style="justify-content:center;">
                <div>
                  <div class="stat-value" style="color:var(--danger);">14 Units</div>
                  <div class="stat-label">Blood Group B+</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-23: Blood Management Information System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let donors = [
      { id: 1, name: "Dr. Suresh Kumar", group: "O+", city: "Chennai", phone: "+91 98401 11223", available: true },
      { id: 2, name: "Priyanka Nair", group: "O-", city: "Chennai", phone: "+91 98402 33445", available: true },
      { id: 3, name: "Mohammed Tariq", group: "B+", city: "Bangalore", phone: "+91 98403 55667", available: true }
    ];

    function renderDonors() {
      const grid = document.getElementById('donorsGrid');
      const g = document.getElementById('srchGroup').value;
      const c = document.getElementById('srchCity').value.toLowerCase();
      grid.innerHTML = '';

      const filtered = donors.filter(d => {
        return (g === 'All' || d.group === g) &&
               d.city.toLowerCase().includes(c);
      });

      filtered.forEach(d => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-header">
            <span>${d.name}</span>
            <span class="badge badge-danger">${d.group}</span>
          </div>
          <div class="card-body">
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">&#128205; ${d.city} &bull; ${d.phone}</div>
            <button class="btn btn-sm btn-outline btn-block" onclick="contactDonor('${d.name}', '${d.phone}')">Contact Donor</button>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    function contactDonor(name, phone) {
      showToast(`Contacting voluntary donor ${name} at ${phone}...`, 'info');
    }

    function broadcastSos() {
      showToast('EMERGENCY BROADCAST sent to all matching blood donors in the district!', 'success');
    }

    function handleRegisterDonor(e) {
      e.preventDefault();
      const name = document.getElementById('dName').value;
      const group = document.getElementById('dGroup').value;
      const city = document.getElementById('dCity').value;
      const phone = document.getElementById('dPhone').value;

      donors.push({ id: Date.now(), name, group, city, phone, available: true });
      renderDonors();
      e.target.reset();
      showToast('Enlisted as voluntary life donor! Thank you.', 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderDonors();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-23")

def generate_exp_24(base_dir):
    exp = EXPERIMENTS[23]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 24: Wanderlust Travels - Travel Agency & Booking</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .tour-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .tour-img { height:160px; background:linear-gradient(135deg, #0ea5e9, #0284c7); display:flex; align-items:center; justify-content:center; color:#fff; font-size:3rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127757;</div>
        <span>Wanderlust Travels</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 24</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Wanderlust Travels - Online Travel Agency</h1>
        <p class="lab-hero-desc">All-in-one travel agency platform: curated destinations, hotel & route details, dining packages, online booking confirmation vouchers, and tourism administration controls.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="packagesTab">&#127958; Tour Packages</button>
        <button class="tab-btn" data-tab="myBookingsTab">&#127915; My Booked Trips</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Tourism Admin</button>
      </div>

      <!-- Packages Tab -->
      <div id="packagesTab" class="tab-pane active">
        <div class="grid grid-3" id="toursGrid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- My Bookings Tab -->
      <div id="myBookingsTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Confirmed Vacation Bookings</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Voucher Ref</th>
                    <th>Destination</th>
                    <th>Duration</th>
                    <th>Hotel Stay</th>
                    <th>Total Cost</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody id="vouchersTbody">
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
          <div class="card-header">Admin Tourism & Hotel Contracting</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Manage vacation routes, negotiate dining contracts, and oversee agency revenue logs.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-24: Wanderlust Travels Online Agency</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let tours = [
      { id: 1, dest: "Swiss Alps & Lucerne", days: "5 Days / 4 Nights", hotel: "5-Star Alpine Resort + Breakfast", price: 1450, icon: "&#127956;" },
      { id: 2, dest: "Bali Tropical Paradise", days: "6 Days / 5 Nights", hotel: "Private Beach Villa + Island Tour", price: 890, icon: "&#127958;" },
      { id: 3, dest: "Kyoto Heritage & Mount Fuji", days: "7 Days / 6 Nights", hotel: "Traditional Ryokan + Bullet Train", price: 1650, icon: "&#127800;" }
    ];

    let bookings = [
      { id: "TRV-8901", dest: "Swiss Alps & Lucerne", days: "5D / 4N", hotel: "Alpine Resort", cost: "$1,450", status: "Confirmed" }
    ];

    function renderTours() {
      const grid = document.getElementById('toursGrid');
      grid.innerHTML = '';
      tours.forEach(t => {
        const c = document.createElement('div');
        c.className = 'tour-card';
        c.innerHTML = `
          <div class="tour-img">${t.icon}</div>
          <div style="padding:1.25rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <h4 style="margin:0;">${t.dest}</h4>
              <span class="badge badge-primary">${t.days}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">${t.hotel}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:1.3rem; font-weight:800; color:var(--primary);">$${t.price}</span>
              <button class="btn btn-sm btn-primary" onclick="bookTour('${t.dest}', '${t.days}', '${t.hotel}', ${t.price})">Book Package</button>
            </div>
          </div>
        `;
        grid.appendChild(c);
      });
    }

    function bookTour(dest, days, hotel, price) {
      const vId = 'TRV-' + Math.floor(1000 + Math.random() * 9000);
      bookings.push({ id: vId, dest, days, hotel, cost: '$' + price, status: "Confirmed" });
      renderBookings();
      showToast(`Vacation booked! Voucher ${vId} generated.`, 'success');
    }

    function renderBookings() {
      const tbody = document.getElementById('vouchersTbody');
      tbody.innerHTML = '';
      bookings.forEach(b => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${b.id}</strong></td>
          <td>${b.dest}</td>
          <td>${b.days}</td>
          <td>${b.hotel}</td>
          <td>${b.cost}</td>
          <td><span class="badge badge-success">${b.status}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderTours();
      renderBookings();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-24")

def generate_exp_25(base_dir):
    exp = EXPERIMENTS[24]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 25: On-Road Vehicle Breakdown Assistance</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128295;</div>
        <span>RoadRescue On-Demand Assistance</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 25</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">On-Road Vehicle Breakdown Assistance System</h1>
        <p class="lab-hero-desc">Immediate roadside breakdown rescue: GPS radar locating nearest certified mechanics, service selection (tire flat, battery jumpstart, towing), mechanic job dispatch, and customer ratings.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="sosTab">&#128680; Emergency SOS Request</button>
        <button class="tab-btn" data-tab="mechanicTab">&#128295; Mechanic Portal</button>
      </div>

      <!-- SOS Tab -->
      <div id="sosTab" class="tab-pane active">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Request Nearby Emergency Roadside Mechanic</div>
          <div class="card-body">
            <form onsubmit="handleSosRequest(event)">
              <div class="form-group">
                <label class="form-label">Breakdown Issue Type</label>
                <select id="sosIssue" class="form-select">
                  <option>Flat Tire Puncture Repair</option>
                  <option>Dead Battery Jumpstart</option>
                  <option>Engine Overheating / Coolant Leak</option>
                  <option>Flatbed Towing Truck Service</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Vehicle Details</label>
                <input type="text" id="sosVeh" class="form-control" value="Honda City (TN-09-CB-4210)" required>
              </div>
              <div class="form-group">
                <label class="form-label">Simulated GPS Breakdown Location</label>
                <input type="text" class="form-control" value="OMR Expressway near Navalur Toll, Chennai" readonly>
              </div>
              <button type="submit" class="btn btn-danger btn-block">&#128680; Dispatch Nearest Certified Mechanic</button>
            </form>

            <div id="radarResult" style="margin-top:1.5rem; display:none; padding:1.25rem; background:var(--surface-2); border-radius:var(--radius);">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>

      <!-- Mechanic Tab -->
      <div id="mechanicTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Licensed Mechanic Business Profile & Active Dispatches</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">View incoming roadside SOS alerts, accept towing jobs, and navigate to client coordinates.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-25: On-Road Breakdown Assistance System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function handleSosRequest(e) {
      e.preventDefault();
      const issue = document.getElementById('sosIssue').value;
      const res = document.getElementById('radarResult');
      res.style.display = 'block';
      res.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
          <h4 style="margin:0; color:var(--success);">&#9989; MECHANIC DISPATCHED!</h4>
          <span class="badge badge-primary">ETA: 12 Mins</span>
        </div>
        <div style="font-size:0.9rem;">
          <strong>Technician:</strong> Kumar Auto Works (Govt Certified Mechanic)<br>
          <strong>Distance:</strong> 1.8 km away &bull; Phone: +91 98409 88771<br>
          <strong>Assigned Service:</strong> ${issue}
        </div>
      `;
      showToast('Roadside assistance team dispatched to your location!', 'success');
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-25")

def generate_exp_26(base_dir):
    exp = EXPERIMENTS[25]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 26: Traffic Squad - E-Challan & Penalty Management</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:var(--primary);">&#128659;</div>
        <span>Traffic Squad E-Challan</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 26</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Traffic Squad - E-Challan & Penalty System</h1>
        <p class="lab-hero-desc">Digital enforcement of traffic rules: Police officers file violation cases with photo proof, citizens search & pay e-Challan penalties online, with live traffic advisory updates.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="citizenTab">&#128663; Citizen Challan Lookup & Pay</button>
        <button class="tab-btn" data-tab="policeTab">&#128110; Police Officer (Create FIR)</button>
        <button class="tab-btn" data-tab="trafficTab">&#128657; Live Traffic Updates</button>
      </div>

      <!-- Citizen Tab -->
      <div id="citizenTab" class="tab-pane active">
        <div class="card" style="max-width:650px; margin:0 auto 1.5rem auto;">
          <div class="card-header">Search Pending Traffic Violations</div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">Vehicle Registration Number</label>
              <div style="display:flex; gap:0.5rem;">
                <input type="text" id="vehSearch" class="form-control" value="TN-01-AX-4820">
                <button class="btn btn-primary" onclick="searchChallan()">Search Challans</button>
              </div>
            </div>
          </div>
        </div>

        <div id="challanResult" style="display:none;" class="card">
          <div class="card-header">Pending Violation Challan Record</div>
          <div class="card-body" id="challanDetails">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- Police Tab -->
      <div id="policeTab" class="tab-pane">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">File Traffic Violation FIR & Photo Proof</div>
          <div class="card-body">
            <form onsubmit="handleFileCase(event)">
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Vehicle Number</label>
                  <input type="text" id="polVeh" class="form-control" placeholder="e.g. TN-07-BL-9912" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Violation Rule</label>
                  <select id="polRule" class="form-select" onchange="updateFineAmt()">
                    <option value="1000">Signal Jumping / Red Light (Rs. 1,000)</option>
                    <option value="1000">Riding Without Helmet (Rs. 1,000)</option>
                    <option value="2000">Overspeeding Beyond Limit (Rs. 2,000)</option>
                    <option value="5000">Dangerous Driving / Drunk Drive (Rs. 5,000)</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Upload Photo Proof (Simulated Link)</label>
                <input type="text" class="form-control" value="https://trafficpolice.gov.in/proofs/cam_junction_42.jpg" readonly>
              </div>
              <button type="submit" class="btn btn-danger btn-block">Issue Certified E-Challan</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Traffic Tab -->
      <div id="trafficTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Live Road Traffic Advisory & Congestion Map</div>
          <div class="card-body">
            <div class="alert" style="background:#fffbeb; border:1px solid #fde68a; padding:1rem; border-radius:var(--radius); margin-bottom:1rem;">
              <strong>&#9888; Traffic Alert:</strong> Heavy congestion reported on Anna Salai due to metro construction work. Commuters advised to use bypass route.
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-26: Traffic Squad E-Challan Management</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let challans = [
      { id: "CHN-89210", veh: "TN-01-AX-4820", rule: "Signal Jumping / Red Light", fine: 1000, date: "2026-11-18", status: "Unpaid" }
    ];

    function searchChallan() {
      const q = document.getElementById('vehSearch').value.trim();
      const item = challans.find(c => c.veh === q);
      const res = document.getElementById('challanResult');
      const det = document.getElementById('challanDetails');
      res.style.display = 'block';

      if (item) {
        det.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <div>
              <h4 style="margin:0;">Challan No: ${item.id}</h4>
              <div style="font-size:0.85rem; color:var(--text-muted);">Vehicle: ${item.veh} &bull; Date: ${item.date}</div>
            </div>
            <span class="badge ${item.status === 'Paid' ? 'badge-success' : 'badge-danger'}">${item.status}</span>
          </div>
          <p><strong>Violation:</strong> ${item.rule}</p>
          <div style="font-size:1.4rem; font-weight:800; color:var(--primary); margin-bottom:1rem;">Penalty: Rs. ${item.fine}</div>
          <button class="btn btn-success" onclick="payChallan('${item.id}')" ${item.status === 'Paid' ? 'disabled' : ''}>Pay Fine Online</button>
        `;
      } else {
        det.innerHTML = `<span style="color:var(--success);">&#9989; No pending traffic challans found for vehicle ${q}.</span>`;
      }
    }

    function payChallan(id) {
      const item = challans.find(c => c.id === id);
      if (item) {
        item.status = "Paid";
        searchChallan();
        showToast(`Penalty for Challan ${id} paid successfully! Clearance receipt issued.`, 'success');
      }
    }

    function handleFileCase(e) {
      e.preventDefault();
      const veh = document.getElementById('polVeh').value;
      const ruleElem = document.getElementById('polRule');
      const fine = parseInt(ruleElem.value);
      const ruleText = ruleElem.options[ruleElem.selectedIndex].text.split('(')[0].trim();
      const cId = 'CHN-' + Math.floor(10000 + Math.random() * 90000);

      challans.push({
        id: cId,
        veh: veh,
        rule: ruleText,
        fine: fine,
        date: new Date().toISOString().split('T')[0],
        status: "Unpaid"
      });

      e.target.reset();
      showToast(`E-Challan ${cId} issued against ${veh}!`, 'success');
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-26")

def generate_exp_27(base_dir):
    exp = EXPERIMENTS[26]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 27: Bus Pass Management System with QR Code</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .pass-card { border:2px solid var(--primary); border-radius:var(--radius); padding:1.5rem; background:#fff; max-width:480px; margin:0 auto; box-shadow:var(--shadow); position:relative; }
    .pass-qr { width:120px; height:120px; border:2px dashed var(--primary); display:flex; align-items:center; justify-content:center; font-size:2rem; margin:1rem auto; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128652;</div>
        <span>MetroBus Pass Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 27</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Bus Pass Management System with QR Code</h1>
        <p class="lab-hero-desc">Digital bus pass issuing system: Student concession passes (free for govt schools), Route commuter passes, monthly wallet deduction renewal, QR pass generation, and bus conductor verification scanner.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="applyTab">&#128221; Apply for Bus Pass</button>
        <button class="tab-btn" data-tab="viewPassTab">&#127915; My Digital QR Pass</button>
        <button class="tab-btn" data-tab="conductorTab">&#128247; Conductor QR Scanner</button>
      </div>

      <!-- Apply Tab -->
      <div id="applyTab" class="tab-pane active">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Application for Digital Bus Concession Pass</div>
          <div class="card-body">
            <form onsubmit="handleApplyPass(event)">
              <div class="form-group">
                <label class="form-label">Full Name of Candidate</label>
                <input type="text" id="pName" class="form-control" value="Aakif" required>
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Pass Category</label>
                  <select id="pCategory" class="form-select" onchange="updateFeePreview()">
                    <option value="free">Government School Student (100% Free)</option>
                    <option value="student">College Student Concession (Rs. 250 / mo)</option>
                    <option value="route">Route Employee Pass (Rs. 600 / mo)</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">Institution / Employer Name</label>
                  <input type="text" id="pInst" class="form-control" value="Anna University" required>
                </div>
              </div>
              <div class="grid grid-2">
                <div class="form-group">
                  <label class="form-label">Starting Bus Stop</label>
                  <input type="text" id="pFrom" class="form-control" value="Guindy" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Destination Stop</label>
                  <input type="text" id="pTo" class="form-control" value="Tambaram" required>
                </div>
              </div>
              <div id="passFeeNote" style="margin-bottom:1rem; font-weight:bold; color:var(--primary);">
                Payable Fee: Rs. 0 (Free for Govt School Students)
              </div>
              <button type="submit" class="btn btn-primary btn-block">Submit Bus Pass Application</button>
            </form>
          </div>
        </div>
      </div>

      <!-- View Pass Tab -->
      <div id="viewPassTab" class="tab-pane">
        <div class="pass-card">
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border); padding-bottom:0.5rem;">
            <strong>METROPOLITAN TRANSPORT BUS PASS</strong>
            <span class="badge badge-success">ACTIVE</span>
          </div>
          <div class="pass-qr">
            &#9638;&#9638;&#9638;
          </div>
          <div style="font-size:0.9rem; line-height:1.6;">
            <div><strong>Pass Holder:</strong> Aakif</div>
            <div><strong>Category:</strong> College Student Concession</div>
            <div><strong>Route:</strong> Guindy &harr; Tambaram (Route 52B)</div>
            <div><strong>Valid Period:</strong> Till 2026-12-31</div>
          </div>
          <button class="btn btn-sm btn-outline btn-block" style="margin-top:1rem;" onclick="showToast('Monthly renewal processed via e-Wallet!', 'success')">Renew Pass for Next Month</button>
        </div>
      </div>

      <!-- Conductor Tab -->
      <div id="conductorTab" class="tab-pane">
        <div class="card" style="max-width:650px; margin:0 auto;">
          <div class="card-header">Bus Conductor QR Validation Terminal</div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">Scan Pass ID / QR Data</label>
              <div style="display:flex; gap:0.5rem;">
                <input type="text" id="condScan" class="form-control" value="PASS-STU-2026-401">
                <button class="btn btn-primary" onclick="verifyConductor()">Verify Pass</button>
              </div>
            </div>
            <div id="condResult" style="display:none; padding:1.25rem; background:var(--surface-2); border-radius:var(--radius); margin-top:1.5rem;">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-27: Bus Pass Management System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function updateFeePreview() {
      const cat = document.getElementById('pCategory').value;
      const note = document.getElementById('passFeeNote');
      if (cat === 'free') note.textContent = "Payable Fee: Rs. 0 (Free for Govt School Students)";
      else if (cat === 'student') note.textContent = "Payable Fee: Rs. 250 / Month";
      else note.textContent = "Payable Fee: Rs. 600 / Month";
    }

    function handleApplyPass(e) {
      e.preventDefault();
      showToast('Bus pass issued with dynamic QR Code! Access in "My Digital QR Pass".', 'success');
    }

    function verifyConductor() {
      const q = document.getElementById('condScan').value;
      const res = document.getElementById('condResult');
      res.style.display = 'block';
      res.innerHTML = `
        <div style="color:var(--success); font-weight:800; font-size:1.1rem; margin-bottom:0.5rem;">&#9989; PASS AUTHENTICATED & VALID</div>
        <div style="font-size:0.9rem;">
          <strong>Pass ID:</strong> ${q}<br>
          <strong>Route:</strong> Guindy to Tambaram &bull; Student Concession Pass<br>
          <strong>Validity:</strong> Active (Expires 31-Dec-2026)
        </div>
      `;
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-27")

def generate_exp_28(base_dir):
    exp = EXPERIMENTS[27]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 28: ArtistryHub - Emily Harris Artist Portfolio</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .art-card { border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; background:#fff; display:flex; flex-direction:column; }
    .art-img { height:200px; background:linear-gradient(135deg, #a855f7, #6366f1); display:flex; align-items:center; justify-content:center; color:#fff; font-size:4rem; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#a855f7;">&#127912;</div>
        <span>ArtistryHub &bull; Emily Harris</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 28</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">ArtistryHub - Portfolio of Emily Harris</h1>
        <p class="lab-hero-desc">Bespoke portfolio celebrating renowned visual artist Emily Harris: high-res artwork gallery, career biography timeline, publications bibliography, media interviews, and exhibition events.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="galleryTab">&#127912; Art Gallery</button>
        <button class="tab-btn" data-tab="bioTab">&#128100; Artist Biography</button>
        <button class="tab-btn" data-tab="biblioTab">&#128218; Bibliography</button>
        <button class="tab-btn" data-tab="eventsTab">&#128197; Exhibitions & Press</button>
      </div>

      <!-- Gallery Tab -->
      <div id="galleryTab" class="tab-pane active">
        <div class="grid grid-3">
          <div class="art-card">
            <div class="art-img">&#127749;</div>
            <div style="padding:1.25rem;">
              <h4 style="margin:0 0 0.35rem 0;">Whispers of Dawn (2024)</h4>
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Oil on Belgian Linen &bull; 48 x 60 in</p>
              <button class="btn btn-sm btn-primary" onclick="showToast('Viewing high-resolution canvas detail...', 'info')">View Artwork</button>
            </div>
          </div>
          <div class="art-card">
            <div class="art-img" style="background:linear-gradient(135deg, #0ea5e9, #38bdf8);">&#127754;</div>
            <div style="padding:1.25rem;">
              <h4 style="margin:0 0 0.35rem 0;">Echoes of Solitude (2025)</h4>
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Mixed Media Acrylic & 24K Gold Leaf</p>
              <button class="btn btn-sm btn-primary" onclick="showToast('Viewing high-resolution canvas detail...', 'info')">View Artwork</button>
            </div>
          </div>
          <div class="art-card">
            <div class="art-img" style="background:linear-gradient(135deg, #f59e0b, #ef4444);">&#127774;</div>
            <div style="padding:1.25rem;">
              <h4 style="margin:0 0 0.35rem 0;">Autumnal Reverie (2026)</h4>
              <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Textured Impasto on Wood</p>
              <button class="btn btn-sm btn-primary" onclick="showToast('Viewing high-resolution canvas detail...', 'info')">View Artwork</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Bio Tab -->
      <div id="bioTab" class="tab-pane">
        <div class="card" style="max-width:800px; margin:0 auto;">
          <div class="card-header">About the Artist: Emily Harris</div>
          <div class="card-body">
            <p style="font-size:0.95rem; line-height:1.7; color:var(--text-main); margin-bottom:1rem;">Emily Harris is a contemporary visual painter recognized for her atmospheric landscapes and expressive impasto textures. Educated at the Royal Academy of Arts, her work has been showcased in major retrospectives in London, Paris, and Tokyo.</p>
            <p style="font-size:0.95rem; line-height:1.7; color:var(--text-muted);">Her creative philosophy explores the fragile harmony between untouched natural landscapes and transient human emotions.</p>
          </div>
        </div>
      </div>

      <!-- Bibliography Tab -->
      <div id="biblioTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Monographs & Exhibition Catalogs</div>
          <div class="card-body" style="padding:0;">
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Title of Publication</th>
                    <th>Publisher</th>
                    <th>Year</th>
                    <th>ISBN</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><em>Emily Harris: Light and Form</em></td>
                    <td>Thames & Hudson</td>
                    <td>2023</td>
                    <td>978-0500294819</td>
                  </tr>
                  <tr>
                    <td><em>The Texture of Memory</em></td>
                    <td>Phaidon Press</td>
                    <td>2025</td>
                    <td>978-1838661205</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Events Tab -->
      <div id="eventsTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Upcoming Solo Exhibitions</div>
          <div class="card-body">
            <p><strong>Spring Retrospective:</strong> Tate Modern, London &bull; April 12 &ndash; May 20, 2027</p>
            <p><strong>Art Basel Guest Showcase:</strong> Basel, Switzerland &bull; September 2027</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-28: ArtistryHub Emily Harris Portfolio</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-28")

def generate_exp_29(base_dir):
    exp = EXPERIMENTS[28]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 29: Event Landing & Registration Page</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .speaker-card { border:1px solid var(--border); border-radius:var(--radius); padding:1.25rem; background:#fff; text-align:center; }
    .speaker-img { width:80px; height:80px; border-radius:50%; background:var(--primary-light); color:var(--primary); font-size:2.2rem; display:flex; align-items:center; justify-content:center; margin:0 auto 0.75rem auto; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#127919;</div>
        <span>TechCon Global 2026</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 29</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">TechCon 2026: Future of Internet Engineering</h1>
        <p class="lab-hero-desc">Featured keynote speakers, chunked schedule sessions, venue coordinates, target audience definition, and participant registration.</p>
      </div>

      <!-- Speakers Chunk -->
      <h3 style="margin-bottom:1rem;">Distinguished Keynote Speakers</h3>
      <div class="grid grid-3" style="margin-bottom:2rem;">
        <div class="speaker-card">
          <div class="speaker-img">&#128104;&#8205;&#128187;</div>
          <h4 style="margin:0;">Dr. Alex Rivera</h4>
          <div style="font-size:0.85rem; color:var(--primary);">Chief Web Architect, Google Cloud</div>
          <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.35rem;">Topic: "Hyper-Scalable Web Systems & HTTP/3"</p>
        </div>
        <div class="speaker-card">
          <div class="speaker-img">&#128105;&#8205;&#128187;</div>
          <h4 style="margin:0;">Elena Rostova</h4>
          <div style="font-size:0.85rem; color:var(--primary);">Head of AI Infrastructure, DeepMind</div>
          <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.35rem;">Topic: "Autonomous Agentic Web Workflows"</p>
        </div>
        <div class="speaker-card">
          <div class="speaker-img">&#128104;&#8205;&#9877;</div>
          <h4 style="margin:0;">Marcus Vance</h4>
          <div style="font-size:0.85rem; color:var(--primary);">Principal Security Officer, Cloudflare</div>
          <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.35rem;">Topic: "Next-Gen Cryptography & Zero-Trust"</p>
        </div>
      </div>

      <!-- Schedule Chunk -->
      <div class="card" style="margin-bottom:2rem;">
        <div class="card-header">Conference Schedule & Chunked Timeline</div>
        <div class="card-body">
          <div class="grid grid-2">
            <div>
              <h4 style="color:var(--primary);">Morning Sessions (09:00 - 13:00)</h4>
              <p style="font-size:0.9rem; margin-top:0.5rem;">
                &bull; 09:00 AM: Welcome & Inaugural Address<br>
                &bull; 10:00 AM: Keynote by Dr. Alex Rivera<br>
                &bull; 11:30 AM: Panel Discussion: Future of Full-Stack Architecture
              </p>
            </div>
            <div>
              <h4 style="color:var(--secondary);">Afternoon Sessions (14:00 - 18:00)</h4>
              <p style="font-size:0.9rem; margin-top:0.5rem;">
                &bull; 02:00 PM: Agentic AI Hands-on Workshop<br>
                &bull; 04:00 PM: Research Paper Presentations<br>
                &bull; 05:30 PM: Networking Gala & Valedictory
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Registration Form Chunk -->
      <div class="card" style="max-width:650px; margin:0 auto;">
        <div class="card-header">Register for Conference Pass</div>
        <div class="card-body">
          <form onsubmit="handleEventReg(event)">
            <div class="form-group">
              <label class="form-label">Attendee Full Name</label>
              <input type="text" id="regName" class="form-control" value="Aakif" required>
            </div>
            <div class="grid grid-2">
              <div class="form-group">
                <label class="form-label">Email ID</label>
                <input type="email" id="regEmail" class="form-control" value="aakif@college.edu" required>
              </div>
              <div class="form-group">
                <label class="form-label">Pass Tier</label>
                <select id="regTier" class="form-select">
                  <option>Student Delegate (Free)</option>
                  <option>Professional Pass ($150)</option>
                  <option>VIP All-Access ($300)</option>
                </select>
              </div>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Confirm Registration</button>
          </form>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-29: Event Landing & Registration Page</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function handleEventReg(e) {
      e.preventDefault();
      const name = document.getElementById('regName').value;
      const tier = document.getElementById('regTier').value;
      showToast(`Conference badge issued for ${name} (${tier})!`, 'success');
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-29")

def generate_exp_30(base_dir):
    exp = EXPERIMENTS[29]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 30: IJSSE - Academic Journal Publishing Portal</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#0f766e;">&#128218;</div>
        <span>IJSSE Scopus Journal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 30</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">International Journal of Scientific & Social Excellence</h1>
        <p class="lab-hero-desc">Scopus Indexed Peer-Reviewed Publisher &bull; Print ISSN: <strong>2395-1443</strong> &bull; Online ISSN: <strong>2395-1451</strong>. Dedicated portals for Authors, Peer Reviewers, and Editors.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="authorTab">&#128221; For Authors</button>
        <button class="tab-btn" data-tab="reviewerTab">&#128269; For Reviewers</button>
        <button class="tab-btn" data-tab="editorTab">&#128188; For Editors</button>
        <button class="tab-btn" data-tab="archiveTab">&#128218; Current Issue & Archive</button>
      </div>

      <!-- Author Tab -->
      <div id="authorTab" class="tab-pane active">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Submit Manuscript to IJSSE</div>
            <div class="card-body">
              <form onsubmit="handleSubmitPaper(event)">
                <div class="form-group">
                  <label class="form-label">Manuscript Title</label>
                  <input type="text" id="paperTitle" class="form-control" required placeholder="e.g. Distributed Consensus in Cloud Computing">
                </div>
                <div class="form-group">
                  <label class="form-label">Authors & Affiliations</label>
                  <input type="text" id="paperAuthors" class="form-control" value="Aakif, Dr. M. Ramanathan" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Abstract</label>
                  <textarea id="paperAbstract" class="form-control" rows="3" required placeholder="State research problem, methodology, and empirical findings..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Submit Manuscript for Peer Review</button>
              </form>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Author Instructions & Templates</div>
            <div class="card-body">
              <p style="font-size:0.9rem; margin-bottom:1rem;">Authors must follow double-blind review standards. Download IEEE/IJSSE standard LaTeX and Word templates.</p>
              <div style="display:flex; flex-direction:column; gap:0.5rem;">
                <button class="btn btn-outline" onclick="showToast('Downloading IJSSE_Template.docx...', 'info')">&#128229; Download Article Template (.docx)</button>
                <button class="btn btn-outline" onclick="showToast('Downloading Copyright_Form.pdf...', 'info')">&#128229; Download Copyright Agreement (.pdf)</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviewer Tab -->
      <div id="reviewerTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Reviewer Queue & Scoring Rubric</div>
          <div class="card-body" id="reviewerQueue">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>

      <!-- Editor Tab -->
      <div id="editorTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Editorial Board Decision Desk</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Manage manuscript reviewer allocations, examine similarity plagiarism reports, and issue final publication verdicts.</p>
          </div>
        </div>
      </div>

      <!-- Archive Tab -->
      <div id="archiveTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Vol. 12 No. 4 (2026): Published Articles</div>
          <div class="card-body">
            <div style="border-bottom:1px solid var(--border); padding-bottom:1rem; margin-bottom:1rem;">
              <h4 style="margin:0 0 0.25rem 0;">1. Scalable Microservice Communication Protocols for IoT Fog Networks</h4>
              <div style="font-size:0.85rem; color:var(--text-muted);">Authors: S. Venkatesh, K. Alagappan &bull; DOI: 10.2395/ijsse.2026.0401</div>
              <p style="font-size:0.9rem; margin-top:0.35rem;">Published Open Access &bull; Citations: 14</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-30: IJSSE Academic Journal Publishing Portal</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let papers = [
      { id: "MS-842", title: "Distributed Consensus in Cloud Computing", authors: "Aakif, Dr. M. Ramanathan", status: "Under Review" }
    ];

    function handleSubmitPaper(e) {
      e.preventDefault();
      const title = document.getElementById('paperTitle').value;
      const authors = document.getElementById('paperAuthors').value;
      const msId = 'MS-' + Math.floor(100 + Math.random() * 900);

      papers.push({ id: msId, title, authors, status: "Under Review" });
      renderReviewerQueue();
      showToast(`Manuscript ${msId} received! Acknowledgement email sent.`, 'success');
      e.target.reset();
    }

    function renderReviewerQueue() {
      const q = document.getElementById('reviewerQueue');
      q.innerHTML = '';
      papers.forEach(p => {
        const div = document.createElement('div');
        div.style.padding = '1rem';
        div.style.border = '1px solid var(--border)';
        div.style.borderRadius = 'var(--radius)';
        div.style.marginBottom = '0.75rem';
        div.innerHTML = `
          <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
            <strong>${p.id}: ${p.title}</strong>
            <span class="badge badge-primary">${p.status}</span>
          </div>
          <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Authors: ${p.authors}</div>
          <button class="btn btn-sm btn-success" onclick="acceptPaper('${p.id}')">Submit Acceptance Verdict</button>
        `;
        q.appendChild(div);
      });
    }

    function acceptPaper(id) {
      const p = papers.find(item => item.id === id);
      if (p) {
        p.status = "Accepted for Publication";
        renderReviewerQueue();
        showToast(`Paper ${id} marked Accepted for upcoming volume!`, 'success');
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderReviewerQueue();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-30")

def run_all(base_dir="LAB"):
    generate_exp_21(base_dir)
    generate_exp_22(base_dir)
    generate_exp_23(base_dir)
    generate_exp_24(base_dir)
    generate_exp_25(base_dir)
    generate_exp_26(base_dir)
    generate_exp_27(base_dir)
    generate_exp_28(base_dir)
    generate_exp_29(base_dir)
    generate_exp_30(base_dir)
    print("Batch 3 completed (Exp 21 to 30).")

if __name__ == "__main__":
    run_all()
