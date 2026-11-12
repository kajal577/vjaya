
// ==========================================
// VJAYA ROBOTICS STORE - PRODUCT CATALOGUE
// ==========================================

const products = [

    // ======================================
    // jumper wires
    // ======================================

     {
        id: 32,
        name: "male to male",
        category: "boards",
        description: "Wheels and caster for mobile robot platforms.",
        price: 10,
        stock: 20,
        icon: "🛞"
    },

    {
        id: 32,
        name: "male to female",
        category: "boards",
        description: "Wheels and caster for mobile robot platforms.",
        price: 10,
        stock: 20,
        icon: "🛞"
    },
    {
        id: 32,
        name: "female to female",
        category: "boards",
        description: "Wheels and caster for mobile robot platforms.",
        price: 10,
        stock: 20,
        icon: "🛞"
    },

    // ======================================
    // DEVELOPMENT BOARDS
    // ======================================

   

    {
        id: 1,
        name: "ESP32 Development Board",
        category: "Microcontrollers",
        description: "Wi-Fi and Bluetooth development board.",
        price: 450,
        stock: 20,
        icon: "📟"
    },
    {
        id: 2,
        name: "Arduino UNO Compatible",
        category: "Microcontrollers",
        description: "Beginner-friendly microcontroller board.",
        price: 550,
        stock: 20,
        icon: "🔌"
    },
    {
        id: 7,
        name: "Arduino Nano",
        category: "Microcontrollers",
        description: "Compact board for embedded robotics projects.",
        price: 250,
        stock: 20,
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
        stock: 20,
        icon: "📷"
    },
    {
        id: 10,
        name: "Raspberry Pi Pico",
        category: "Microcontrollers",
        description: "Compact RP2040 microcontroller development board.",
        price: 400,
        stock: 20,
        icon: "💻"
    },
    {
        id: 11,
        name: "NodeMCU ESP8266",
        category: "Microcontrollers",
        description: "Wi-Fi development board for IoT projects.",
        price: 300,
        stock: 20,
        icon: "📡"
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
        stock: 20,
        icon: "📡"
    },
    {
        id: 12,
        name: "IR Sensor Module",
        category: "Sensors",
        description: "Detect nearby objects and line surfaces.",
        price: 60,
        stock: 20,
        icon: "🔴"
    },
    {
        id: 13,
        name: "PIR Motion Sensor",
        category: "Sensors",
        description: "Detect movement using infrared radiation.",
        price: 100,
        stock: 20,
        icon: "🚶"
    },
    {
        id: 14,
        name: "DHT11 Temperature Sensor",
        category: "Sensors",
        description: "Measure temperature and humidity.",
        price: 90,
        stock: 20,  
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
        stock: 20,
        icon: "🧭"
    },
    {
        id: 17,
        name: "MQ-2 Gas Sensor",
        category: "Sensors",
        description: "Detect smoke and certain combustible gases.",
        price: 130,
        stock: 20,
        icon: "💨"
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
        stock: 20,
        icon: "⚙️"
    },
    {
        id: 18,
        name: "DC Gear Motor",
        category: "Motors",
        description: "Geared DC motor for mobile robots.",
        price: 180,
        stock: 20,
        icon: "⚙️"
    },
    {
        id: 19,
        name: "BO Motor",
        category: "Motors",
        description: "DC geared motor for robot cars.",
        price: 100,
        stock: 20,
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
        stock: 20,
        icon: "🦾"
    },
    {
        id: 22,
        name: "28BYJ-48 Stepper Motor",
        category: "Motors",
        description: "Compact geared stepper motor.",
        price: 120,
        stock: 20,
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
        stock: 20,
        icon: "🧩"
    },
    {
        id: 23,
        name: "L293D Motor Driver",
        category: "Drivers",
        description: "Dual H-bridge motor driver IC/module.",
        price: 100,
        stock: 20,
        icon: "🔌"
    },
    {
        id: 24,
        name: "BTS7960 Motor Driver",
        category: "Drivers",
        description: "High-current motor driver module.",
        price: 450,
        stock: 20,
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
        stock: 20,
        icon: "🔋"
    },
    {
        id: 26,
        name: "4-Channel Relay Module",
        category: "Modules",
        description: "Control four separate electrical circuits.",
        price: 180,
        stock: 20,
        icon: "🔌"
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
        stock: 20,
        icon: "🚗"
    },
    {
        id: 28,
        name: "Robot Car Chassis",
        category: "Accessories",
        description: "Chassis platform for DIY robot cars.",
        price: 250,
        stock: 20,
        icon: "🚙"
    },
    {
        id: 29,
        name: "Jumper Wire Set",
        category: "Accessories",
        description: "Male-to-male, male-to-female and female-to-female wires.",
        price: 100,
        stock: 20,
        icon: "🔗"
    },
    {
        id: 30,
        name: "Breadboard",
        category: "Accessories",
        description: "Reusable solderless prototyping board.",
        price: 90,
        stock: 20,
        icon: "🧱"
    },
    {
        id: 31,
        name: "Battery Holder",
        category: "Accessories",
        description: "Battery holder for powering robotics projects.",
        price: 60,
        stock: 20,
        icon: "🔋"
    },
    {
        id: 32,
        name: "Robot Wheel and Caster Set",
        category: "Accessories",
        description: "Wheels and caster for mobile robot platforms.",
        price: 180,
        stock: 20,
        icon: "🛞"
    },
    
    // ======================================
    // Bluetooth
    // ======================================

    {
        id: 27,
        name: "HC-05 Bluetooth Module",
        category: "Bluetooth",
        description: "Bluetooth serial communication for Arduino.",
        price: 250,
        stock: 20,
        icon: "📶"
    },


];
