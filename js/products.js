
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
    {
        id: 27,
        name: "HC-05 Bluetooth Module",
        category: "Modules",
        description: "Bluetooth serial communication for Arduino.",
        price: 250,
        stock: 20,
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
    }

];


// ==========================================
// PRODUCT IMAGE PATHS
// Place the matching image files in images/products/
// ==========================================

const productImages = {
    1: "images/products/esp32-development-board.jpg",
    2: "images/products/arduino-uno.jpg",
    3: "images/products/ultrasonic-hc-sr04.jpg",
    4: "images/products/sg90-servo.jpg",
    5: "images/products/l298n-motor-driver.jpg",
    6: "images/products/robot-car-starter-kit.jpg",
    7: "images/products/arduino-nano.jpg",
    8: "images/products/arduino-mega-2560.jpg",
    9: "images/products/esp32-cam.jpg",
    10: "images/products/raspberry-pi-pico.jpg",
    11: "images/products/nodemcu-esp8266.jpg",
    12: "images/products/ir-sensor.jpg",
    13: "images/products/pir-motion-sensor.jpg",
    14: "images/products/dht11-sensor.jpg",
    15: "images/products/soil-moisture-sensor.jpg",
    16: "images/products/mpu6050-gyroscope.jpg",
    17: "images/products/mq2-gas-sensor.jpg",
    18: "images/products/dc-gear-motor.jpg",
    19: "images/products/bo-motor.jpg",
    20: "images/products/nema17-stepper-motor.jpg",
    21: "images/products/mg996r-servo.jpg",
    22: "images/products/28byj48-stepper-motor.jpg",
    23: "images/products/l293d-motor-driver.jpg",
    24: "images/products/bts7960-motor-driver.jpg",
    25: "images/products/1-channel-relay.jpg",
    26: "images/products/4-channel-relay.jpg",
    27: "images/products/hc05-bluetooth-module.jpg",
    28: "images/products/robot-car-chassis.jpg",
    29: "images/products/jumper-wire-set.jpg",
    30: "images/products/breadboard.jpg",
    31: "images/products/battery-holder.jpg",
    32: "images/products/robot-wheel-caster-set.jpg"
};

products.forEach(product => {
    product.image = productImages[product.id] || "";
});

