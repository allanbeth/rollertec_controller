// --- Utility Functions ---

function escapeHTML(str) {
    return str.replace(/[&<>"']/g, match => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }[match]));
}

// --- Navigation Active State Helper ---

/**
 * Sets the active class on the navigation icon for the current view.
 * @param {string} navId - The ID of the navigation link to activate.
 */
function setActiveNav(navId) {
    document.querySelectorAll('.nav-icons a').forEach(a => a.classList.remove('active'));
    const active = document.getElementById(navId);
    if (active) active.classList.add('active');
}

// --- UI Navigation ---

function showContainer(containerId) {
    document.getElementById('control-container').style.display = 'none';
    document.getElementById('log-container').style.display = 'none';
    document.getElementById('config-container').style.display = 'none';
    document.getElementById('about-container').style.display = 'none';
    document.getElementById(containerId).style.display = '';
}

// --- Command Sending ---

function sendCommand(action) {
    fetch('/' + action, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = "Status: " + data.status;
        })
        .catch(() => {
            document.getElementById("status").innerText = "Error sending command.";
        });
}

// --- Log Fetching ---

function fetchLog() {
    const logContainer = document.getElementById("log-content");
    logContainer.innerHTML = "<p>Loading logs...</p>";

    fetch('/log')
        .then(response => response.json())
        .then(data => {
            const logEntries = data.logs ?? [];

            if (logEntries.length === 0) {
                logContainer.innerHTML = "<p>No log data found.</p>";
                return;
            }
            const LOG_ENTRY_REGEX = /^\s*([\d\-:, ]+)\s+([A-Z]+)\s+(.*)$/;

            const logFileHTML = logEntries.map(entry => {
                const logText = entry.logs.trim();
                const match = logText.match(LOG_ENTRY_REGEX);

                if (match) {
                    const logDate = match[1];
                    const logType = match[2];
                    const logMessage = match[3];
                    return `
                        <div class="log-entry">
                            <p>
                                <strong style="font-weight:bold;">${escapeHTML(logDate)}</strong>
                                <strong style="color:green;"> ${escapeHTML(logType)}</strong>
                                ${escapeHTML(logMessage)}
                            </p>
                        </div>
                    `;
                } else {
                    return `<div class="log-entry"><p>${escapeHTML(logText)}</p></div>`;
                }
            }).join('');

            logContainer.innerHTML = logFileHTML;
        })
        .catch(error => {
            logContainer.innerHTML = "<p>Failed to load logs.</p>";
            console.error("Log fetch error:", error);
        });
}

// --- Config Form Handling ---

function handleConfigFormSubmit(e) {
    e.preventDefault();
    const configForm = document.getElementById("config-form");
    const configCard = document.getElementById("config-card");

    const formData = new FormData(configForm);
    const configData = {};

    configData.max_log = parseInt(formData.get("max_log")) || 0;
    configData.open_pin = parseInt(formData.get("open_pin")) || 0;
    configData.close_pin = parseInt(formData.get("close_pin")) || 0;
    configData.stop_pin = parseInt(formData.get("stop_pin")) || 0;
    configData.roller_time = parseInt(formData.get("roller_time")) || 0;
    configData.press_time = parseInt(formData.get("press_time")) || 0;
    configData.stop_btn = document.getElementById("stop_btn").checked ? 1 : 0;
    configData.mqtt_broker = formData.get("mqtt_broker") || "";
    configData.mqtt_port = parseInt(formData.get("mqtt_port")) || 0;
    configData.webserver_host = formData.get("webserver_host") || "";
    const webserverPortValue = parseInt(formData.get("webserver_port"));
    configData.webserver_port = isNaN(webserverPortValue) ? 0 : webserverPortValue;
    configData.remote_gpio = document.getElementById("remote_gpio").checked ? 1 : 0;
    configData.gpio_address = formData.get("gpio_address") || "";

    fetch('/config', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(configData)
})
.then(async response => {
    // Hide the form and show a large tick
    configForm.style.display = "none";
    // Remove any existing tick/message
    let oldSuccess = document.getElementById("config-success");
    if (oldSuccess) oldSuccess.remove();

    // Create success container
    const success = document.createElement("div");
    success.id = "config-success";
    success.className = "config-success";

    // Create tick and message
    const tick = document.createElement("span");
    tick.id = "config-success-tick";
    tick.className = "config-success-tick";
    tick.innerHTML = `<i class="fas fa-check"></i>`;

    const msg = document.createElement("p");
    msg.id = "config-success-msg";
    msg.className = "config-success-msg";
    msg.innerHTML = "Configuration saved successfully!";

    // Append tick and message to success container
    success.appendChild(tick);
    success.appendChild(msg);

    // Append success container to config card
    configCard.appendChild(success);

    setTimeout(() => {
    // Remove tick/message, show form, go back to main controls
    if (success) success.remove();
    configForm.style.display = "";
    // Dynamically update Stop button visibility
    const stopBtnCheckbox = document.getElementById("stop_btn");
    const stopBtn = document.getElementById("stop-btn");
    if (stopBtnCheckbox && stopBtn) {
        if (stopBtnCheckbox.checked) {
            stopBtn.style.display = "";
        } else {
            stopBtn.style.display = "none";
        }
    }
        showContainer('control-container');
        setActiveNav('show-buttons-link');
}, 1000);

    if (response.ok) {
        return "Saved!";
    } else {
        let errorMsg = "Save failed";
        try {
            const errorData = await response.json();
            if (errorData && errorData.error) {
                errorMsg += ": " + errorData.error;
            }
        } catch (e) {}
        return errorMsg;
    }
})
.catch(() => {
    // Optionally handle error if needed
});
}

/**
 * Fetches the README file content from the backend and displays it in the about container.
 */
function fetchReadme() {
    const aboutContent = document.getElementById("about-content");
    if (aboutContent) {
        aboutContent.innerHTML = "<p>Loading...</p>";
    }

    fetch('/about')
        .then(res => res.json())
        .then(data => {
            if (data.content) {
                aboutContent.innerHTML = marked.parse(data.content);
            } else if (data.error) {
                aboutContent.innerHTML = `<p style="color:red;">${escapeHTML(data.error)}</p>`;
            } else {
                aboutContent.innerHTML = "<p>No about information found.</p>";
            }
        })
        .catch(() => {
            if (aboutContent) {
                aboutContent.innerHTML = "<p style='color:red;'>Failed to load about information.</p>";
            }
        });
}


// --- Event Listeners ---

document.addEventListener("DOMContentLoaded", function() {
    // Navigation links
    const showButtonsLink = document.getElementById("show-buttons-link");
    const showLogLink = document.getElementById("show-log-link");
    const showConfigLink = document.getElementById("show-config-link");
    const showAboutLink = document.getElementById("show-about-link");

    if (showButtonsLink) {
    showButtonsLink.addEventListener("click", function(e) {
        e.preventDefault();
        showContainer('control-container');
        setActiveNav('show-buttons-link');
    });
}
if (showLogLink) {
    showLogLink.addEventListener("click", function(e) {
        e.preventDefault();
        fetchLog();
        showContainer('log-container');
        setActiveNav('show-log-link');
    });
}
if (showConfigLink) {
    showConfigLink.addEventListener("click", function(e) {
        e.preventDefault();
        showContainer('config-container');
        setActiveNav('show-config-link');
    });
}
if (showAboutLink) {
    showAboutLink.addEventListener("click", function(e) {
        e.preventDefault();
        showContainer('about-container');
        setActiveNav('show-about-link');
        fetchReadme();
    });

}

    // Control buttons
    const controlCard = document.getElementById("control-card");
    const stopBtn = document.getElementById("stop-btn");
    if (controlCard && controlCard.dataset.stopBtn === "0") {
        if (stopBtn) stopBtn.style.display = "none";
    }
    const openBtn = document.getElementById("open-btn");
    const closeBtn = document.getElementById("close-btn");

    if (openBtn) openBtn.addEventListener("click", () => sendCommand('open'));
    if (stopBtn) stopBtn.addEventListener("click", () => sendCommand('stop'));
    if (closeBtn) closeBtn.addEventListener("click", () => sendCommand('close'));

    // Refresh log button
    const refreshBtn = document.getElementById("refresh-log-btn");
    if (refreshBtn) {
        refreshBtn.addEventListener("click", function(e) {
            e.preventDefault();
            fetchLog();
        });
    }

    // Config form save button
    const configForm = document.getElementById("config-form");
    const saveBtn = document.getElementById("save-config-btn");
    if (saveBtn && configForm) {
        saveBtn.addEventListener("click", function(e) {
            e.preventDefault();
            configForm.requestSubmit(); // Triggers the form's submit event
        });
    }
    if (configForm) {
        configForm.onsubmit = handleConfigFormSubmit;
    }

    // Set control card nav as active on initial load
    setActiveNav('show-buttons-link');
    
});