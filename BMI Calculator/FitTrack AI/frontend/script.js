// Minimal frontend behavior: particles, flip card, call /api/bmi
const canvas = document.getElementById('bg');
const ctx = canvas.getContext('2d');
let W = canvas.width = innerWidth;
let H = canvas.height = innerHeight;
window.addEventListener('resize', () => { W = canvas.width = innerWidth; H = canvas.height = innerHeight })

// simple particles
const particles = [];
for (let i = 0; i < 80; i++) particles.push({ x: Math.random() * W, y: Math.random() * H, r: 2 + Math.random() * 4, dx: (Math.random() - 0.5) * 2, dy: (0.5 + Math.random() * 1.5), color: `hsl(${Math.random() * 360}, 70%, 60%)` })

let mouse = { x: W / 2, y: H / 2 };
window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });

function stepParticles() {
    ctx.clearRect(0, 0, W, H);
    for (const p of particles) {
        // slight attraction to mouse
        const dist = Math.sqrt((p.x - mouse.x) ** 2 + (p.y - mouse.y) ** 2);
        if (dist < 150) {
            p.dx += (mouse.x - p.x) / dist * 0.02;
            p.dy += (mouse.y - p.y) / dist * 0.02;
        }
        p.x += p.dx; p.y += p.dy;
        p.dx *= 0.999; p.dy *= 0.999; // minimal friction
        if (p.x < -20) p.x = W + 20; if (p.x > W + 20) p.x = -20; if (p.y > H + 20) p.y = -20;
        ctx.beginPath(); ctx.fillStyle = p.color; ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    }
    requestAnimationFrame(stepParticles);
}
stepParticles();

// UI bindings
const card = document.getElementById('card');
const calc = document.getElementById('calc');
const reset = document.getElementById('reset');
const backBtn = document.getElementById('backBtn');
const themeToggle = document.getElementById('themeToggle');
const weightInput = document.getElementById('weight');
const heightMInput = document.getElementById('height_m');
const heightFtInput = document.getElementById('height_ft');
const heightInInput = document.getElementById('height_in');
const heightUnitRadios = document.getElementsByName('heightUnit');
const bmiVal = document.getElementById('bmiVal');
const bmiCat = document.getElementById('bmiCat');
const msg = document.getElementById('msg');

function showResult(data) {
    bmiVal.textContent = data.bmi;
    bmiCat.textContent = data.category;
    bmiCat.style.color = data.color;
    msg.textContent = data.message;
    // Set BMI bar
    const percentage = Math.min(100, Math.max(0, (data.bmi - 15) / (40 - 15) * 100));
    document.getElementById('bmiBar').style.width = percentage + '%';
    card.classList.add('flipped');
    // highlight the matching row in the BMI legend (if present)
    highlightBMIRows(data.bmi);
}

function highlightBMIRows(bmi) {
    try {
        const rows = document.querySelectorAll('#bmiLegend .bmi-row');
        rows.forEach(r => r.classList.remove('highlight'));
        for (const r of rows) {
            const min = parseFloat(r.dataset.min);
            const max = parseFloat(r.dataset.max);
            if (!isNaN(min) && !isNaN(max) && bmi >= min && bmi <= max) {
                r.classList.add('highlight');
                // ensure it's visible on small screens
                r.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                break;
            }
        }
    } catch (err) {
        // ignore if legend not present
    }
}

// Inline validation: show messages and enable/disable Calculate
const formErrorsDiv = document.getElementById('formErrors');
function validateInputs() {
    const weight = parseFloat(weightInput.value);
    let chosen = 'm';
    for (const r of heightUnitRadios) if (r.checked) { chosen = r.value; break }
    let valid = true;
    let msgs = [];
    if (!weight || weight <= 0) { valid = false; msgs.push('Enter weight (kg) > 0'); }
    if (chosen === 'm') {
        const h = parseFloat(heightMInput.value);
        if (!h || h <= 0) { valid = false; msgs.push('Enter height in meters > 0'); }
    } else {
        const ft = parseFloat(heightFtInput.value) || 0;
        const inch = parseInt(heightInInput?.value) || 0;
        if (ft <= 0 && inch <= 0) { valid = false; msgs.push('Enter height in feet and/or inches'); }
        if (inch < 0 || inch > 11) { valid = false; msgs.push('Inches must be between 0 and 11'); }
    }
    formErrorsDiv.innerHTML = msgs.map(m => `<div class="error-text">${m}</div>`).join('');
    calc.disabled = !valid;
    return valid;
}

// bind inputs to validation
weightInput.addEventListener('input', validateInputs);
if (heightMInput) heightMInput.addEventListener('input', validateInputs);
if (heightFtInput) heightFtInput.addEventListener('input', validateInputs);
if (heightInInput) heightInInput.addEventListener('input', validateInputs);
for (const r of heightUnitRadios) r.addEventListener('change', () => { updateHeightVisibility(); validateInputs(); });
// initial validation state
validateInputs();

async function calculate() {
    const weight = parseFloat(weightInput.value);
    // determine chosen height unit
    let chosen = 'm';
    for (const r of heightUnitRadios) if (r.checked) { chosen = r.value; break }

    if (!weight) { alert('Enter weight (kg)'); return }

    let payload = { weight_kg: weight };
    if (chosen === 'm') {
        const h = parseFloat(heightMInput.value);
        if (!h) { alert('Enter height in meters'); return }
        payload.height_m = h;
    } else {
        const ft = parseFloat(heightFtInput.value) || 0;
        const inch = parseInt(heightInInput?.value) || 0;
        if (ft <= 0 && inch <= 0) { alert('Enter height in feet and/or inches'); return }
        if (inch < 0 || inch > 11) { alert('Inches must be between 0 and 11'); return }
        // convert feet+inches -> meters on client to avoid ambiguity and ensure exact conversion
        const total_inches = (ft * 12) + inch;
        const height_m = total_inches * 0.0254; // 1 inch = 0.0254 m
        payload.height_m = parseFloat(height_m.toFixed(4));
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    calc.disabled = true;
    reset.disabled = true;

    try {
        const res = await fetch('/api/bmi', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!res.ok) { const txt = await res.text(); alert('Error: ' + txt); return }
        const data = await res.json();
        showResult(data);
    } catch (err) { alert('Network error: ' + err.message) } finally {
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        calc.disabled = false;
        reset.disabled = false;
    }
}

calc.addEventListener('click', calculate);
reset.addEventListener('click', () => {
    weightInput.value = '';
    if (heightMInput) heightMInput.value = '';
    if (heightFtInput) heightFtInput.value = '';
    if (heightInInput) heightInInput.value = '';
    // reset radio to meters
    for (const r of heightUnitRadios) r.checked = (r.value === 'm');
    // adjust visibility
    updateHeightVisibility();
    bmiVal.textContent = '';
    bmiCat.textContent = '';
    msg.textContent = '';
    card.classList.remove('flipped')
});
backBtn.addEventListener('click', () => { card.classList.remove('flipped') });

// Theme toggle
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-theme');
    const icon = themeToggle.querySelector('i');
    if (document.body.classList.contains('light-theme')) {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
});

// Nav bar functionality
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute('data-section');
        showSection(sectionId);
    });
});

function showSection(sectionId) {
    sections.forEach(section => {
        section.classList.remove('active');
    });
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');
}

// Show/hide meter vs ft/in inputs
function updateHeightVisibility() {
    const chosen = Array.from(heightUnitRadios).find(r => r.checked)?.value || 'm';
    const unitM = document.querySelector('.unit-m');
    const unitFt = document.querySelector('.unit-ft');
    if (unitM) unitM.style.display = (chosen === 'm') ? 'block' : 'none';
    if (unitFt) unitFt.style.display = (chosen === 'ft') ? 'flex' : 'none';
}
// bind radio change
for (const r of heightUnitRadios) r.addEventListener('change', updateHeightVisibility);
// initial visibility
updateHeightVisibility();
