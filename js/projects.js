
const roboticsProjects = [
    {
        id: "wifi_scanner",
        name: "ESP32 WiFi Scanner & Setup Portal",
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
        description: "Build an autonomous Arduino UNO robot car that scans its surroundings and navigates around obstacles.",
        page: "maze_solver_car.html"
    },

    {
    id: "self_balancing_robot",
    name: "SELF-BALANCING ROBOT",
    platform: "Arduino",
    description: "Build a two-wheel self-balancing robot using Arduino UNO, MPU6050, L298N motor driver and Bluetooth control.",
    page: "self_balancing_robot.html"
    },
     {
        id: "security_door_lock",
        name: "SMART SECURITY DOOR LOCK",
        platform: "ESP32",
        description: "ESP32 smart door lock using an SG90 servo, vibration detection, WiFi web control, voice commands and Telegram emergency alerts.",
        page: "security_door_lock.html"
    },
        {
        id: "gps_navigation_car",
        name: "GPS NAVIGATION CAR",
        platform: "Arduino",
        description: "Build an Arduino UNO navigation car using GPS positioning, QMC5883L compass, HC-05 Bluetooth and ultrasonic obstacle detection.",
        page: "gps_navigation_car.html"
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
