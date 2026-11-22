// Common Helper Utilities for Internet Programming Lab Experiments
function showToast(message, type = 'info') {
  let container = document.getElementById('labToastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'labToastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add('show');
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove('show');
}

function initTabs() {
  document.querySelectorAll('.tabs-header').forEach(header => {
    const btns = header.querySelectorAll('.tab-btn');
    const container = header.parentElement;
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-tab');
        btns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        container.querySelectorAll('.tab-pane').forEach(pane => {
          if (pane.id === targetId) {
            pane.classList.add('active');
          } else {
            pane.classList.remove('active');
          }
        });
      });
    });
  });
}

function formatINR(val) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(val);
}

function formatUSD(val) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);
}

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  // Close modal when backdrop clicked
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) backdrop.classList.remove('show');
    });
  });
});
