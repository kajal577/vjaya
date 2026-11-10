const roboticsProjects = [
    {
        id: "wifi_scanner",
        name: "ESP32 WIFI SCANNER & SETUP PORTAL",
        platform: "ESP32",
        description: "Scan nearby WiFi networks, view SSID and signal strength on an OLED, and configure WiFi through a phone-friendly setup portal.",
        page: "wifi_scanner.html"
    },

    {
        id: "smart_home_automation",
        name: "SMART HOME AUTOMATION",
        platform: "Arduino",
        description: "Arduino smart home automation project. Project details and source code will be added.",
        page: "smart_home_automation.html"
    },

    {
        id: "maze_solver_car",
        name: "MAZE SOLVER CAR",
        platform: "Arduino",
        description: "Arduino maze-solving robot car project. Project details and source code will be added.",
        page: "maze_solver_car.html"
    },

    {
        id: "security_door_lock",
        name: "SMART SECURITY DOOR LOCK",
        platform: "ESP32",
        description: "ESP32 smart door lock using an SG90 servo, vibration detection, WiFi web control, voice commands and Telegram emergency alerts.",
        page: "security_door_lock.html"
    },

    {
        id: "smart_home_gesture_control",
        name: "SMART HOME GESTURE CONTROL",
        platform: "Arduino",
        description: "Control smart home devices using hand gestures detected by a webcam and processed with Python and OpenCV.",
        page: "smart_home_gesture_control.html"
    },

    {
        id: "ai_vision_robot_car",
        name: "AI VISION ROBOT CAR",
        platform: "Arduino",
        description: "Control a robot car using hand gesture detection with Python, OpenCV and MediaPipe, sending movement commands to an Arduino.",
        page: "ai_vision_robot_car.html"
    },

    {
        id: "ai_assisstant",
        name: "AI ASSISTANT",
        platform: "ESP32",
        description: "An AI assistant project using ESP32, capable of voice recognition and natural language processing.",
        page: "ai_assistant.html"
    },
    {
       id: "ai_vision_robot",
        name: "AI VISION ROBOT",
        platform: "esp32",
        description: "An AI vision robot project using esp32 ,python code, capable of recognizing objects and navigating through web camera input.",
        page: "ai_vision_robot.html"                                                
    },
    {
         id: "offline_google",
         name: "OFFLINE GOOGLE ASSISTANT",
         platform: "esp32",
         description: "An offline google assistant project using esp32 ,python code, capable of recognizing voice commands and responding without internet.",
         page: "offline_google.html"
    },
    {
        id: "gps_navigation_car",
        name: "GPS NAVIGATION CAR",
        platform: "Arduino",
        description: "An Arduino GPS navigation car project using GPS module and motor driver to navigate through predefined waypoints.",
        page: "gps_navigation_car.html"
    },
    {
        id: "object_avoidance_car",
        name: "OBJECT AVOIDANCE CAR",
        platform: "Arduino",
        description: "An Arduino object avoidance car project using ultrasonic sensors to detect obstacles and navigate around them.",
        page: "object_avoidance_car.html"
    },
    {
        id: "line_follower_car",
        name: "LINE FOLLOWER CAR",
        platform: "Arduino",
        description: "An Arduino line follower car project using infrared sensors to follow a line on the ground.",
        page: "line_follower_car.html"
    },
    {
        id: "bluetooth_controlled_car",
        name: "BLUETOOTH CONTROLLED CAR",
        platform: "Arduino",
        description: "An Arduino Bluetooth controlled car project using a Bluetooth module and motor driver to control the car with a smartphone.",
        page: "bluetooth_controlled_car.html"
    },
];

const pageParams = new URLSearchParams(window.location.search);
let selectedPlatform = pageParams.get("platform") || "All";

function renderProjects() {
    const grid = document.getElementById("projects-grid");

    const filteredProjects = roboticsProjects.filter(project => {
        return selectedPlatform === "All" ||
               project.platform === selectedPlatform;
    });

    if (filteredProjects.length === 0) {
        grid.innerHTML = `
            <div class="project-empty">
                <h3>No projects added yet!</h3>
                <p>
                    Robotics projects for ${selectedPlatform}
                    will appear here.
                </p>
            </div>
        `;
        return;
    }

    grid.innerHTML = filteredProjects.map(project => `
        <article class="feature-card">
            <div class="feature-icon">🤖</div>
            <p class="eyebrow">${project.platform}</p>
            <h3>${project.name}</h3>
            <p>${project.description}</p>
            <a class="button secondary" href="${project.page}">
                View Project
            </a>
        </article>
    `).join("");
}

document.addEventListener("DOMContentLoaded", () => {

    const filterButtons = document.querySelectorAll(
        ".project-filters button"
    );

    filterButtons.forEach(button => {

        button.classList.toggle(
            "active",
            button.dataset.platform === selectedPlatform
        );

        button.addEventListener("click", () => {
            selectedPlatform = button.dataset.platform;

            filterButtons.forEach(item => {
                item.classList.toggle(
                    "active",
                    item.dataset.platform === selectedPlatform
                );
            });

            renderProjects();
        });
    });

    document.getElementById("project-year").textContent =
        new Date().getFullYear();

    renderProjects();
});
