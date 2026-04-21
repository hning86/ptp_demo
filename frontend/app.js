const presetPrompts = [
    { id: "btn_cable_pull", label: "Pull Cable", text: "We are at the UNO3 campus, Area B of the data hall. We are about to pull low voltage cable in aisle 3. The cable trays are already installed. I have a crew of 3 people today and we have 10 hours to get the work done." },
    { id: "btn_yes", label: "Yes", text: "Yes please go ahead." },
    { id: "btn_new_members", label: "New Member", text: "We have a new member in the crew. This is his first day at the job site. He might need some extra help." },
    { id: "btn_congestion", label: "Congestion", text: "Work area has become congested and we can't drive the scissor lift in. Can you suggest some alternatives?" },
    { id: "btn_fatigue", label: "Fatigue", text: "We are doing OK. Just a little tired. nothing unusual. We will be fine." },
    { id: "btn_ready", label: "Ready", text: "We are ready to move on to the next step." }
];




let currentScene = 1;
let sceneStepIndex = 0;
let currentSessionSuffix = Date.now().toString();
const chatWindow = document.getElementById("chat-window");
const interactiveForms = document.getElementById("interactive-forms");
const logList = document.getElementById("log-list");

const allShortcutIds = ["btn_cable_pull", "btn_yes", "btn_new_members", "btn_congestion", "btn_fatigue", "btn_ready"];

// Setup quick preset buttons
function updatePresets() {
    allShortcutIds.forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.style.display = "none";
    });

    const presets = presetPrompts;
    presets.forEach(item => {
        const btn = document.getElementById(item.id);
        if (btn) {
            btn.textContent = item.label;
            btn.setAttribute("data-tooltip", item.text);
            btn.style.display = "inline-block";
            btn.onclick = () => {
                document.getElementById("user-input").value = item.text;
            };
        }
    });
    
    const resetBtn = document.getElementById("btn_reset");
    if (resetBtn) {
        resetBtn.onclick = async () => {
            try {
                currentSessionSuffix = Date.now().toString();
                await fetch("/reset", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ session_id: "demo-stage-" + currentScene + "-" + currentSessionSuffix })
                });
                addLog("Resetting fully to a clean unique memory pool...");
                setTimeout(() => window.location.reload(), 200);
            } catch (err) {
                window.location.reload();
            }
        };
    }
}

// Add simple log
function addLog(msg) {
    const li = document.createElement("li");
    li.textContent = msg;
    logList.appendChild(li);
    logList.scrollTop = logList.scrollHeight;
}

// Toggle Scenes
document.querySelectorAll(".scene-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
        document.querySelectorAll(".scene-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        
        const selectedScene = parseInt(btn.getAttribute("data-scene"));
        sceneStepIndex = 0;
        
        interactiveForms.innerHTML = "";
        
        if (selectedScene === 2) {
            // Stay on Scene 1 agent, but load Scene 2 presets (now overridden to scene 1)
            updatePresets();
            
            // Display stop graphic in message pane
            const activeLayer = document.getElementById("chat-scene-1");
            if (activeLayer) {
                const imgDiv = document.createElement("div");
                imgDiv.className = "message-bubble agent";
                imgDiv.innerHTML = '<img src="stop_work.png" alt="Stop Work Authority" style="max-width: 100%; border-radius: 8px; margin: 10px 0;">';
                activeLayer.appendChild(imgDiv);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
            
            addLog("Initiated midday periodic Stop Work authority check.");

            // Automatically send message to agent
            const userInput = document.getElementById("user-input");
            if (userInput) {
                userInput.value = "pause work and reassess the plan";
                document.getElementById("message-form").requestSubmit();
            }
        } else {
            currentScene = selectedScene;
            updatePresets();
            
            addLog(`Navigated to Scene ${currentScene}`);
        }
    });
});

// Dynamic Interactive Form Rendering
function renderChecklist(options, onSelect) {
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

function renderCheckboxes(questions) {
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

function embedYouTube(html) {
    const youtubeRegex = /<a href="https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)".*?>.*?<\/a>/g;
    return html.replace(youtubeRegex, (match, videoId) => {
        return `<div class="video-container"><iframe src="https://www.youtube.com/embed/${videoId}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
    });
}

// Process response side effects
function handleScriptTriggers(agentText) {


    // Parse markdown checkboxes (allowing leading whitespace)
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

// Send Message via Stream or Fallback
const form = document.getElementById("message-form");
const input = document.getElementById("user-input");

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit();
    }
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("user-input");
    const msg = input.value.trim();
    if (!msg) return;

    const activeLayer = document.getElementById("chat-scene-1");
    // Render user msg
    const userDiv = document.createElement("div");
    userDiv.className = "message-bubble user";
    userDiv.textContent = msg;
    if (activeLayer) activeLayer.appendChild(userDiv);
    input.value = "";
    chatWindow.scrollTop = chatWindow.scrollHeight;
    
    addLog("Sending request to backend proxy...");
    
    // Agent placeholder
    const agentDiv = document.createElement("div");
    agentDiv.className = "message-bubble agent thinking";
    agentDiv.innerHTML = '<span class="typing-indicator"><span></span><span></span><span></span></span>';
    if (activeLayer) activeLayer.appendChild(agentDiv);

    try {
        const res = await fetch(`/scene${currentScene}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: `demo-stage-${currentScene}-${currentSessionSuffix}`, message: msg })
        });
        
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedText = "";
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split("\n");
            for (let line of lines) {
                if (line.startsWith("data: ")) {
                    const jsonStr = line.slice(6).trim();
                    if (jsonStr === "[DONE]") continue;
                    try {
                        const parsed = JSON.parse(jsonStr);
                        if (parsed.text) {
                            accumulatedText += parsed.text;

                            // Filter out duplicate checklist items for display
                            const filteredText = accumulatedText.split("\n")
                                .filter(l => !l.match(/^\s*-\s*\[\s*\]/))
                                .join("\n");

                            const parsedHtml = marked.parse(filteredText);
                            agentDiv.innerHTML = embedYouTube(parsedHtml) + '<span class="typing-indicator"><span></span><span></span><span></span></span>';
                            chatWindow.scrollTop = chatWindow.scrollHeight;
                        }
                    } catch (err) {}
                }
            }
        }

        const filteredText = accumulatedText.split("\n")
            .filter(l => !l.match(/^\s*-\s*\[\s*\]/))
            .join("\n");

        const parsedHtml = marked.parse(filteredText);
        agentDiv.innerHTML = embedYouTube(parsedHtml);
        handleScriptTriggers(accumulatedText);
        
        if (accumulatedText.includes("PTP v2 Generated")) {
            const swatBtn = document.getElementById("scene-2-btn");
            if (swatBtn) {
                swatBtn.disabled = false;
                addLog("SWAT-2 button enabled.");
            }
        }
        
        addLog("Received full streaming context.");
        
    } catch (error) {
        addLog(`Error: ${error.message}`);
        agentDiv.classList.remove("thinking");
        agentDiv.innerHTML = marked.parse(`**Error:** ${error.message || error}`);
    }
});

updatePresets();

// Trigger automated initial handshake
async function triggerHiddenGreeting() {
    const activeLayer = document.getElementById("chat-scene-1");
    const agentDiv = document.createElement("div");
    agentDiv.className = "message-bubble agent thinking";
    agentDiv.innerHTML = '<span class="typing-indicator"><span></span><span></span><span></span></span>';
    if (activeLayer) activeLayer.appendChild(agentDiv);

    try {
        const res = await fetch("/scene1/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: "demo-stage-1-" + currentSessionSuffix, message: "Briefly greet the user to start the Morning task brief!" })
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedText = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split("\n");
            for (let line of lines) {
                if (line.startsWith("data: ")) {
                    const jsonStr = line.slice(6).trim();
                    if (jsonStr === "[DONE]") continue;
                    try {
                        const parsed = JSON.parse(jsonStr);
                        if (parsed.text) {
                            accumulatedText += parsed.text;
                            agentDiv.innerHTML = marked.parse(accumulatedText) + '<span class="typing-indicator"><span></span><span></span><span></span></span>';
                        }
                    } catch (err) { }
                }
            }
        }
        agentDiv.innerHTML = marked.parse(accumulatedText);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    } catch (err) {
        agentDiv.innerHTML = marked.parse("Good morning! Welcome to UNO3 construction management system. Ready for shift briefs?");
    }
}

window.addEventListener("DOMContentLoaded", triggerHiddenGreeting);

// Schedule Pane Logic
const showScheduleBtn = document.getElementById("show-schedule-btn");
const closeScheduleBtn = document.getElementById("close-schedule-btn");
const schedulePane = document.getElementById("schedule-pane");
const scheduleContent = document.getElementById("schedule-content");

if (showScheduleBtn && schedulePane && closeScheduleBtn) {
    showScheduleBtn.addEventListener("click", () => {
        renderSchedule();
        schedulePane.classList.add("open");
    });

    closeScheduleBtn.addEventListener("click", () => {
        schedulePane.classList.remove("open");
    });
}

async function renderSchedule() {
    if (!scheduleContent) return;
    scheduleContent.innerHTML = "<p>Loading schedule...</p>";
    try {
        const response = await fetch("/schedule");
        const data = await response.json();
        if (data.error) {
            scheduleContent.innerHTML = `<p>Error loading schedule: ${data.error}</p>`;
            return;
        }
        scheduleContent.innerHTML = "";
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
    } catch (err) {
        scheduleContent.innerHTML = `<p>Error loading schedule: ${err.message}</p>`;
    }
}

// Docs Pane Logic
const showDocsBtn = document.getElementById("show-docs-btn");
const closeDocsBtn = document.getElementById("close-docs-btn");
const docsPane = document.getElementById("docs-pane");
const docsContent = document.getElementById("docs-content");

if (showDocsBtn && docsPane && closeDocsBtn) {
    showDocsBtn.addEventListener("click", () => {
        renderDocs();
        docsPane.classList.add("open");
    });

    closeDocsBtn.addEventListener("click", () => {
        docsPane.classList.remove("open");
    });
}

async function renderDocs() {
    if (!docsContent) return;
    docsContent.innerHTML = "<p>Loading documents...</p>";
    try {
        const response = await fetch("/safety-docs");
        const data = await response.json();
        if (data.error) {
            docsContent.innerHTML = `<p>Error loading documents: ${data.error}</p>`;
            return;
        }
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
    } catch (err) {
        docsContent.innerHTML = `<p>Error loading documents: ${err.message}</p>`;
    }
}
