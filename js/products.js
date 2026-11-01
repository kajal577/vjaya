
// ==========================================
// VJAYA ROBOTICS STORE - PRODUCT CATALOGUE
// ==========================================

const products = [

    // ======================================
    // DEVELOPMENT BOARDS
    // ======================================

    {
        id: 1,
        name: "ESP32 Development Board",
        category: "Microcontrollers",
        description: "Wi-Fi and Bluetooth development board.",
        price: 450,
        icon: "📟"
    },
    {
        id: 2,
        name: "Arduino UNO Compatible",
        category: "Microcontrollers",
        description: "Beginner-friendly microcontroller board.",
        price: 550,
        icon: "🔌"
    },
    {
        id: 7,
        name: "Arduino Nano",
        category: "Microcontrollers",
        description: "Compact board for embedded robotics projects.",
        price: 250,
        icon: "📟"
    },
    {
        id: 8,
        name: "Arduino Mega 2560",
        category: "Microcontrollers",
        description: "Microcontroller with many input and output pins.",
        price: 850,
        icon: "🖥️"
    },
    {
        id: 9,
        name: "ESP32-CAM",
        category: "Microcontrollers",
        description: "ESP32 board with an integrated camera.",
        price: 650,
        icon: "📷"
    },
    {
        id: 10,
        name: "Raspberry Pi Pico",
        category: "Microcontrollers",
        description: "Compact RP2040 microcontroller development board.",
        price: 400,
        icon: "💻"
    },
    {
        id: 11,
        name: "NodeMCU ESP8266",
        category: "Microcontrollers",
        description: "Wi-Fi development board for IoT projects.",
        price: 300,
        icon: "📡"
    },

	{
    id: 33,
    name: "ESP32-S3 Development Board",
    category: "Microcontrollers",
    description: "Advanced ESP32 board with Wi-Fi, Bluetooth LE and AI-friendly processing.",
    price: 550,
    icon: "📟"
},
{
    id: 34,
    name: "ESP32-C3 Development Board",
    category: "Microcontrollers",
    description: "Compact RISC-V microcontroller with Wi-Fi and Bluetooth LE.",
    price: 300,
    icon: "📟"
},
{
    id: 35,
    name: "Arduino Leonardo",
    category: "Microcontrollers",
    description: "Arduino board with native USB communication.",
    price: 650,
    icon: "🔌"
},
{
    id: 36,
    name: "STM32 Blue Pill",
    category: "Microcontrollers",
    description: "32-bit ARM Cortex-M3 microcontroller development board.",
    price: 180,
    icon: "📟"
},
{
    id: 37,
    name: "Raspberry Pi Pico W",
    category: "Microcontrollers",
    description: "RP2040 microcontroller board with Wi-Fi connectivity.",
    price: 450,
    icon: "📟"
},

    // ======================================
    // SENSORS
    // ======================================

    {
        id: 3,
        name: "Ultrasonic Sensor HC-SR04",
        category: "Sensors",
        description: "Measure distance for obstacle detection.",
        price: 120,
        icon: "📡"
    },
    {
        id: 12,
        name: "IR Sensor Module",
        category: "Sensors",
        description: "Detect nearby objects and line surfaces.",
        price: 60,
        icon: "🔴"
    },
    {
        id: 13,
        name: "PIR Motion Sensor",
        category: "Sensors",
        description: "Detect movement using infrared radiation.",
        price: 100,
        icon: "🚶"
    },
    {
        id: 14,
        name: "DHT11 Temperature Sensor",
        category: "Sensors",
        description: "Measure temperature and humidity.",
        price: 90,
        icon: "🌡️"
    },
    {
        id: 15,
        name: "Soil Moisture Sensor",
        category: "Sensors",
        description: "Monitor soil moisture for smart irrigation.",
        price: 70,
        icon: "🌱"
    },
    {
        id: 16,
        name: "MPU6050 Gyroscope",
        category: "Sensors",
        description: "Six-axis motion and orientation sensor.",
        price: 180,
        icon: "🧭"
    },
    {
        id: 17,
        name: "MQ-2 Gas Sensor",
        category: "Sensors",
        description: "Detect smoke and certain combustible gases.",
        price: 130,
        icon: "💨"
    },


	{
    id: 38,
    name: "Flame Sensor Module",
    category: "Sensors",
    description: "Detects flame using infrared light for fire detection projects.",
    price: 80,
    icon: "🔥"
},
{
    id: 39,
    name: "Rain Sensor Module",
    category: "Sensors",
    description: "Detects rain and water droplets for weather monitoring projects.",
    price: 90,
    icon: "🌧️"
},
{
    id: 40,
    name: "Sound Sensor Module",
    category: "Sensors",
    description: "Detects sound levels for sound-activated robotics projects.",
    price: 70,
    icon: "🔊"
},
{
    id: 41,
    name: "Touch Sensor TTP223",
    category: "Sensors",
    description: "Capacitive touch sensor for touch-controlled projects.",
    price: 40,
    icon: "👆"
},
{
    id: 42,
    name: "Water Level Sensor",
    category: "Sensors",
    description: "Detects water level for tank monitoring and automation.",
    price: 80,
    icon: "💧"
},
{
    id: 43,
    name: "TCS34725 Color Sensor",
    category: "Sensors",
    description: "Detects colors using RGB light sensing.",
    price: 180,
    icon: "🌈"
},
{
    id: 44,
    name: "R307 Fingerprint Sensor",
    category: "Sensors",
    description: "Fingerprint recognition module for biometric access-control projects.",
    price: 450,
    icon: "🔐"
},




    // ======================================
    // MOTORS
    // ======================================

    {
        id: 4,
        name: "SG90 Servo Motor",
        category: "Motors",
        description: "Small servo for robotic arms and grippers.",
        price: 150,
        icon: "⚙️"
    },
    {
        id: 18,
        name: "DC Gear Motor",
        category: "Motors",
        description: "Geared DC motor for mobile robots.",
        price: 180,
        icon: "⚙️"
    },
    {
        id: 19,
        name: "BO Motor",
        category: "Motors",
        description: "DC geared motor for robot cars.",
        price: 100,
        icon: "🚗"
    },
    {
        id: 20,
        name: "NEMA 17 Stepper Motor",
        category: "Motors",
        description: "Precision stepper motor for robotics and CNC.",
        price: 850,
        icon: "🔄"
    },
    {
        id: 21,
        name: "MG996R Servo Motor",
        category: "Motors",
        description: "High-torque servo for robotic mechanisms.",
        price: 350,
        icon: "🦾"
    },
    {
        id: 22,
        name: "28BYJ-48 Stepper Motor",
        category: "Motors",
        description: "Compact geared stepper motor.",
        price: 120,
        icon: "🔄"
    },

    // ======================================
    // MOTOR DRIVERS
    // ======================================

    {
        id: 5,
        name: "L298N Motor Driver",
        category: "Drivers",
        description: "Control two DC motors independently.",
        price: 180,
        icon: "🧩"
    },
    {
        id: 23,
        name: "L293D Motor Driver",
        category: "Drivers",
        description: "Dual H-bridge motor driver IC/module.",
        price: 100,
        icon: "🔌"
    },
    {
        id: 24,
        name: "BTS7960 Motor Driver",
        category: "Drivers",
        description: "High-current motor driver module.",
        price: 450,
        icon: "⚡"
    },

    // ======================================
    // RELAY AND COMMUNICATION MODULES
    // ======================================

    {
        id: 25,
        name: "1-Channel Relay Module",
        category: "Modules",
        description: "Switch electrical loads using a control signal.",
        price: 80,
        icon: "🔋"
    },
    {
        id: 26,
        name: "4-Channel Relay Module",
        category: "Modules",
        description: "Control four separate electrical circuits.",
        price: 180,
        icon: "🔌"
    },
    {
        id: 27,
        name: "HC-05 Bluetooth Module",
        category: "Modules",
        description: "Bluetooth serial communication for Arduino.",
        price: 250,
        icon: "📶"
    },

    // ======================================
    // ROBOTICS KITS AND ACCESSORIES
    // ======================================

    {
        id: 6,
        name: "Robot Car Starter Kit",
        category: "Kits",
        description: "Starter kit concept for building a mobile robot.",
        price: 999,
        icon: "🚗"
    },
    {
        id: 28,
        name: "Robot Car Chassis",
        category: "Accessories",
        description: "Chassis platform for DIY robot cars.",
        price: 250,
        icon: "🚙"
    },
    {
        id: 29,
        name: "Jumper Wire Set",
        category: "Accessories",
        description: "Male-to-male, male-to-female and female-to-female wires.",
        price: 100,
        icon: "🔗"
    },
    {
        id: 30,
        name: "Breadboard",
        category: "Accessories",
        description: "Reusable solderless prototyping board.",
        price: 90,
        icon: "🧱"
    },
    {
        id: 31,
        name: "Battery Holder",
        category: "Accessories",
        description: "Battery holder for powering robotics projects.",
        price: 60,
        icon: "🔋"
    },
    {
        id: 32,
        name: "Robot Wheel and Caster Set",
        category: "Accessories",
        description: "Wheels and caster for mobile robot platforms.",
        price: 180,
        icon: "🛞"
    }

];
