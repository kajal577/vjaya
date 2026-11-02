#include "server.h"
#include "groq_client.h"
#include "display.h"
#include "wifi_manager.h"
#include "config.h"

#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <LittleFS.h>

WebServer server(80);

// =====================================================
// SETTINGS
// =====================================================
#define STT_FILE "/recording.webm"

const char *GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions";
const char *GROQ_STT_MODEL = "whisper-large-v3-turbo";

// =====================================================
// AUDIO UPLOAD VARIABLES
// =====================================================
File uploadFile;
bool uploadStarted = false;
size_t uploadedBytes = 0;

// =====================================================
// MAIN WEB PAGE (CLEAN CONTROL PANEL FOR FAN & MUSIC)
// =====================================================
const char MAIN_PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Muskan AI Assistant</title>
<style>
body { font-family: Arial, sans-serif; background: #111; color: white; text-align: center; margin: 0; padding: 20px; }
.container { max-width: 600px; margin: auto; }
h1 { margin-bottom: 20px; color: #00f5d4; }
textarea { width: 95%; height: 100px; padding: 12px; font-size: 18px; border-radius: 10px; border: none; resize: none; box-sizing: border-box; background: #222; color: #fff; }
button { margin: 10px 5px; padding: 12px 20px; font-size: 17px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
.askButton { background: #2196F3; color: white; }
.speakButton { background: #4CAF50; color: white; }
.speakButton:disabled { background: #777; cursor: not-allowed; }
.ctrl-section { margin-top: 25px; padding: 15px; background: #1a1a2e; border-radius: 10px; border: 1px solid #333; }
.ctrl-title { font-size: 18px; margin-bottom: 10px; font-weight: bold; color: #00bbf9; }
.fan-on { background: #00bbf9; color: white; }
.fan-off { background: #f15bb5; color: white; }
.music-on { background: #9b5de5; color: white; }
.music-off { background: #f15bb5; color: white; }
#status { margin-top: 10px; font-size: 16px; color: #aaa; }
#answer { margin-top: 20px; padding: 15px; background: #222; border-radius: 10px; text-align: left; min-height: 50px; white-space: pre-wrap; }
</style>
</head>
<body>
<div class="container">
<h1>🤖 Muskan AI Fan & Music Controller</h1>

<textarea id="question" placeholder="Type your question here..."></textarea>
<br>
<button class="askButton" onclick="askAI()">Ask AI</button>
<button id="speakButton" class="speakButton" onclick="startVoice()">🎤 Speak</button>

<!-- NEW WEB INTERFACE PANEL FOR RELAY & MUSIC MODULE -->
<div class="ctrl-section">
    <div class="ctrl-title">🌀 Fan Control (Relay)</div>
    <button class="fan-on" onclick="sendControl('fan on')">Turn Fan ON</button>
    <button class="fan-off" onclick="sendControl('fan off')">Turn Fan OFF</button>
</div>

<div class="ctrl-section">
    <div class="ctrl-title">🎵 Music Control (DFPlayer)</div>
    <button class="music-on" onclick="sendControl('music on')">Play Music</button>
    <button class="music-off" onclick="sendControl('music off')">Stop Music</button>
</div>

<div id="status">Ready</div>
<div id="answer">Ready...</div>
</div>

<script>
let mediaRecorder = null;
let audioChunks = [];
let recording = false;

function setStatus(text) {
    const status = document.getElementById("status");
    if (status) { status.innerHTML = text; }
}

async function startVoice() {
    console.log("Speak button pressed");
    if (recording) { console.log("Already recording"); return; }
    try {
        setStatus("Requesting microphone...");
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        console.log("Microphone permission granted");
        audioChunks = [];
        let options = { mimeType: "audio/webm;codecs=opus" };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            console.log("WebM Opus not supported");
            options = {};
        }
        mediaRecorder = new MediaRecorder(stream, options);
        mediaRecorder.ondataavailable = function(event) {
            if (event.data && event.data.size > 0) { audioChunks.push(event.data); }
        };
        mediaRecorder.onstop = function() {
            console.log("Recording stopped");
            stream.getTracks().forEach(track => track.stop());
            const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType || "audio/webm" });
            console.log("Audio size:", audioBlob.size);
            uploadAudio(audioBlob);
        };
        mediaRecorder.start();
        recording = true;
        const button = document.getElementById("speakButton");
        if (button) { button.disabled = false; button.innerHTML = "⏹ Stop"; }
        setStatus("🔴 Listening... Speak now");
        console.log("Recording started");
        setTimeout(function() { if (recording) { stopRecording(); } }, 8000);
    } catch(error) {
        console.log("Microphone error:", error);
        recording = false;
        setStatus("Microphone error");
        alert("Could not access microphone: " + error.name + " - " + error.message);
    }
}

function stopRecording() {
    if (!mediaRecorder) return;
    if (mediaRecorder.state === "recording") {
        console.log("Stopping recording");
        mediaRecorder.stop();
        recording = false;
        const button = document.getElementById("speakButton");
        if (button) { button.disabled = true; button.innerHTML = "⏳ Processing..."; }
        setStatus("Uploading audio...");
    }
}

async function uploadAudio(blob) {
    console.log("Uploading audio to ESP32");
    // Rest of your standard JavaScript upload execution infrastructure...
}

// HANDLES QUICK COMMAND BUTTON CLICKS FROM THE PANEL
function sendControl(commandText) {
    document.getElementById("question").value = commandText;
    askAI();
}

async function askAI() {
    const q = document.getElementById("question").value;
    if(!q.trim()) return;
    setStatus("Thinking...");
    try {
        const res = await fetch("/ask?q=" + encodeURIComponent(q));
        const text = await res.text();
        document.getElementById("answer").innerText = text;
        setStatus("Ready");
    } catch(e) {
        setStatus("Error sending request");
    }
}
</script>
</body>
</html>
)rawliteral";

// =====================================================
// SERVER ROUTING HANDLERS
// =====================================================
void handleRoot() {
    server.send(200, "text/html", MAIN_PAGE);
}

void handleAsk() {
    if (!server.hasArg("q")) {
        server.send(400, "text/plain", "Missing query parameter 'q'");
        return;
    }
    String question = server.arg("q");
    String answer = askGroq(question);
    server.send(200, "text/plain", answer);
}

// =====================================================
// INITIALIZE WEB SERVER (Called in your main setup())
// =====================================================
void initServer() {
    // Route for the main HTML control dashboard page
    server.on("/", HTTP_GET, handleRoot);
    
    // Route for text/voice queries submitted via buttons or input fields
    server.on("/ask", HTTP_GET, handleAsk);

    // Start running the HTTP server pipeline
    server.begin();
    
    Serial.println("==============================");
    Serial.println("Web server started successfully!");
    Serial.println("==============================");
}

// =====================================================
// HANDLE INCOMING CLIENTS (Called in your main loop())
// =====================================================
void handleServer() {
    server.handleClient();
}


// Rest of your file's WebServer stream parsing routes continue cleanly down here...
