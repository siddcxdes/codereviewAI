const API_BASE = "http://localhost:8000/api";

// Elements
const authSection = document.getElementById("auth-section");
const mainApp = document.getElementById("main-app");
const authControls = document.getElementById("auth-controls");
const userGreeting = document.getElementById("user-greeting");
const historySection = document.getElementById("history-section");
const historyContainer = document.getElementById("history-container");
const usernameDisplay = document.getElementById("username-display");

let currentAuthMode = 'login'; // 'login' or 'signup'

// Token Management
function getToken() {
    return localStorage.getItem('cr_token');
}

function setToken(token, username) {
    localStorage.setItem('cr_token', token);
    localStorage.setItem('cr_username', username);
    checkAuthStatus();
}

function logout() {
    localStorage.removeItem('cr_token');
    localStorage.removeItem('cr_username');
    checkAuthStatus();
}

function checkAuthStatus() {
    const token = getToken();
    const username = localStorage.getItem('cr_username');
    
    if (token && username) {
        // Logged in
        authControls.classList.add("hidden");
        userGreeting.classList.remove("hidden");
        usernameDisplay.textContent = username;
        historySection.classList.remove("hidden");
        loadHistory();
    } else {
        // Not logged in
        authControls.classList.remove("hidden");
        userGreeting.classList.add("hidden");
        historySection.classList.add("hidden");
    }
}

// Authentication Flow
function showAuth(mode) {
    currentAuthMode = mode;
    authSection.classList.remove("hidden");
    mainApp.classList.add("hidden");
    
    document.getElementById("auth-title").innerText = mode === 'login' ? "Sign in to your account" : "Create an account";
    document.getElementById("auth-toggle-link").innerText = mode === 'login' 
        ? "Don't have an account? Sign up" 
        : "Already have an account? Sign in";
}

function toggleAuthMode() {
    showAuth(currentAuthMode === 'login' ? 'signup' : 'login');
}

document.getElementById("auth-submit-btn").addEventListener("click", async () => {
    const username = document.getElementById("auth-username").value;
    const password = document.getElementById("auth-password").value;
    const errorEl = document.getElementById("auth-error");
    const submitBtn = document.getElementById("auth-submit-btn");
    
    if(!username || !password) {
        errorEl.innerText = "Please enter username and password.";
        errorEl.classList.remove("hidden");
        return;
    }
    
    submitBtn.disabled = true;
    submitBtn.innerText = "Authenticating...";
    
    try {
        const res = await fetch(`${API_BASE}/${currentAuthMode}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        
        if (data.status === 'success') {
            setToken(data.token, data.username);
            authSection.classList.add("hidden");
            mainApp.classList.remove("hidden");
            document.getElementById("auth-password").value = ''; // clear password
            errorEl.classList.add("hidden");
        } else {
            errorEl.innerText = data.message;
            errorEl.classList.remove("hidden");
        }
    } catch(e) {
        errorEl.innerText = "Server error. Try again.";
        errorEl.classList.remove("hidden");
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = "Continue";
    }
});

// Load History
async function loadHistory() {
    const token = getToken();
    if (!token) return;
    
    try {
        const res = await fetch(`${API_BASE}/history`, {
            headers: { 'Authorization': token }
        });
        const data = await res.json();
        
        if (data.status === 'success' && data.history.length > 0) {
            historyContainer.innerHTML = data.history.map(h => `
                <div class="history-item">
                    <div class="history-item-header">
                        <span class="history-repo">${h.repo_name} #${h.pr_number}</span>
                        <span class="grade-badge" style="background: var(--bg-body); border-color: var(--border-color); color: var(--text-secondary);">Grade ${h.grade}</span>
                    </div>
                    <div class="history-title">${h.pr_title}</div>
                    <div class="history-meta">Score: ${h.score}/10 &bull; Analyzed on ${new Date(h.created_at).toLocaleDateString()}</div>
                </div>
            `).join('');
        } else {
            historyContainer.innerHTML = "<div class='empty-state'>No historical analysis records found.</div>";
        }
    } catch(e) {
        historyContainer.innerHTML = "<div class='empty-state'>Failed to synchronize history.</div>";
    }
}

// PR Analysis Flow
document.getElementById("analyze-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const repo = document.getElementById("repo-input").value;
    const pr = parseInt(document.getElementById("pr-input").value);
    
    const analyzeBtn = document.getElementById("analyze-btn");
    const loadingSection = document.getElementById("loading-state");
    const resultsContainer = document.getElementById("results-container");
    
    // UI Loading state
    analyzeBtn.disabled = true;
    resultsContainer.classList.add("hidden");
    loadingSection.classList.remove("hidden");
    resultsContainer.innerHTML = "";
    
    try {
        const headers = { 'Content-Type': 'application/json' };
        const token = getToken();
        if(token) headers['Authorization'] = token;
        
        const res = await fetch(`${API_BASE}/analyze`, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ repo_name: repo, pr_number: pr })
        });
        
        const json = await res.json();
        
        if (json.status === "error") {
            resultsContainer.innerHTML = `<div class="error-message" style="margin:2rem">Error: ${json.message}</div>`;
        } else {
            const data = json.data;
            const score = data.score?.total_score || 0;
            const grade = data.score?.grade || "N/A";
            
            // Format results cleanly
            resultsContainer.innerHTML = `
                <div class="results-header">
                    <span class="score-badge">${score}/10 Score</span>
                    <span class="grade-badge">Grade ${grade}</span>
                </div>
                <div class="results-body">${data.comment || "Analysis complete."}</div>
            `;
            if (token) loadHistory(); // refresh history if logged in
        }
    } catch (err) {
        resultsContainer.innerHTML = `<div class="error-message" style="margin:2rem">Integration Error: Remote services unavailable.</div>`;
    } finally {
        analyzeBtn.disabled = false;
        loadingSection.classList.add("hidden");
        resultsContainer.classList.remove("hidden");
    }
});

// Run on load
checkAuthStatus();
