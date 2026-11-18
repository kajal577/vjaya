
// ==========================================
// VJAYA ROBOTICS - TRUSTED PRODUCT CATALOGUE
// Backend prices are authoritative for payments.
// Shipping weights and dimensions are estimates.
// Weight is in grams; dimensions are in centimetres.
// ==========================================

const products = [
    { id: 1, name: "ESP32 Development Board", price: 450, stock: 20, weightGrams: 50, lengthCm: 10, breadthCm: 8, heightCm: 3 },
    { id: 2, name: "Arduino UNO Compatible", price: 550, stock: 20, weightGrams: 70, lengthCm: 12, breadthCm: 9, heightCm: 4 },
    { id: 3, name: "Ultrasonic Sensor HC-SR04", price: 120, stock: 20, weightGrams: 20, lengthCm: 8, breadthCm: 5, heightCm: 3 },
    { id: 4, name: "SG90 Servo Motor", price: 150, stock: 20, weightGrams: 15, lengthCm: 5, breadthCm: 4, heightCm: 3 },
    { id: 5, name: "L298N Motor Driver", price: 180, stock: 20, weightGrams: 45, lengthCm: 8, breadthCm: 6, heightCm: 4 },
    { id: 6, name: "Robot Car Starter Kit", price: 999, stock: 20, weightGrams: 700, lengthCm: 25, breadthCm: 20, heightCm: 10 },
    { id: 7, name: "Arduino Nano", price: 250, stock: 20, weightGrams: 15, lengthCm: 8, breadthCm: 5, heightCm: 2 },
    { id: 8, name: "Arduino Mega 2560", price: 850, stock: 20, weightGrams: 70, lengthCm: 12, breadthCm: 10, heightCm: 4 },
    { id: 9, name: "ESP32-CAM", price: 650, stock: 20, weightGrams: 25, lengthCm: 8, breadthCm: 6, heightCm: 3 },
    { id: 10, name: "Raspberry Pi Pico", price: 400, stock: 20, weightGrams: 15, lengthCm: 8, breadthCm: 5, heightCm: 2 },
    { id: 11, name: "NodeMCU ESP8266", price: 300, stock: 20, weightGrams: 20, lengthCm: 8, breadthCm: 5, heightCm: 3 },
    { id: 12, name: "IR Sensor Module", price: 60, stock: 20, weightGrams: 10, lengthCm: 6, breadthCm: 4, heightCm: 2 },
    { id: 13, name: "PIR Motion Sensor", price: 100, stock: 20, weightGrams: 20, lengthCm: 8, breadthCm: 6, heightCm: 4 },
    { id: 14, name: "DHT11 Temperature Sensor", price: 90, stock: 20, weightGrams: 10, lengthCm: 6, breadthCm: 4, heightCm: 2 },
    { id: 15, name: "Soil Moisture Sensor", price: 70, stock: 20, weightGrams: 15, lengthCm: 8, breadthCm: 4, heightCm: 2 },
    { id: 16, name: "MPU6050 Gyroscope", price: 180, stock: 20, weightGrams: 10, lengthCm: 6, breadthCm: 4, heightCm: 2 },
    { id: 17, name: "MQ-2 Gas Sensor", price: 130, stock: 20, weightGrams: 25, lengthCm: 8, breadthCm: 6, heightCm: 4 },
    { id: 18, name: "DC Gear Motor", price: 180, stock: 20, weightGrams: 100, lengthCm: 10, breadthCm: 7, heightCm: 5 },
    { id: 19, name: "BO Motor", price: 100, stock: 20, weightGrams: 80, lengthCm: 10, breadthCm: 7, heightCm: 5 },
    { id: 20, name: "NEMA 17 Stepper Motor", price: 850, stock: 20, weightGrams: 350, lengthCm: 10, breadthCm: 10, heightCm: 8 },
    { id: 21, name: "MG996R Servo Motor", price: 350, stock: 20, weightGrams: 65, lengthCm: 7, breadthCm: 5, heightCm: 4 },
    { id: 22, name: "28BYJ-48 Stepper Motor", price: 120, stock: 20, weightGrams: 60, lengthCm: 8, breadthCm: 5, heightCm: 4 },
    { id: 23, name: "L293D Motor Driver", price: 100, stock: 20, weightGrams: 15, lengthCm: 6, breadthCm: 4, heightCm: 2 },
    { id: 24, name: "BTS7960 Motor Driver", price: 450, stock: 20, weightGrams: 150, lengthCm: 10, breadthCm: 8, heightCm: 5 },
    { id: 25, name: "1-Channel Relay Module", price: 80, stock: 20, weightGrams: 25, lengthCm: 7, breadthCm: 5, heightCm: 3 },
    { id: 26, name: "4-Channel Relay Module", price: 180, stock: 20, weightGrams: 60, lengthCm: 10, breadthCm: 7, heightCm: 4 },
    { id: 27, name: "HC-05 Bluetooth Module", price: 250, stock: 20, weightGrams: 15, lengthCm: 6, breadthCm: 4, heightCm: 2 },
    { id: 28, name: "Robot Car Chassis", price: 250, stock: 20, weightGrams: 250, lengthCm: 25, breadthCm: 18, heightCm: 5 },
    { id: 29, name: "Jumper Wire Set", price: 100, stock: 20, weightGrams: 50, lengthCm: 12, breadthCm: 8, heightCm: 3 },
    { id: 30, name: "Breadboard", price: 90, stock: 20, weightGrams: 60, lengthCm: 17, breadthCm: 10, heightCm: 2 },
    { id: 31, name: "Battery Holder", price: 60, stock: 20, weightGrams: 20, lengthCm: 8, breadthCm: 5, heightCm: 3 },
    { id: 32, name: "Robot Wheel and Caster Set", price: 180, stock: 20, weightGrams: 120, lengthCm: 12, breadthCm: 10, heightCm: 5 }
];

module.exports = products;
