document.addEventListener('DOMContentLoaded', () => {
    // Core API config
    const API_URL = '/api';
    
    // DOM Elements
    const elements = {
        themeToggle: document.getElementById('themeToggle'),
        themeIcon: document.getElementById('themeIcon'),
        htmlElement: document.documentElement,
        
        textInput: document.getElementById('textInput'),
        wordCount: document.getElementById('wordCount'),
        charCount: document.getElementById('charCount'),
        analyzeBtn: document.getElementById('analyzeBtn'),
        clearBtn: document.getElementById('clearBtn'),
        pasteBtn: document.getElementById('pasteBtn'),
        exampleBtn: document.getElementById('exampleBtn'),
        realtimeToggle: document.getElementById('realtimeToggle'),
        
        emptyState: document.getElementById('emptyState'),
        loadingState: document.getElementById('loadingState'),
        errorState: document.getElementById('errorState'),
        errorMsg: document.getElementById('errorMsg'),
        resultContent: document.getElementById('resultContent'),
        
        sentimentEmoji: document.getElementById('sentimentEmoji'),
        sentimentLabel: document.getElementById('sentimentLabel'),
        sentimentScore: document.getElementById('sentimentScore'),
        sentimentCard: document.querySelector('.sentiment-card'),
        
        posFill: document.getElementById('posFill'),
        neuFill: document.getElementById('neuFill'),
        negFill: document.getElementById('negFill'),
        posPercent: document.getElementById('posPercent'),
        neuPercent: document.getElementById('neuPercent'),
        negPercent: document.getElementById('negPercent'),
        
        highlightedText: document.getElementById('highlightedText'),
        copyBtn: document.getElementById('copyBtn'),
        
        historyBody: document.getElementById('historyBody'),
        emptyHistory: document.getElementById('emptyHistory'),
        exportBtn: document.getElementById('exportBtn')
    };

    // State
    let debounceTimer;
    let analysisHistory = JSON.parse(localStorage.getItem('sentimentHistory')) || [];

    // --- Initialization ---
    initTheme();
    renderHistory();

    // --- Event Listeners ---
    elements.themeToggle.addEventListener('click', toggleTheme);
    
    elements.textInput.addEventListener('input', () => {
        updateCounters();
        if (elements.realtimeToggle.checked) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if(elements.textInput.value.trim().length > 0) {
                    analyzeText();
                } else {
                    resetWorkspace();
                }
            }, 800); // 800ms debounce
        }
    });

    elements.analyzeBtn.addEventListener('click', () => {
        if(elements.textInput.value.trim().length > 0) {
            analyzeText();
        }
    });

    elements.clearBtn.addEventListener('click', () => {
        elements.textInput.value = '';
        updateCounters();
        resetWorkspace();
    });

    elements.pasteBtn.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            elements.textInput.value = text;
            updateCounters();
            if(elements.realtimeToggle.checked) analyzeText();
        } catch (err) {
            console.error('Failed to read clipboard contents: ', err);
        }
    });

    elements.exampleBtn.addEventListener('click', () => {
        const examples = [
            "The new product update is absolutely fantastic, the team did a great job!",
            "I'm extremely disappointed with the customer service I received today.",
            "The meeting is scheduled for 3 PM tomorrow in the conference room.",
            "This software is somewhat okay, but it lacks several key features."
        ];
        elements.textInput.value = examples[Math.floor(Math.random() * examples.length)];
        updateCounters();
        if(elements.realtimeToggle.checked) analyzeText();
    });

    elements.copyBtn.addEventListener('click', () => {
        const label = elements.sentimentLabel.textContent;
        const text = elements.textInput.value.trim();
        const score = elements.sentimentScore.textContent;
        const copyText = `Text: "${text}"\nSentiment: ${label}\n${score}`;
        
        navigator.clipboard.writeText(copyText).then(() => {
            const icon = elements.copyBtn.querySelector('i');
            icon.className = 'ph ph-check';
            setTimeout(() => { icon.className = 'ph ph-copy'; }, 2000);
        });
    });

    elements.exportBtn.addEventListener('click', exportToCSV);

    // --- Theme Logic ---
    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        elements.htmlElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    function toggleTheme() {
        const currentTheme = elements.htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        elements.htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    }

    function updateThemeIcon(theme) {
        elements.themeIcon.className = theme === 'dark' ? 'ph ph-sun' : 'ph ph-moon';
    }

    // --- Core Logic ---
    function updateCounters() {
        const text = elements.textInput.value;
        elements.charCount.textContent = `${text.length} characters`;
        
        const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        elements.wordCount.textContent = `${words} words`;
    }

    function resetWorkspace() {
        elements.emptyState.classList.remove('hidden');
        elements.loadingState.classList.add('hidden');
        elements.errorState.classList.add('hidden');
        elements.resultContent.classList.add('hidden');
    }

    async function analyzeText() {
        const text = elements.textInput.value.trim();
        if(!text) return;

        // UI State: Loading
        elements.emptyState.classList.add('hidden');
        elements.errorState.classList.add('hidden');
        elements.resultContent.classList.add('hidden');
        elements.loadingState.classList.remove('hidden');

        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            if (!response.ok) throw new Error('API Request Failed');
            const data = await response.json();
            
            if(data.error) throw new Error(data.error);

            displayResult(data.result, text);
            addToHistory(text, data.result);
        } catch (err) {
            elements.loadingState.classList.add('hidden');
            elements.errorMsg.textContent = err.message;
            elements.errorState.classList.remove('hidden');
        }
    }

    function displayResult(result, originalText) {
        elements.loadingState.classList.add('hidden');
        elements.resultContent.classList.remove('hidden');

        const { sentiment, confidence, probabilities } = result;
        const confPercent = (confidence * 100).toFixed(1);

        // Update Card
        elements.sentimentLabel.textContent = sentiment;
        elements.sentimentScore.textContent = `Confidence: ${confPercent}%`;
        
        elements.sentimentCard.className = 'sentiment-card'; // reset
        if(sentiment === 'Positive') {
            elements.sentimentCard.classList.add('pos');
            elements.sentimentEmoji.textContent = '😊';
        } else if(sentiment === 'Negative') {
            elements.sentimentCard.classList.add('neg');
            elements.sentimentEmoji.textContent = '😡';
        } else {
            elements.sentimentCard.classList.add('neu');
            elements.sentimentEmoji.textContent = '😐';
        }

        // Update Meters
        const pPos = (probabilities.Positive * 100).toFixed(1);
        const pNeu = (probabilities.Neutral * 100).toFixed(1);
        const pNeg = (probabilities.Negative * 100).toFixed(1);

        elements.posPercent.textContent = `${pPos}%`;
        elements.neuPercent.textContent = `${pNeu}%`;
        elements.negPercent.textContent = `${pNeg}%`;

        // Small delay to trigger CSS transition
        setTimeout(() => {
            elements.posFill.style.width = `${pPos}%`;
            elements.neuFill.style.width = `${pNeu}%`;
            elements.negFill.style.width = `${pNeg}%`;
        }, 50);

        // Client-side Keyword Highlighter (Visual Polish)
        highlightKeywords(originalText);
    }

    function highlightKeywords(text) {
        // Very basic dictionary for visual effect
        const posWords = ['good', 'great', 'excellent', 'amazing', 'fantastic', 'love', 'happy', 'beautiful', 'best', 'awesome'];
        const negWords = ['bad', 'terrible', 'worst', 'hate', 'disappointed', 'awful', 'sad', 'angry', 'poor', 'stupid'];

        let highlighted = escapeHtml(text);
        
        const words = highlighted.split(/\b/);
        const processed = words.map(word => {
            const lower = word.toLowerCase();
            if (posWords.includes(lower)) return `<span class="word-pos">${word}</span>`;
            if (negWords.includes(lower)) return `<span class="word-neg">${word}</span>`;
            return word;
        });

        elements.highlightedText.innerHTML = processed.join('');
    }

    // --- History & Export Logic ---
    function addToHistory(text, result) {
        const newItem = {
            id: Date.now(),
            time: new Date().toLocaleTimeString(),
            text: text,
            sentiment: result.sentiment,
            confidence: (result.confidence * 100).toFixed(1)
        };

        analysisHistory.unshift(newItem);
        if(analysisHistory.length > 50) analysisHistory.pop(); // keep last 50
        
        localStorage.setItem('sentimentHistory', JSON.stringify(analysisHistory));
        renderHistory();
    }

    function renderHistory() {
        elements.historyBody.innerHTML = '';
        
        if (analysisHistory.length === 0) {
            elements.emptyHistory.style.display = 'block';
            return;
        }

        elements.emptyHistory.style.display = 'none';
        
        analysisHistory.slice(0, 10).forEach(item => { // Show top 10
            const tr = document.createElement('tr');
            
            let badgeClass = 'neu';
            if(item.sentiment === 'Positive') badgeClass = 'pos';
            if(item.sentiment === 'Negative') badgeClass = 'neg';

            const snippet = item.text.length > 40 ? item.text.substring(0, 40) + '...' : item.text;

            tr.innerHTML = `
                <td>${item.time}</td>
                <td title="${escapeHtml(item.text)}">${escapeHtml(snippet)}</td>
                <td><span class="table-sentiment ${badgeClass}">${item.sentiment}</span></td>
                <td>${item.confidence}%</td>
            `;
            elements.historyBody.appendChild(tr);
        });
    }

    function exportToCSV() {
        if(analysisHistory.length === 0) return;

        let csvContent = "data:text/csv;charset=utf-8,";
        csvContent += "Time,Text,Sentiment,Confidence(%)\n";

        analysisHistory.forEach(row => {
            // escape quotes in text
            const escapedText = row.text.replace(/"/g, '""');
            const csvRow = `"${row.time}","${escapedText}","${row.sentiment}",${row.confidence}`;
            csvContent += csvRow + "\n";
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "sentiment_history.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function escapeHtml(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
});
