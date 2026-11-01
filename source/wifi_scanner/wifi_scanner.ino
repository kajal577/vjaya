
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Arduino Smart Home Automation project using relay modules and voice commands.">
    <title>Smart Home Automation | VJaYa Robotics</title>

    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/project-detail.css">
</head>

<body>

<header class="site-header">
    <div class="container">
        <a href="index.html" class="brand">VJaYa Robotics</a>

        <nav>
            <a href="index.html">Home</a>
            <a href="projects.html">Projects</a>
            <a href="index.html#learn">Learn</a>
            <a href="index.html#store">Store</a>
        </nav>
    </div>
</header>

<main class="project-detail-page">

    <!-- HERO SECTION -->
    <section class="project-detail-hero">
        <div class="container">
            <p class="project-eyebrow">VJAYA ROBOTICS PROJECT 02</p>
            <span class="project-tag">Arduino Project</span>

            <h1>Smart Home Automation</h1>

            <p>
                Control household appliances such as lights and fans
                using an Arduino UNO, relay module and voice commands.
            </p>

            <a href="#project-overview" class="btn">Explore Project</a>
        </div>
    </section>

    <div class="container project-content-section">

        <!-- OVERVIEW -->
        <section id="project-overview">
            <h2>Project Overview</h2>

            <p>
                Smart Home Automation is an Arduino-based project
                designed to control electrical appliances using
                serial voice commands.
            </p>

            <p>
                The Arduino UNO receives commands and controls two
                relay outputs. One relay controls the light and
                the other controls the fan.
            </p>
        </section>

        <!-- FEATURES -->
        <section>
            <h2>Project Features</h2>

            <div class="project-info-grid">

                <div class="project-info-card">
                    <h3>Light Control</h3>
                    <p>Control the light using voice commands.</p>
                </div>

                <div class="project-info-card">
                    <h3>Fan Control</h3>
                    <p>Switch the fan using voice commands.</p>
                </div>

                <div class="project-info-card">
                    <h3>Relay Switching</h3>
                    <p>Two relay outputs control two appliances.</p>
                </div>

                <div class="project-info-card">
                    <h3>Serial Communication</h3>
                    <p>Arduino receives commands at 9600 baud.</p>
                </div>

            </div>
        </section>

        <!-- COMPONENTS -->
        <section>
            <h2>Required Components</h2>

            <ul class="project-list">
                <li>Arduino UNO</li>
                <li>2-Channel Relay Module</li>
                <li>Bluetooth Module (HC-05, if used in your setup)</li>
                <li>Light or demonstration load</li>
                <li>Fan or demonstration load</li>
                <li>Connecting wires</li>
                <li>Power supply suitable for the modules</li>
            </ul>
        </section>

        <!-- WIRING -->
        <section>
            <h2>Wiring Connections</h2>

            <p>
                The following relay pin connections are taken
                directly from your Arduino program.
            </p>

            <div class="project-table-wrapper">
                <table class="project-table">
                    <thead>
                        <tr>
                            <th>Component</th>
                            <th>Connection</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr>
                            <td>Light Relay IN</td>
                            <td>Arduino Digital Pin 7</td>
                        </tr>

                        <tr>
                            <td>Fan Relay IN</td>
                            <td>Arduino Digital Pin 8</td>
                        </tr>

                        <tr>
                            <td>Relay VCC</td>
                            <td>Compatible power supply</td>
                        </tr>

                        <tr>
                            <td>Relay GND</td>
                            <td>Arduino GND</td>
                        </tr>

                        <tr>
                            <td>Serial Communication</td>
                            <td>Arduino Hardware Serial</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <p class="project-note">
                Note: Your supplied sketch uses Serial communication.
                Confirm the actual Bluetooth module connections
                against your hardware setup before wiring.
            </p>
        </section>

        <!-- SOFTWARE -->
        <section>
            <h2>Software Requirements</h2>

            <ul class="project-list">
                <li>Arduino IDE</li>
                <li>Arduino UNO board support</li>
                <li>Serial voice-command application</li>
                <li>Bluetooth communication application, if using HC-05</li>
            </ul>
        </section>

        <!-- WORKING -->
        <section>
            <h2>How the Project Works</h2>

            <ol class="project-list">
                <li>Arduino initializes the relay output pins.</li>
                <li>The serial communication starts at 9600 baud.</li>
                <li>Arduino receives a command as text.</li>
                <li>The received command is converted to lowercase.</li>
                <li>Arduino checks whether the command is for the light or fan.</li>
                <li>The corresponding relay output is switched.</li>
                <li>The Arduino prints the appliance status.</li>
            </ol>
        </section>

        <!-- COMMANDS -->
        <section>
            <h2>Supported Voice Commands</h2>

            <div class="project-table-wrapper">
                <table class="project-table">
                    <thead>
                        <tr>
                            <th>Appliance</th>
                            <th>Command</th>
                            <th>Arduino Output</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr>
                            <td>Light</td>
                            <td>light off</td>
                            <td>Pin 7 HIGH</td>
                        </tr>

                        <tr>
                            <td>Light</td>
                            <td>light on</td>
                            <td>Pin 7 LOW</td>
                        </tr>

                        <tr>
                            <td>Light</td>
                            <td>turn off light</td>
                            <td>Pin 7 HIGH</td>
                        </tr>

                        <tr>
                            <td>Light</td>
                            <td>turn on light</td>
                            <td>Pin 7 LOW</td>
                        </tr>

                        <tr>
                            <td>Fan</td>
                            <td>fan off</td>
                            <td>Pin 8 HIGH</td>
                        </tr>

                        <tr>
                            <td>Fan</td>
                            <td>fan on</td>
                            <td>Pin 8 LOW</td>
                        </tr>

                        <tr>
                            <td>Fan</td>
                            <td>turn off fan</td>
                            <td>Pin 8 HIGH</td>
                        </tr>

                        <tr>
                            <td>Fan</td>
                            <td>turn on fan</td>
                            <td>Pin 8 LOW</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- SOURCE DOWNLOADS -->
        <section>
            <h2>Download Project Source Code</h2>

            <p>
                Download the original Arduino source code used
                in this project.
            </p>

            <div class="project-source-grid">

                <div class="project-source-card">
                    <h3>Arduino Main Code</h3>
                    <p>Original Smart Home Automation sketch.</p>

                    <a href="source/smart_home_automation/smart_home_automation.ino"
                       download>
                        Download .ino
                    </a>
                </div>

            </div>
        </section>

        <!-- DEMONSTRATION VIDEO -->
        <section>
            <h2>Project Demonstration Video</h2>

            <p>
                Watch the complete Smart Home Automation
                project demonstration here.
            </p>

            <div class="project-video-placeholder">
                <div>
                    <span class="video-icon">▶</span>
                    <h3>Video Coming Soon</h3>
                    <p>
                        Our project demonstration video
                        will be available here.
                    </p>
                </div>
            </div>
        </section>

    </div>
</main>

<footer class="site-footer">
    <div class="container">
        <p>© <span id="year"></span> VJaYa Robotics. All rights reserved.</p>
    </div>
</footer>

<script>
    document.getElementById("year").textContent =
        new Date().getFullYear();
</script>

</body>
</html>
