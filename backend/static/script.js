/**
 * SPACE DEBRIS MANAGEMENT - CORE SYSTEM SCRIPT (FLASK CONNECTED)
 */

document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initLiveStats();
    populateCatalog();
    updateSystemTime();
    initRAGQuery();   // ⭐ NEW
});


// --- 1. NAVIGATION SYSTEM ---
function initNavigation() {
    const navLinks = document.querySelectorAll(".navbar a");
    const pages = document.querySelectorAll(".page");

    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            const targetId = link.getAttribute("data-page");

            navLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            pages.forEach(page => {
                page.classList.remove("active");
                if (page.id === targetId) {
                    page.classList.add("active");
                }
            });
        });
    });
}


// --- 2. LIVE DATA SIMULATION ---
function initLiveStats() {
    const trackedCount = document.querySelector(".stats .card:nth-child(1) h2");
    const coverageCount = document.querySelector(".stats .card:nth-child(4) h2");

    setInterval(() => {
        if (trackedCount) {
            let current = parseInt(trackedCount.innerText.replace(',', ''));
            let change = Math.floor(Math.random() * 3) - 1;
            trackedCount.innerText = (current + change).toLocaleString();
        }

        if (coverageCount) {
            let currentCov = parseFloat(coverageCount.innerText);
            let drift = (Math.random() * 0.04 - 0.02).toFixed(2);
            coverageCount.innerText = (currentCov + parseFloat(drift)).toFixed(1) + "%";
        }
    }, 5000);
}


// --- 3. DYNAMIC CATALOG (still demo data) ---
function populateCatalog() {
    const debrisData = [
        { id: "DBR-2034-451", name: "Cosmos 2251 Frag", type: "Fragment", orbit: "LEO", alt: "780 km", risk: "High" },
        { id: "SAT-1998-067", name: "ISS Module Debris", type: "Satellite", orbit: "LEO", alt: "420 km", risk: "Medium" },
        { id: "RKT-2001-889", name: "Ariane 5 Upper", type: "Rocket", orbit: "GEO", alt: "35k km", risk: "Low" }
    ];

    const tbody = document.querySelector("#catalog table tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    debrisData.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td class="blue">${item.type}</td>
            <td>${item.orbit}</td>
            <td>${item.alt}</td>
            <td>--</td>
            <td>${item.risk}</td>
            <td>Just now</td>
        `;
        tbody.appendChild(row);
    });
}


// --- 4. SYSTEM CLOCK ---
function updateSystemTime() {
    const statusDiv = document.querySelector(".status");

    const update = () => {
        const now = new Date();
        const timeStr = now.toUTCString().split(" ")[4].slice(0,5);
        if (statusDiv) {
            statusDiv.innerHTML = `<span class="dot"></span> SYSTEM ACTIVE // ${timeStr} UTC`;
        }
    };

    update();
    setInterval(update, 10000);
}


// ⭐⭐⭐ 5. CONNECT TO FLASK RAG (MOST IMPORTANT) ⭐⭐⭐
function initRAGQuery() {
    const askBtn = document.getElementById("askBtn");
    const questionInput = document.getElementById("question");
    const answerDiv = document.getElementById("answer");

    if (!askBtn) return;

    askBtn.addEventListener("click", async () => {
        const question = questionInput.value.trim();
        if (!question) return;

        answerDiv.innerHTML = "Thinking...";

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            answerDiv.innerHTML = data.answer.replace(/\n/g, "<br>");
        } catch (err) {
            answerDiv.innerHTML = "Error connecting to AI system.";
        }
    });
}
