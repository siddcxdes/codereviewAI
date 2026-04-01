document.addEventListener('DOMContentLoaded', () => {
    const statusText = document.getElementById('backend-status');
    const statusDot = document.querySelector('.status-dot');

    async function checkBackendStatus() {
        try {
            const response = await fetch('http://127.0.0.1:8000/');
            
            if (response.ok) {
                const data = await response.json();
                statusText.textContent = 'Operational';
                statusDot.classList.remove('offline');
                statusDot.classList.add('online');
            } else {
                throw new Error('Backend returned non-200');
            }
        } catch (error) {
            console.error('Connection error:', error);
            statusText.textContent = 'Degraded Performance';
            statusDot.classList.remove('online');
            statusDot.classList.add('offline');
        }
    }

    checkBackendStatus();
    setInterval(checkBackendStatus, 10000);

    // Form Handling
    const form = document.getElementById('analyze-form');
    const repoInput = document.getElementById('repo-input');
    const prInput = document.getElementById('pr-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingState = document.getElementById('loading-state');
    const resultsContainer = document.getElementById('results-container');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const repoName = repoInput.value.trim();
        const prNumber = parseInt(prInput.value.trim(), 10);

        if (!repoName || isNaN(prNumber)) return;

        // Reset UI
        resultsContainer.classList.add('hidden');
        resultsContainer.innerHTML = '';
        loadingState.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('http://127.0.0.1:8000/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    repo_name: repoName,
                    pr_number: prNumber
                })
            });

            const data = await response.json();

            loadingState.classList.add('hidden');
            analyzeBtn.disabled = false;

            if (data.status === 'success') {
                const report = data.data;
                const score = report.score.total_score;
                const grade = report.score.grade;
                const rawComment = report.comment;

                resultsContainer.innerHTML = `
                    <div class="results-header">
                        <div class="score-badge">Quality Score: ${score}/100</div>
                        <div class="grade-badge">Grade ${grade}</div>
                    </div>
                    <div class="results-body">${escapeHTML(rawComment)}</div>
                `;
                resultsContainer.classList.remove('hidden');
            } else {
                alert(`Analysis Failed: ${data.message || 'Unknown error'}`);
            }

        } catch (error) {
            console.error(error);
            loadingState.classList.add('hidden');
            analyzeBtn.disabled = false;
            alert('Failed to connect to the analysis engine. Ensure backend is running.');
        }
    });

    // Basic HTML escaper for security
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
});