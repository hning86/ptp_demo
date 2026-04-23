// UI Utilities and Dynamic Renderers

let docsMapping = {};
fetch("/safety-docs")
    .then(res => res.json())
    .then(data => {
        if (Array.isArray(data)) {
            data.forEach(doc => {
                const match = doc.title.match(/CON-EHS-TSS-\d{3}(?:\.\d{2})?/);
                if (match) {
                    docsMapping[match[0]] = doc.url;
                    if (match[0].endsWith(".00")) {
                        docsMapping[match[0].slice(0, -3)] = doc.url;
                    }
                } else if (doc.title.includes("Energy Wheel")) {
                    docsMapping["Energy Wheel"] = doc.url;
                    docsMapping["Energy Wheel.pdf"] = doc.url;
                }
            });
        }
    })
    .catch(err => console.error("Failed to load safety docs mapping:", err));

export function embedSafetyDocs(html) {
    const docRegex = /(CON-EHS-TSS-\d{3}(?:\.\d{2})?|Energy Wheel(?:\.pdf)?)/g;
    return html.replace(docRegex, (match) => {
        const url = docsMapping[match] || docsMapping[match + ".00"];
        if (url) {
            return `<a href="${url}" target="_blank" class="safety-doc-link" style="color: var(--primary-blue); text-decoration: underline;">${match}</a>`;
        }
        return match;
    });
}

export function addLog(msg) {
    const logList = document.getElementById("log-list");
    if (!logList) return;
    const li = document.createElement("li");
    li.textContent = msg;
    logList.appendChild(li);
    logList.scrollTop = logList.scrollHeight;
}

export function renderChecklist(options, onSelect) {
    const interactiveForms = document.getElementById("interactive-forms");
    if (!interactiveForms) return;
    interactiveForms.innerHTML = "";
    interactiveForms.classList.remove("collapsed");
    
    const closeBtn = document.createElement("button");
    closeBtn.className = "close-flyout-btn";
    closeBtn.onclick = () => {
        interactiveForms.classList.toggle("collapsed");
    };
    interactiveForms.appendChild(closeBtn);

    options.forEach(opt => {
        const pill = document.createElement("button");
        pill.className = "checklist-pill";
        pill.textContent = opt;
        pill.onclick = () => {
            pill.classList.toggle("selected");
            onSelect(opt, pill.classList.contains("selected"));
        };
        interactiveForms.appendChild(pill);
    });
}

export function renderCheckboxes(questions) {
    const interactiveForms = document.getElementById("interactive-forms");
    if (!interactiveForms) return;
    interactiveForms.innerHTML = "";
    interactiveForms.classList.remove("collapsed");
    
    const closeBtn = document.createElement("button");
    closeBtn.className = "close-flyout-btn";
    closeBtn.onclick = () => {
        interactiveForms.classList.toggle("collapsed");
    };
    interactiveForms.appendChild(closeBtn);

    const form = document.createElement("div");
    form.className = "checkbox-form";

    questions.forEach((q, index) => {
        const div = document.createElement("div");
        div.className = "checkbox-item";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = `q-${index}`;
        checkbox.value = q;

        const label = document.createElement("label");
        label.htmlFor = `q-${index}`;
        label.textContent = q;

        div.appendChild(checkbox);
        div.appendChild(label);
        form.appendChild(div);
    });

    const submitBtn = document.createElement("button");
    submitBtn.textContent = "Submit Selected";
    submitBtn.className = "submit-btn";

    submitBtn.onclick = () => {
        const selected = [];
        form.querySelectorAll("input[type='checkbox']:checked").forEach(cb => {
            selected.push(cb.value);
        });
        if (selected.length > 0) {
            const userInput = document.getElementById("user-input");
            userInput.value = "Ask me about: " + selected.join(", ") + ". And I am good with everything else.";
            document.getElementById("message-form").requestSubmit();
            interactiveForms.innerHTML = ""; // Clear after submit
        }
    };
    form.appendChild(submitBtn);

    interactiveForms.appendChild(form);
}

export function embedYouTube(html) {
    const youtubeRegex = /<a href="https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)".*?>.*?<\/a>/g;
    return html.replace(youtubeRegex, (match, videoId) => {
        return `<div class="video-container"><iframe src="https://www.youtube.com/embed/${videoId}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
    });
}

export function handleScriptTriggers(agentText) {
    const lines = agentText.split("\n");
    const questions = [];
    let consecutiveCount = 0;
    let currentSequence = [];

    lines.forEach(line => {
        const match = line.match(/^\s*-\s*\[\s*\]\s*(.*)/);
        if (match) {
            consecutiveCount++;
            currentSequence.push(match[1].trim());
        } else {
            if (consecutiveCount >= 2) {
                questions.push(...currentSequence);
            }
            consecutiveCount = 0;
            currentSequence = [];
        }
    });
    
    if (consecutiveCount >= 2) {
        questions.push(...currentSequence);
    }

    if (questions.length > 0) {
        renderCheckboxes(questions);
        addLog(`Rendered ${questions.length} interactive checkboxes.`);
    }
}

const USE_TIMELINE = true; // Set to false to revert to old card UI

let scheduleCache = null;
let docsCache = null;

export async function renderSchedule() {
    const scheduleContent = document.getElementById("schedule-content");
    if (!scheduleContent) return;
    
    if (scheduleCache) {
        renderScheduleHTML(scheduleCache);
        return;
    }
    
    scheduleContent.innerHTML = "<p>Loading schedule...</p>";
    try {
        const response = await fetch("/schedule");
        const data = await response.json();
        if (data.error) {
            scheduleContent.innerHTML = `<p>Error loading schedule: ${data.error}</p>`;
            return;
        }
        scheduleCache = data;
        renderScheduleHTML(scheduleCache);
    } catch (err) {
        scheduleContent.innerHTML = `<p>Error loading schedule: ${err.message}</p>`;
    }
}

function renderScheduleHTML(data) {
    const scheduleContent = document.getElementById("schedule-content");
    if (!scheduleContent) return;
    scheduleContent.innerHTML = "";
    
    if (USE_TIMELINE) {
        const container = document.createElement("div");
        container.className = "timeline-container";
        
        data.forEach(item => {
            const timelineItem = document.createElement("div");
            timelineItem.className = "timeline-item";
            timelineItem.innerHTML = `
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <h4>${item.description}</h4>
                    <p><span class="label">Task ID:</span> ${item.task_id}</p>
                    <p><span class="label">Dates:</span> ${item.start_date} to ${item.end_date}</p>
                    <p><span class="label">Location:</span> ${item.location}</p>
                    <p><span class="label">Foreperson:</span> ${item.crew_foreperson}</p>
                </div>
            `;
            container.appendChild(timelineItem);
        });
        scheduleContent.appendChild(container);
    } else {
        data.forEach(item => {
            const card = document.createElement("div");
            card.className = "schedule-card";
            card.innerHTML = `
                <h4>${item.description}</h4>
                <p><span class="label">Task ID:</span> ${item.task_id}</p>
                <p><span class="label">Dates:</span> ${item.start_date} to ${item.end_date}</p>
                <p><span class="label">Location:</span> ${item.location}</p>
                <p><span class="label">Foreperson:</span> ${item.crew_foreperson}</p>
            `;
            scheduleContent.appendChild(card);
        });
    }
}

export async function renderDocs() {
    const docsContent = document.getElementById("docs-content");
    if (!docsContent) return;
    
    if (docsCache) {
        renderDocsHTML(docsCache);
        return;
    }
    
    docsContent.innerHTML = "<p>Loading documents...</p>";
    try {
        const response = await fetch("/safety-docs");
        const data = await response.json();
        if (data.error) {
            docsContent.innerHTML = `<p>Error loading documents: ${data.error}</p>`;
            return;
        }
        docsCache = data;
        renderDocsHTML(docsCache);
    } catch (err) {
        docsContent.innerHTML = `<p>Error loading documents: ${err.message}</p>`;
    }
}

function renderDocsHTML(data) {
    const docsContent = document.getElementById("docs-content");
    if (!docsContent) return;
    docsContent.innerHTML = "";
    data.forEach(item => {
        const card = document.createElement("div");
        card.className = "schedule-card";
        card.innerHTML = `
            <h4><a href="${item.url}" target="_blank" style="color: var(--primary-blue); text-decoration: none;">${item.title}</a></h4>
            <p><span class="label">Category:</span> ${item.category}</p>
        `;
        docsContent.appendChild(card);
    });
}
