# modules/exp_41_46.py
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

def generate_exp_41(base_dir):
    exp = EXPERIMENTS[40]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 41: CulinaryDelight - Digital Recipe Book</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#ea580c;">&#127859;</div>
        <span>CulinaryDelight Recipes</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 41</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">CulinaryDelight - Digital Recipe Book</h1>
        <p class="lab-hero-desc">Interactive culinary guide: dynamic serving size scaler, step-by-step cooking mode, ingredient measurement auto-adjustment, ratings, and meal planner.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="recipeTab">&#127859; Featured Recipe</button>
        <button class="tab-btn" data-tab="plannerTab">&#128197; Weekly Meal Planner</button>
      </div>

      <div id="recipeTab" class="tab-pane active">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">
              <span>Classic Creamy Tuscan Garlic Chicken</span>
              <span class="badge badge-primary">Italian &bull; 30 Mins</span>
            </div>
            <div class="card-body">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; padding:0.75rem; background:var(--surface-2); border-radius:var(--radius);">
                <strong>Adjust Serving Count:</strong>
                <div style="display:flex; gap:0.5rem; align-items:center;">
                  <button class="btn btn-sm btn-outline" onclick="scaleServings(-1)">-</button>
                  <span id="servingCountLabel" style="font-weight:800; font-size:1.1rem;">2</span>
                  <button class="btn btn-sm btn-outline" onclick="scaleServings(1)">+</button>
                </div>
              </div>

              <h4 style="margin-bottom:0.5rem;">Ingredients List (Scaled):</h4>
              <ul id="ingredientsList" style="padding-left:1.25rem; font-size:0.9rem; line-height:1.7;">
                <!-- Populated by JS -->
              </ul>
            </div>
          </div>

          <div class="card">
            <div class="card-header">Step-by-Step Cooking Instructions</div>
            <div class="card-body">
              <ol style="padding-left:1.25rem; font-size:0.9rem; line-height:1.8;">
                <li>Season chicken breasts with sea salt, pepper, and dried oregano.</li>
                <li>In a large skillet over medium-high heat, heat olive oil and sear chicken 5 mins per side until golden.</li>
                <li>Remove chicken; add minced garlic, sundried tomatoes, and fresh spinach to skillet.</li>
                <li>Pour heavy cream and simmer for 3 minutes until sauce thickens.</li>
                <li>Return chicken to pan, spoon sauce over, and garnish with fresh basil.</li>
              </ol>
              <button class="btn btn-primary btn-block" style="margin-top:1.5rem;" onclick="showToast('Shopping list added to device clipboard!', 'success')">&#128203; Export Ingredients to Shopping List</button>
            </div>
          </div>
        </div>
      </div>

      <div id="plannerTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Weekly Meal Plan Schedule</div>
          <div class="card-body">
            <p><strong>Monday Dinner:</strong> Tuscan Garlic Chicken</p>
            <p><strong>Tuesday Dinner:</strong> Mediterranean Grilled Vegetable Salad</p>
            <p><strong>Wednesday Dinner:</strong> Slow-Cooked Basil Pesto Salmon</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-41: CulinaryDelight Digital Recipe Book</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let baseIngredients = [
      { name: "Boneless Chicken Breast", qty: 250, unit: "g" },
      { name: "Heavy Whipping Cream", qty: 100, unit: "ml" },
      { name: "Fresh Baby Spinach", qty: 50, unit: "g" },
      { name: "Sundried Tomatoes", qty: 40, unit: "g" },
      { name: "Garlic Cloves (Minced)", qty: 3, unit: "cloves" }
    ];

    let currentServings = 2;

    function renderIngredients() {
      const ul = document.getElementById('ingredientsList');
      ul.innerHTML = '';
      const mult = currentServings / 2;
      baseIngredients.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${Math.round(item.qty * mult)} ${item.unit} ${item.name}`;
        ul.appendChild(li);
      });
      document.getElementById('servingCountLabel').textContent = currentServings;
    }

    function scaleServings(delta) {
      if (currentServings + delta >= 1 && currentServings + delta <= 12) {
        currentServings += delta;
        renderIngredients();
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderIngredients();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-41")

def generate_exp_42(base_dir):
    exp = EXPERIMENTS[41]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 42: Online Electricity Bill Payment System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#eab308; color:#000;">&#9889;</div>
        <span>PowerGrid EB Billing Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 42</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Online Electricity Bill Payment System</h1>
        <p class="lab-hero-desc">Exact tariff calculation formulas for Domestic & Commercial connections, bi-monthly billing duration, overdue fine computation (Rs. 10/day), and payment receipt generator.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="consumerTab">&#9889; Consumer Bill & Payment</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Electricity Board Admin Formula</button>
      </div>

      <!-- Consumer Tab -->
      <div id="consumerTab" class="tab-pane active">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Calculate & Pay Electricity Bill</div>
            <div class="card-body">
              <form onsubmit="handleCalculateEB(event)">
                <div class="form-group">
                  <label class="form-label">Consumer Number</label>
                  <input type="text" id="ebConsumer" class="form-control" value="04-201-9842" required>
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Connection Type</label>
                    <select id="ebConnType" class="form-select" onchange="calcEB()">
                      <option value="domestic">Domestic Connection</option>
                      <option value="commercial">Commercial Connection</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Consumed Units (kWh)</label>
                    <input type="number" id="ebUnits" class="form-control" value="320" required oninput="calcEB()">
                  </div>
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Bill Due Date</label>
                    <input type="date" id="ebDueDate" class="form-control" onchange="calcEB()">
                  </div>
                  <div class="form-group">
                    <label class="form-label">Payment Date</label>
                    <input type="date" id="ebPayDate" class="form-control" onchange="calcEB()">
                  </div>
                </div>
                <button type="button" class="btn btn-primary btn-block" onclick="payEB()">Pay Electricity Bill Online</button>
              </form>
            </div>
          </div>

          <!-- Bill Summary Display -->
          <div class="card">
            <div class="card-header">Tariff Slab Breakdown & Net Payable</div>
            <div class="card-body">
              <div id="ebBreakdown" style="font-size:0.9rem; line-height:1.7;">
                <!-- Populated by JS -->
              </div>
              <div style="margin-top:1.5rem; padding:1rem; background:var(--surface-2); border-radius:var(--radius); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:1.1rem; font-weight:bold;">Net Payable:</span>
                <span style="font-size:1.6rem; font-weight:800; color:var(--primary);" id="ebNetPayable">Rs. 0</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Statutory Tariff Slab Norms (Board Approved)</div>
          <div class="card-body">
            <div class="grid grid-2">
              <div style="padding:1rem; border:1px solid var(--border); border-radius:var(--radius);">
                <h4 style="color:var(--primary); margin-bottom:0.5rem;">Domestic Connection Slabs</h4>
                <p style="font-size:0.85rem; line-height:1.6;">
                  &bull; 1 to 100 Units: <strong>Rs. 1.00 / unit</strong><br>
                  &bull; 101 to 200 Units: <strong>Rs. 2.50 / unit</strong><br>
                  &bull; 201 to 500 Units: <strong>Rs. 4.00 / unit</strong><br>
                  &bull; 501+ Units: <strong>Rs. 6.00 / unit</strong>
                </p>
              </div>
              <div style="padding:1rem; border:1px solid var(--border); border-radius:var(--radius);">
                <h4 style="color:var(--secondary); margin-bottom:0.5rem;">Commercial Connection Slabs</h4>
                <p style="font-size:0.85rem; line-height:1.6;">
                  &bull; 1 to 100 Units: <strong>Rs. 2.00 / unit</strong><br>
                  &bull; 101 to 200 Units: <strong>Rs. 4.50 / unit</strong><br>
                  &bull; 201 to 500 Units: <strong>Rs. 6.00 / unit</strong><br>
                  &bull; 501+ Units: <strong>Rs. 7.00 / unit</strong>
                </p>
              </div>
            </div>
            <div style="margin-top:1rem; font-size:0.85rem; color:var(--text-muted);">
              &bull; <strong>Late Fine:</strong> Rs. 10.00 added as fine for each day after the last payment due date.
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-42: Online Electricity Bill Payment System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function calcEB() {
      const type = document.getElementById('ebConnType').value;
      const units = parseFloat(document.getElementById('ebUnits').value) || 0;
      const dueDate = new Date(document.getElementById('ebDueDate').value);
      const payDate = new Date(document.getElementById('ebPayDate').value);

      let energyCharge = 0;
      let slabHtml = '';

      if (type === 'domestic') {
        if (units <= 100) {
          energyCharge = units * 1.0;
          slabHtml += `<div>Slab 1 (0-100 u @ Rs. 1.00): Rs. ${energyCharge.toFixed(2)}</div>`;
        } else if (units <= 200) {
          energyCharge = (100 * 1.0) + ((units - 100) * 2.5);
          slabHtml += `<div>Slab 1 (100 u @ Rs. 1.00): Rs. 100.00</div>`;
          slabHtml += `<div>Slab 2 (${units - 100} u @ Rs. 2.50): Rs. ${((units - 100) * 2.5).toFixed(2)}</div>`;
        } else if (units <= 500) {
          energyCharge = (100 * 1.0) + (100 * 2.5) + ((units - 200) * 4.0);
          slabHtml += `<div>Slab 1 (100 u @ Rs. 1.00): Rs. 100.00</div>`;
          slabHtml += `<div>Slab 2 (100 u @ Rs. 2.50): Rs. 250.00</div>`;
          slabHtml += `<div>Slab 3 (${units - 200} u @ Rs. 4.00): Rs. ${((units - 200) * 4.0).toFixed(2)}</div>`;
        } else {
          energyCharge = (100 * 1.0) + (100 * 2.5) + (300 * 4.0) + ((units - 500) * 6.0);
          slabHtml += `<div>Slab 1 (100 u @ Rs. 1.00): Rs. 100.00</div>`;
          slabHtml += `<div>Slab 2 (100 u @ Rs. 2.50): Rs. 250.00</div>`;
          slabHtml += `<div>Slab 3 (300 u @ Rs. 4.00): Rs. 1200.00</div>`;
          slabHtml += `<div>Slab 4 (${units - 500} u @ Rs. 6.00): Rs. ${((units - 500) * 6.0).toFixed(2)}</div>`;
        }
      } else {
        // Commercial
        if (units <= 100) {
          energyCharge = units * 2.0;
          slabHtml += `<div>Slab 1 (0-100 u @ Rs. 2.00): Rs. ${energyCharge.toFixed(2)}</div>`;
        } else if (units <= 200) {
          energyCharge = (100 * 2.0) + ((units - 100) * 4.5);
          slabHtml += `<div>Slab 1 (100 u @ Rs. 2.00): Rs. 200.00</div>`;
          slabHtml += `<div>Slab 2 (${units - 100} u @ Rs. 4.50): Rs. ${((units - 100) * 4.5).toFixed(2)}</div>`;
        } else if (units <= 500) {
          energyCharge = (100 * 2.0) + (100 * 4.5) + ((units - 200) * 6.0);
          slabHtml += `<div>Slab 1 (100 u @ Rs. 2.00): Rs. 200.00</div>`;
          slabHtml += `<div>Slab 2 (100 u @ Rs. 4.50): Rs. 450.00</div>`;
          slabHtml += `<div>Slab 3 (${units - 200} u @ Rs. 6.00): Rs. ${((units - 200) * 4.0).toFixed(2)}</div>`;
        } else {
          energyCharge = (100 * 2.0) + (100 * 4.5) + (300 * 6.0) + ((units - 500) * 7.0);
          slabHtml += `<div>Slab 1 (100 u @ Rs. 2.00): Rs. 200.00</div>`;
          slabHtml += `<div>Slab 2 (100 u @ Rs. 4.50): Rs. 450.00</div>`;
          slabHtml += `<div>Slab 3 (300 u @ Rs. 6.00): Rs. 1800.00</div>`;
          slabHtml += `<div>Slab 4 (${units - 500} u @ Rs. 7.00): Rs. ${((units - 500) * 7.0).toFixed(2)}</div>`;
        }
      }

      // Late fine calculation: Rs. 10/day after last date
      let fine = 0;
      let diffDays = 0;
      if (payDate > dueDate) {
        diffDays = Math.ceil((payDate - dueDate) / (1000 * 60 * 60 * 24));
        fine = diffDays * 10;
        slabHtml += `<div style="color:var(--danger); font-weight:bold; margin-top:0.5rem;">Overdue Fine (${diffDays} days @ Rs. 10/day): Rs. ${fine}.00</div>`;
      } else {
        slabHtml += `<div style="color:var(--success); margin-top:0.5rem;">Payment within due date &bull; Late Fine: Rs. 0</div>`;
      }

      const net = energyCharge + fine;
      document.getElementById('ebBreakdown').innerHTML = slabHtml;
      document.getElementById('ebNetPayable').textContent = 'Rs. ' + net.toFixed(2);
    }

    function payEB() {
      const net = document.getElementById('ebNetPayable').textContent;
      showToast(`Payment of ${net} successful! Official receipt generated.`, 'success');
    }

    document.addEventListener('DOMContentLoaded', () => {
      const today = new Date();
      const due = new Date(today.getTime() - 2*24*60*60*1000); // 2 days past due to test fine
      document.getElementById('ebDueDate').value = due.toISOString().split('T')[0];
      document.getElementById('ebPayDate').value = today.toISOString().split('T')[0];
      calcEB();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-42")

def generate_exp_43(base_dir):
    exp = EXPERIMENTS[42]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 43: Online Placement Examination System</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .timer-badge { font-size:1.4rem; font-weight:800; color:var(--danger); background:var(--danger-bg); padding:0.4rem 1rem; border-radius:var(--radius); border:1px solid #fecaca; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon">&#128221;</div>
        <span>Placement Exam Portal</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 43</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Online Placement Examination System</h1>
        <p class="lab-hero-desc">Admin exam scheduling & question bank, candidate timed test interface with real-time countdown timer, automated evaluation, scorecard generation, and ranking list.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="examTab">&#9997; Attempt Placement Exam</button>
        <button class="tab-btn" data-tab="scorecardTab">&#127942; Scorecard & Merit Ranking</button>
      </div>

      <!-- Exam Tab -->
      <div id="examTab" class="tab-pane active">
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-body" style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <h3 style="margin:0;">Campus Recruitment Aptitude & Coding Test</h3>
              <div style="font-size:0.85rem; color:var(--text-muted);">Candidate: Aakif (21CS042)</div>
            </div>
            <div class="timer-badge" id="examTimer">14:59</div>
          </div>
        </div>

        <div class="card" style="max-width:800px; margin:0 auto;">
          <div class="card-body" id="questionsContainer">
            <div style="margin-bottom:1.5rem;">
              <p><strong>1. What is the time complexity of searching an element in a balanced Binary Search Tree (AVL / Red-Black)?</strong></p>
              <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:0.5rem;">
                <label><input type="radio" name="pq1" value="A"> O(N)</label>
                <label><input type="radio" name="pq1" value="B" id="q1Ans"> O(log N)</label>
                <label><input type="radio" name="pq1" value="C"> O(1)</label>
              </div>
            </div>

            <div style="margin-bottom:1.5rem;">
              <p><strong>2. In JavaScript, which mechanism moves variable and function declarations to the top of their scope before code execution?</strong></p>
              <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:0.5rem;">
                <label><input type="radio" name="pq2" value="A" id="q2Ans"> Hoisting</label>
                <label><input type="radio" name="pq2" value="B"> Memoization</label>
                <label><input type="radio" name="pq2" value="C"> Event Bubbling</label>
              </div>
            </div>

            <button class="btn btn-primary btn-block btn-lg" onclick="finishExam()">Submit Placement Test</button>
          </div>
        </div>
      </div>

      <!-- Scorecard Tab -->
      <div id="scorecardTab" class="tab-pane">
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">Candidate Performance Scorecard & Leaderboard</div>
          <div class="card-body">
            <div id="scorecardResult" style="padding:1.5rem; background:var(--surface-2); border-radius:var(--radius); margin-bottom:1.5rem; text-align:center;">
              <div style="font-size:0.9rem; color:var(--text-muted);">Test Score:</div>
              <div style="font-size:2.5rem; font-weight:800; color:var(--success);" id="userScoreDisplay">Pending Submission</div>
              <div id="userPercentile">Attempt the test to view rank</div>
            </div>

            <h4 style="margin-bottom:0.75rem;">Placement Rank List</h4>
            <div class="table-responsive" style="border:none;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Candidate</th>
                    <th>Roll Number</th>
                    <th>Score</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>#1</strong></td>
                    <td>Aakif</td>
                    <td>21CS042</td>
                    <td>100%</td>
                    <td><span class="badge badge-success">Selected</span></td>
                  </tr>
                  <tr>
                    <td><strong>#2</strong></td>
                    <td>Rohan M.</td>
                    <td>21CS089</td>
                    <td>90%</td>
                    <td><span class="badge badge-success">Selected</span></td>
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
      <p>Internet Programming Lab &bull; Exp-43: Online Placement Examination System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let timerSec = 899;
    setInterval(() => {
      if (timerSec > 0) {
        timerSec--;
        const m = Math.floor(timerSec / 60);
        const s = timerSec % 60;
        document.getElementById('examTimer').textContent = `${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
      }
    }, 1000);

    function finishExam() {
      let score = 0;
      if (document.getElementById('q1Ans').checked) score += 50;
      if (document.getElementById('q2Ans').checked) score += 50;

      document.getElementById('userScoreDisplay').textContent = `${score}% (Passed)`;
      document.getElementById('userPercentile').innerHTML = `<strong style="color:var(--success);">Rank: #1 &bull; Percentile: 99.4% &bull; Shortlisted for Interview Round</strong>`;
      showToast(`Test evaluated! Score: ${score}%. Access Scorecard tab.`, 'success');
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-43")

def generate_exp_44(base_dir):
    exp = EXPERIMENTS[43]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 44: Painting Rating and Review Web Application</title>
  <link rel="stylesheet" href="../assets/common.css">
  <style>
    .star-btn { font-size:1.8rem; cursor:pointer; color:#cbd5e1; transition:color 0.2s; }
    .star-btn.active { color:#f59e0b; }
  </style>
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#8b5cf6;">&#127912;</div>
        <span>ArtCritique Gallery</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 44</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Painting Rating and Review Web Application</h1>
        <p class="lab-hero-desc">Art evaluation portal: Admin uploads paintings under scheduled exhibition packages; Owners monitor reviews; Customers submit 1 to 5 star ratings with positive and negative sentiment critique.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="rateTab">&#127912; Current Exhibition & Review</button>
        <button class="tab-btn" data-tab="ownerTab">&#128100; Painting Owner Dashboard</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Admin Package Manager</button>
      </div>

      <!-- Rate Tab -->
      <div id="rateTab" class="tab-pane active">
        <div class="grid grid-2">
          <div class="card">
            <div class="card-header">Exhibited Artwork: "Elysian Solitude"</div>
            <div class="card-body">
              <div style="height:220px; background:linear-gradient(135deg, #4f46e5, #ec4899); border-radius:var(--radius); display:flex; align-items:center; justify-content:center; color:#fff; font-size:4rem; margin-bottom:1rem;">
                &#127756;
              </div>
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <strong>Artist:</strong> Aanya Sengupta<br>
                  <span style="font-size:0.85rem; color:var(--text-muted);">Medium: Oil and Gold Leaf on Wood</span>
                </div>
                <div style="text-align:right;">
                  <div style="font-size:1.6rem; font-weight:800; color:var(--warning);" id="avgRatingBadge">4.8 &#9733;</div>
                  <span style="font-size:0.75rem; color:var(--text-muted);">Based on 14 Reviews</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Rating Form -->
          <div class="card">
            <div class="card-header">Submit Your Critical Review</div>
            <div class="card-body">
              <form onsubmit="handleReview(event)">
                <div class="form-group" style="text-align:center;">
                  <label class="form-label">Select Star Rating (1 to 5 Stars)</label>
                  <div style="display:flex; justify-content:center; gap:0.5rem;" id="starsContainer">
                    <span class="star-btn active" onclick="setStars(1)">&#9733;</span>
                    <span class="star-btn active" onclick="setStars(2)">&#9733;</span>
                    <span class="star-btn active" onclick="setStars(3)">&#9733;</span>
                    <span class="star-btn active" onclick="setStars(4)">&#9733;</span>
                    <span class="star-btn active" onclick="setStars(5)">&#9733;</span>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Positive Aspects / Highlights</label>
                  <input type="text" id="revPos" class="form-control" placeholder="e.g. Masterful use of lighting and emotional depth" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Constructive Critique / Negative Notes</label>
                  <input type="text" id="revNeg" class="form-control" placeholder="e.g. Background brushwork feels slightly hurried">
                </div>
                <button type="submit" class="btn btn-primary btn-block">Publish Art Review</button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Owner Tab -->
      <div id="ownerTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Painting Owner Feedback Analytics</div>
          <div class="card-body" id="reviewsFeed">
            <div style="padding:0.75rem; border-bottom:1px solid var(--border);">
              <strong>5/5 Stars:</strong> "The atmospheric color palette conveys profound serenity."<br>
              <span style="color:var(--text-muted); font-size:0.85rem;">Constructive critique: None</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Admin Exhibition Packages</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Package 1: 7-Day Display ($50) &bull; Package 2: 30-Day Curated Exhibition ($150).</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-44: Painting Rating and Review Web Application</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    let selectedRating = 5;

    function setStars(n) {
      selectedRating = n;
      const stars = document.querySelectorAll('.star-btn');
      stars.forEach((s, idx) => {
        if (idx < n) s.classList.add('active');
        else s.classList.remove('active');
      });
    }

    function handleReview(e) {
      e.preventDefault();
      const pos = document.getElementById('revPos').value;
      const neg = document.getElementById('revNeg').value || "None";
      const feed = document.getElementById('reviewsFeed');
      const div = document.createElement('div');
      div.style.padding = '0.75rem';
      div.style.borderBottom = '1px solid var(--border)';
      div.innerHTML = `<strong>${selectedRating}/5 Stars:</strong> "${pos}"<br><span style="color:var(--text-muted); font-size:0.85rem;">Constructive critique: ${neg}</span>`;
      feed.prepend(div);
      showToast('Thank you! Your critique has been submitted to the artist.', 'success');
      e.target.reset();
      setStars(5);
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-44")

def generate_exp_45(base_dir):
    exp = EXPERIMENTS[44]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 45: Income Tax Calculation Web Application</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#059669;">&#128181;</div>
        <span>TaxPortal Income Tax Calculator</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 45</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Income Tax Calculation Web Application</h1>
        <p class="lab-hero-desc">Exact statutory tax formula implementation: Gross Pay, House Rent Allowance (HRA), Standard Deduction (Rs. 50,000), Pension (capped at Rs. 150,000), Health Insurance, with exact slab calculation.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="calcTab">&#128181; Calculate Income Tax</button>
        <button class="tab-btn" data-tab="normsTab">&#128214; Statutory Slabs & Norms</button>
      </div>

      <!-- Calculator Tab -->
      <div id="calcTab" class="tab-pane active">
        <div class="grid grid-2">
          <!-- Input Form -->
          <div class="card">
            <div class="card-header">Employee Financial Details</div>
            <div class="card-body">
              <form onsubmit="handleTaxSubmit(event)">
                <div class="form-group">
                  <label class="form-label">Monthly Gross Pay (Rs.)</label>
                  <input type="number" id="taxGross" class="form-control" value="85000" required oninput="calcTax()">
                </div>
                <div class="form-group">
                  <label class="form-label">Monthly House Rent Allowance - HRA (Rs.)</label>
                  <input type="number" id="taxHra" class="form-control" value="15000" required oninput="calcTax()">
                </div>
                <div class="grid grid-2">
                  <div class="form-group">
                    <label class="form-label">Monthly Pension (Rs.)</label>
                    <input type="number" id="taxPension" class="form-control" value="10000" required oninput="calcTax()">
                    <span class="form-help">Max deduction capped at Rs. 1,50,000/yr</span>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Monthly Health Insurance (Rs.)</label>
                    <input type="number" id="taxInsurance" class="form-control" value="2500" required oninput="calcTax()">
                  </div>
                </div>
                <button type="button" class="btn btn-success btn-block" onclick="showToast('Tax Computation Sheet Downloaded!', 'success')">&#128229; Download Summary Report</button>
              </form>
            </div>
          </div>

          <!-- Tax Breakdown Output -->
          <div class="card">
            <div class="card-header">Tax Computation Statement</div>
            <div class="card-body" id="taxStatement">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>
      </div>

      <!-- Norms Tab -->
      <div id="normsTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Government Tax Calculation Norms</div>
          <div class="card-body">
            <div class="alert" style="background:var(--surface-2); border-left:4px solid var(--primary); padding:1rem; margin-bottom:1rem;">
              <strong>Net Taxable Income Formula:</strong><br>
              <code>Net Taxable Income = (Gross Pay * 12) - (HRA * 12) - 50,000 [Standard Deduction] - min(Pension * 12, 1,50,000) - (Health Insurance * 12)</code>
            </div>
            <p><strong>Tax Slab Rates:</strong></p>
            <ul style="padding-left:1.25rem; font-size:0.9rem; line-height:1.7;">
              <li>If Net Taxable Income &le; Rs. 5,00,000: <strong>Tax is NIL (Rs. 0)</strong></li>
              <li>If Net Taxable Income &gt; Rs. 5,00,000:
                <ul>
                  <li>0 to 2,50,000: <strong>0%</strong></li>
                  <li>2,50,001 to 5,00,000: <strong>5% of (Net - 2,50,000)</strong></li>
                  <li>5,00,001 to 10,00,000: <strong>Rs. 12,500 + 20% of (Net - 5,00,000)</strong></li>
                  <li>Above 10,00,000: <strong>Rs. 1,12,500 + 30% of (Net - 10,00,000)</strong></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-45: Income Tax Calculation Web Application</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function calcTax() {
      const grossMonthly = parseFloat(document.getElementById('taxGross').value) || 0;
      const hraMonthly = parseFloat(document.getElementById('taxHra').value) || 0;
      const pensionMonthly = parseFloat(document.getElementById('taxPension').value) || 0;
      const insMonthly = parseFloat(document.getElementById('taxInsurance').value) || 0;

      const annualGross = grossMonthly * 12;
      const annualHra = hraMonthly * 12;
      const standardDeduction = 50000;
      const annualPension = Math.min(pensionMonthly * 12, 150000);
      const annualInsurance = insMonthly * 12;

      const totalDeductions = annualHra + standardDeduction + annualPension + annualInsurance;
      const netTaxable = Math.max(0, annualGross - totalDeductions);

      let tax = 0;
      let slabDetails = '';

      if (netTaxable <= 500000) {
        tax = 0;
        slabDetails = '<div style="color:var(--success); font-weight:bold;">Net Taxable Income is &le; Rs. 5,00,000 &bull; Tax Liability is NIL (Rs. 0)</div>';
      } else {
        if (netTaxable <= 1000000) {
          tax = 12500 + (0.20 * (netTaxable - 500000));
          slabDetails = `<div>Slab 2 (2.5L - 5L @ 5%): Rs. 12,500.00</div><div>Slab 3 (5L - 10L @ 20%): Rs. ${(0.20 * (netTaxable - 500000)).toFixed(2)}</div>`;
        } else {
          tax = 112500 + (0.30 * (netTaxable - 1000000));
          slabDetails = `<div>Slab 2 & 3 (Up to 10L): Rs. 1,12,500.00</div><div>Slab 4 (> 10L @ 30%): Rs. ${(0.30 * (netTaxable - 1000000)).toFixed(2)}</div>`;
        }
      }

      const netSalary = annualGross - tax;

      document.getElementById('taxStatement').innerHTML = `
        <div style="font-size:0.9rem; line-height:1.7;">
          <div style="display:flex; justify-content:space-between;"><span>Annual Gross Salary:</span><strong>Rs. ${annualGross.toLocaleString()}</strong></div>
          <div style="display:flex; justify-content:space-between;"><span>Less: HRA Exemption:</span><span>- Rs. ${annualHra.toLocaleString()}</span></div>
          <div style="display:flex; justify-content:space-between;"><span>Less: Standard Deduction:</span><span>- Rs. ${standardDeduction.toLocaleString()}</span></div>
          <div style="display:flex; justify-content:space-between;"><span>Less: Pension Deduction:</span><span>- Rs. ${annualPension.toLocaleString()}</span></div>
          <div style="display:flex; justify-content:space-between;"><span>Less: Health Insurance (80D):</span><span>- Rs. ${annualInsurance.toLocaleString()}</span></div>
          <div style="border-top:1px solid var(--border); margin:0.5rem 0; padding-top:0.5rem; display:flex; justify-content:space-between;">
            <strong>Net Taxable Income:</strong>
            <strong style="color:var(--primary);">Rs. ${netTaxable.toLocaleString()}</strong>
          </div>
          <div style="margin-top:0.75rem; padding:0.75rem; background:var(--surface-2); border-radius:6px;">
            ${slabDetails}
          </div>
          <div style="border-top:2px solid var(--border); margin-top:1rem; padding-top:0.75rem; display:flex; justify-content:space-between; font-size:1.2rem;">
            <span>Total Income Tax Payable:</span>
            <strong style="color:var(--danger);">Rs. ${Math.round(tax).toLocaleString()}</strong>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:var(--text-muted); margin-top:0.35rem;">
            <span>Annual Net Take-Home Salary:</span>
            <strong>Rs. ${Math.round(netSalary).toLocaleString()}</strong>
          </div>
        </div>
      `;
    }

    function handleTaxSubmit(e) {
      e.preventDefault();
      calcTax();
    }

    document.addEventListener('DOMContentLoaded', () => {
      calcTax();
    });
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-45")

def generate_exp_46(base_dir):
    exp = EXPERIMENTS[45]
    exp_dir = os.path.join(base_dir, exp['folder'])
    os.makedirs(exp_dir, exist_ok=True)
    write_exp_readme(exp_dir, exp)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exp 46: Online Phone Bill Payment System</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header class="lab-navbar">
    <div class="lab-container lab-navbar-inner">
      <a href="../index.html" class="lab-brand">
        <div class="lab-brand-icon" style="background:#0284c7;">&#128222;</div>
        <span>TelecomPay Mobile Billing</span>
      </a>
      <div class="lab-nav-actions">
        <span class="lab-badge-exp">Experiment 46</span>
        <a href="../index.html" class="btn btn-outline btn-sm">&larr; Back to Lab Hub</a>
      </div>
    </div>
  </header>

  <main class="lab-main">
    <div class="lab-container">
      <div class="lab-hero">
        <h1 class="lab-hero-title">Online Phone Bill Payment System</h1>
        <p class="lab-hero-desc">Monthly phone billing cycle, overdue fine calculation (Rs. 10 per day after last date), flexible full or custom amount payments, and digital transaction receipts.</p>
      </div>

      <div class="tabs-header">
        <button class="tab-btn active" data-tab="billTab">&#128222; Current Phone Bill & Pay</button>
        <button class="tab-btn" data-tab="adminTab">&#9881; Telecom Billing Admin</button>
      </div>

      <!-- Bill Tab -->
      <div id="billTab" class="tab-pane active">
        <div class="grid grid-2">
          <!-- Bill Breakdown -->
          <div class="card">
            <div class="card-header">Monthly Postpaid Bill Statement</div>
            <div class="card-body">
              <div style="font-size:0.9rem; line-height:1.7;">
                <div style="display:flex; justify-content:space-between;"><span>Subscriber Number:</span><strong>+91 98401 23456</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Billing Cycle:</span><span>01-Nov-2026 to 30-Nov-2026</span></div>
                <div style="display:flex; justify-content:space-between;"><span>Payment Due Date:</span><strong id="dispDueDate">20-Nov-2026</strong></div>
                <div style="border-top:1px solid var(--border); margin:0.75rem 0; padding-top:0.75rem;">
                  <div style="display:flex; justify-content:space-between;"><span>Plan Rental (Unlimited 5G):</span><span>Rs. 699.00</span></div>
                  <div style="display:flex; justify-content:space-between;"><span>National Roaming:</span><span>Rs. 0.00</span></div>
                  <div style="display:flex; justify-content:space-between;"><span>GST (18%):</span><span>Rs. 125.82</span></div>
                  <div style="display:flex; justify-content:space-between; color:var(--danger); font-weight:bold;" id="lateFineRow">
                    <span>Late Payment Fine (Rs. 10/day):</span>
                    <span id="fineAmtText">Rs. 20.00</span>
                  </div>
                </div>
                <div style="border-top:2px solid var(--border); padding-top:0.75rem; display:flex; justify-content:space-between; font-size:1.3rem;">
                  <span>Total Outstanding:</span>
                  <strong style="color:var(--primary);" id="totalBillAmt">Rs. 844.82</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Form -->
          <div class="card">
            <div class="card-header">Select Payment Amount & Method</div>
            <div class="card-body">
              <form onsubmit="handlePayPhoneBill(event)">
                <div class="form-group">
                  <label class="form-label">Payment Option</label>
                  <div style="display:flex; gap:1.5rem; margin-top:0.35rem;">
                    <label><input type="radio" name="payOption" value="full" checked onchange="toggleCustomAmt()"> Pay Entire Bill (Rs. 844.82)</label>
                    <label><input type="radio" name="payOption" value="custom" onchange="toggleCustomAmt()"> Custom Partial Amount</label>
                  </div>
                </div>
                <div class="form-group" id="customAmtGroup" style="display:none;">
                  <label class="form-label">Custom Amount (Rs.)</label>
                  <input type="number" id="customAmtInput" class="form-control" value="500">
                </div>
                <div class="form-group">
                  <label class="form-label">Payment Channel</label>
                  <select class="form-select">
                    <option>UPI (Google Pay, PhonePe, Paytm)</option>
                    <option>Credit / Debit Card</option>
                    <option>Net Banking</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Confirm Payment & Email Receipt</button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tab -->
      <div id="adminTab" class="tab-pane">
        <div class="card">
          <div class="card-header">Admin Billing Cycle Configuration</div>
          <div class="card-body">
            <p style="font-size:0.9rem; color:var(--text-muted);">Configure postpaid cycle windows, statutory telecom taxes, and automatic Rs. 10/day overdue penalty triggers.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="lab-footer">
    <div class="lab-container">
      <p>Internet Programming Lab &bull; Exp-46: Online Phone Bill Payment System</p>
    </div>
  </footer>

  <script src="../assets/common.js"></script>
  <script>
    function toggleCustomAmt() {
      const isCustom = document.querySelector('input[name="payOption"]:checked').value === 'custom';
      document.getElementById('customAmtGroup').style.display = isCustom ? 'block' : 'none';
    }

    function handlePayPhoneBill(e) {
      e.preventDefault();
      const isCustom = document.querySelector('input[name="payOption"]:checked').value === 'custom';
      const paid = isCustom ? document.getElementById('customAmtInput').value : "844.82";
      const txId = 'TXN-' + Math.floor(100000 + Math.random() * 900000);
      showToast(`Phone bill payment of Rs. ${paid} successful! Transaction ID: ${txId}`, 'success');
    }
  </script>
</body>
</html>
"""
    with open(os.path.join(exp_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated Exp-46")

def run_all(base_dir="LAB"):
    generate_exp_41(base_dir)
    generate_exp_42(base_dir)
    generate_exp_43(base_dir)
    generate_exp_44(base_dir)
    generate_exp_45(base_dir)
    generate_exp_46(base_dir)
    print("Batch 5 completed (Exp 41 to 46).")

if __name__ == "__main__":
    run_all()
