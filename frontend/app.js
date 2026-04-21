import { presetPrompts, allShortcutIds } from './presets.js';
import { addLog, embedYouTube, embedSafetyDocs, handleScriptTriggers, renderSchedule, renderDocs } from './ui-handlers.js';

let currentScene = 1;
let sceneStepIndex = 0;
let currentSessionSuffix = Date.now().toString();

const chatWindow = document.getElementById("chat-window");
const interactiveForms = document.getElementById("interactive-forms");

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
                imgDiv.innerHTML = '<img src="images/stop_work.png" alt="Stop Work Authority" style="max-width: 100%; border-radius: 8px; margin: 10px 0;">';
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
        } else if (selectedScene === 3) {
            updatePresets();
            addLog("Initiated End of Shift Plus/Delta session.");

            // Automatically send message to agent
            const userInput = document.getElementById("user-input");
            if (userInput) {
                userInput.value = "We are done for the day and are getting ready to wrap up.";
                document.getElementById("message-form").requestSubmit();
            }
        } else {
            currentScene = selectedScene;
            updatePresets();
            
            addLog(`Navigated to Scene ${currentScene}`);
        }
    });
});

// Send Message via Stream
const form = document.getElementById("message-form");
const input = document.getElementById("user-input");

if (input && form) {
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            form.requestSubmit();
        }
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
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
                                agentDiv.innerHTML = embedSafetyDocs(embedYouTube(parsedHtml)) + '<span class="typing-indicator"><span></span><span></span><span></span></span>';
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
            agentDiv.innerHTML = embedSafetyDocs(embedYouTube(parsedHtml));
            handleScriptTriggers(accumulatedText);
            
            if (accumulatedText.includes("PTP v2 Generated")) {
                const swatBtn = document.getElementById("scene-2-btn");
                if (swatBtn) {
                    swatBtn.disabled = false;
                    addLog("SWAT-2 button enabled.");
                }
            }
            
            if (accumulatedText.includes("PTP v3 Generated") || accumulatedText.includes("PTP v2 Generated")) {
                const eosBtn = document.getElementById("scene-3-btn");
                if (eosBtn) {
                    eosBtn.disabled = false;
                    addLog("End of Shift button enabled.");
                }
            }
            
            addLog("Received full streaming context.");
            
        } catch (error) {
            addLog(`Error: ${error.message}`);
            agentDiv.classList.remove("thinking");
            agentDiv.innerHTML = marked.parse(`**Error:** ${error.message || error}`);
        }
    });
}

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
                            agentDiv.innerHTML = embedSafetyDocs(marked.parse(accumulatedText)) + '<span class="typing-indicator"><span></span><span></span><span></span></span>';
                        }
                    } catch (err) { }
                }
            }
        }
        agentDiv.innerHTML = embedSafetyDocs(marked.parse(accumulatedText));
        chatWindow.scrollTop = chatWindow.scrollHeight;
    } catch (err) {
        agentDiv.innerHTML = embedSafetyDocs(marked.parse("Good morning! Welcome to UNO3 construction management system. Ready for shift briefs?"));
    }
}

window.addEventListener("DOMContentLoaded", triggerHiddenGreeting);

// Schedule Pane Logic
const showScheduleBtn = document.getElementById("show-schedule-btn");
const closeScheduleBtn = document.getElementById("close-schedule-btn");
const schedulePane = document.getElementById("schedule-pane");

const showDocsBtn = document.getElementById("show-docs-btn");
const closeDocsBtn = document.getElementById("close-docs-btn");
const docsPane = document.getElementById("docs-pane");

const showWeatherBtn = document.getElementById("show-weather-btn");
const closeWeatherBtn = document.getElementById("close-weather-btn");
const weatherPane = document.getElementById("weather-pane");

function closeAllPanes() {
    if (schedulePane) schedulePane.classList.remove("open");
    if (docsPane) docsPane.classList.remove("open");
    if (weatherPane) weatherPane.classList.remove("open");
}

// Schedule Pane Logic
if (showScheduleBtn && schedulePane && closeScheduleBtn) {
    showScheduleBtn.addEventListener("click", () => {
        closeAllPanes();
        renderSchedule();
        schedulePane.classList.add("open");
    });

    closeScheduleBtn.addEventListener("click", () => {
        schedulePane.classList.remove("open");
    });
}

// Docs Pane Logic
if (showDocsBtn && docsPane && closeDocsBtn) {
    showDocsBtn.addEventListener("click", () => {
        closeAllPanes();
        renderDocs();
        docsPane.classList.add("open");
    });

    closeDocsBtn.addEventListener("click", () => {
        docsPane.classList.remove("open");
    });
}

// Weather Pane Logic
if (showWeatherBtn && weatherPane && closeWeatherBtn) {
    showWeatherBtn.addEventListener("click", async () => {
        closeAllPanes();
        const weatherContent = document.getElementById("weather-content");
        if (weatherContent) {
            weatherContent.innerHTML = "<p>Loading weather advisory...</p>";
            try {
                const res = await fetch("/weather");
                const data = await res.json();
                weatherContent.innerHTML = `
                    <div class="weather-card">
                        <div class="weather-header">
                            <span class="weather-icon">🌧️</span>
                            <div class="weather-meta">
                                <h4>Weather Advisory</h4>
                                <span class="weather-status">Active Staging Conditions</span>
                            </div>
                        </div>
                        <div class="weather-body">
                            <p>${data.weather}</p>
                        </div>
                    </div>
                `;
            } catch (err) {
                weatherContent.innerHTML = `<p>Error loading weather: ${err.message}</p>`;
            }
        }
        weatherPane.classList.add("open");
    });

    closeWeatherBtn.addEventListener("click", () => {
        weatherPane.classList.remove("open");
    });
}
