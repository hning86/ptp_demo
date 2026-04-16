const presetPrompts = {
    1: [
        { id: "btn_cable_pull", label: "Pull Cable", text: "We are at the UNO3 campus, Area B of the data hall. We are about to pull low voltage cable in aisle 3. The cable trays are already installed. I have a crew of 3 people today and we have 10 hours to get the work done." },
        { id: "btn_yes", label: "Yes", text: "Yes" },
        { id: "btn_no", label: "No", text: "No" },
        { id: "btn_new_members", label: "New Members", text: "We have 2 new crew members, ready for next step." },
        { id: "btn_ready", label: "Ready", text: "We are ready to review the pre-task plan." }
    ],
    2: [
        { id: "btn_cable_pull", label: "Take Two", text: "Take Two" },
        { id: "btn_yes", label: "Congestion", text: "The aisle is congested and the lift cannot access the work spot." },
        { id: "btn_no", label: "Yes", text: "Yes, extension ladder works fine." },
        { id: "btn_ready", label: "Good", text: "No, we are good to proceed." }
    ],
    3: [
        { id: "btn_cable_pull", label: "End Shift", text: "End of Shift" },
        { id: "btn_yes", label: "Delta", text: "The plan worked. Delta: Pre-installed trays had sharp edges that slowed progress." }
    ]
};

let currentScene = 1;
let sceneStepIndex = 0;
let currentSessionSuffix = Date.now().toString();
const chatWindow = document.getElementById("chat-window");
const visualBoard = document.getElementById("visual-board");
const cueText = document.getElementById("cue-text");
const interactiveForms = document.getElementById("interactive-forms");
const logList = document.getElementById("log-list");

const allShortcutIds = ["btn_cable_pull", "btn_yes", "btn_no", "btn_new_members", "btn_ready"];

// Setup quick preset buttons
function updatePresets() {
    allShortcutIds.forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.style.display = "none";
    });

    const presets = presetPrompts[currentScene] || [];
    presets.forEach(item => {
        const btn = document.getElementById(item.id);
        if (btn) {
            btn.textContent = item.label;
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
        currentScene = parseInt(btn.getAttribute("data-scene"));
        sceneStepIndex = 0;
        updatePresets();
        
        document.querySelectorAll(".scene-layer").forEach(l => l.classList.remove("active"));
        const tgt = document.getElementById("chat-scene-" + currentScene);
        if (tgt) tgt.classList.add("active");
        
        interactiveForms.innerHTML = "";
        
        if (currentScene === 2) {
            visualBoard.className = "visual-cue-board stop-sign";
            cueText.textContent = "STOP WORK AUTHORITY: Take Two Pause Initiated";
            addLog("Initiated midday periodic Stop Work authority check.");
        } else {
            visualBoard.className = "visual-cue-board";
            cueText.textContent = `Scene ${currentScene} initialized.`;
            addLog(`Navigated to Scene ${currentScene}`);
        }
    });
});

// Dynamic Interactive Form Rendering
function renderChecklist(options, onSelect) {
    interactiveForms.innerHTML = "";
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

// Process response side effects
function handleScriptTriggers(agentText) {
    // Check for specific conditions from the script to trigger immersive UI
    if (agentText.includes("finalize the task-specific elements") || agentText.includes("choose all that apply")) {
        visualBoard.textContent = "Verifying localized conditions...";
        renderChecklist(["Weather conditions", "New crew members", "Work area accessibility", "Egress", "Lighting"], (opt, sel) => {
            addLog(`Toggled ${opt}: ${sel}`);
        });
    } else if (agentText.includes("Take Two:") || agentText.includes("reassess your plan")) {
        visualBoard.className = "visual-cue-board stop-sign";
        cueText.textContent = "STOP SIGN: Periodic Change Audit in progress";
        renderChecklist(["Work Area Changes", "Tool Availability", "Material Availability", "Weather", "New Crew Members"], (opt, sel) => {});
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

    const activeLayer = document.getElementById("chat-scene-" + currentScene);
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
                            agentDiv.innerHTML = marked.parse(accumulatedText) + '<span class="typing-indicator"><span></span><span></span><span></span></span>';
                            chatWindow.scrollTop = chatWindow.scrollHeight;
                        }
                    } catch (err) {}
                }
            }
        }
        agentDiv.innerHTML = marked.parse(accumulatedText);
        handleScriptTriggers(accumulatedText);
        addLog("Received full streaming context.");
        
    } catch (error) {
        // Reliable mock fallbacks guaranteeing the presenter always wins!
        console.log("Using reliable automated templates...");
        let fallback = "Message received and processed successfully.";
        
        if (msg.includes("UNO3 campus") || msg.includes("pull low voltage cable")) {
            fallback = "Thank you. I have analyzed the requirements for low voltage cable pulling. Based on the P6 schedule, this cable pulling task overlaps with an overhead mechanical pipeline installation. Please make sure you take the below precautions: \n1. Secure lock-out/tag-out\n2. Implement edge shielding\n3. Coordinate air space. \nTo finalize the task-specific elements of today's plan, please choose all that apply:";
        } else if (msg.includes("new crew member")) {
            fallback = "Understood. I am updating your plan to Version 2. Today's weather is mild. Because you have a new crew member, I have added the following learning resources to your plan: \n- Toolbox Fall Hazards Doc\n- Scissor Lift Operations Video\n- Relevant past IRIS congestion logs.";
        } else if (msg.includes("congested") || msg.includes("lift cannot access")) {
            fallback = "Change identified. Would an extension ladder be a suitable alternative to access the overhead work area?";
        } else if (msg.includes("ladder will work")) {
            fallback = "OK I will update the plan to reflect the ladder usage, the requirements inspection procedures. Action Required: A supervisor must sign this permit before ladder work resumes. Do you accept these updates?";
        } else if (msg.includes("Updates accepted")) {
            fallback = "Also tell me how are the crew doing. Any mental or physical fatigue concerns?";
        } else if (msg.includes("overwhelmed")) {
            fallback = "I suggest a 20 minutes break and recharge time. I will build that into the revised plan. Anything else?";
        } else if (msg.includes("plan worked")) {
            fallback = "Thank you. I have captured your Plus/Delta findings. I will integrate this edge-guard recommendation into future PTPs for this campus so the system becomes smarter for the next run. I am now archiving today's final plan.";
        }
        
        agentDiv.innerHTML = marked.parse(fallback);
        handleScriptTriggers(fallback);
        addLog("Mock simulation response applied.");
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
