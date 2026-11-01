// Define relay pins
const int LIGHT_RELAY = 7; // Relay 1 controls the light
const int FAN_RELAY = 8;   // Relay 2 controls the fan

String command = ""; // String variable to hold incoming voice commands

void setup() {
  // Initialize hardware serial communication at 9600 baud rate
  Serial.begin(9600);
  
  // Set relay pins as OUTPUTs
  pinMode(LIGHT_RELAY, OUTPUT);
  pinMode(FAN_RELAY, OUTPUT);
  
  // Turn relays OFF initially 
  // (Change to HIGH if your relay module is Active-Low)
  digitalWrite(LIGHT_RELAY, HIGH); 
  digitalWrite(FAN_RELAY, HIGH);
  
  Serial.println("System Ready. Send voice commands.");
}

void loop() {
  // Read incoming serial data string until a newline character
  while (Serial.available() > 0) {
    char c = Serial.read();
    
    // Ignore newline or carriage return characters
    if (c == '\n' || c == '\r') {
      continue; 
    }
    
    command += c; // Build the command string character by character
    delay(2);     // Short delay for stability
  }

  // If a command has been received
  if (command.length() > 0) {
    command.toLowerCase(); // Convert to lowercase to avoid case-sensitivity issues
    command.trim();        // Remove any accidental trailing spaces
    
    Serial.print("Received Command: ");
    Serial.println(command);

    // --- Light Control Logic ---
    if (command == "light off" || command == "turn off light") {
      digitalWrite(LIGHT_RELAY, HIGH); // Turn Light ON
      Serial.println("Status: Light is ON");
    } 
    else if (command == "light on" || command == "turn on light") {
      digitalWrite(LIGHT_RELAY, LOW);  // Turn Light OFF
      Serial.println("Status: Light is OFF");
    }
    
    // --- Fan Control Logic ---
    else if (command == "fan off" || command == "turn off fan") {
      digitalWrite(FAN_RELAY, HIGH);   // Turn Fan ON
      Serial.println("Status: Fan is ON");
    } 
    else if (command == "fan on" || command == "turn on fan") {
      digitalWrite(FAN_RELAY, LOW);    // Turn Fan OFF
      Serial.println("Status: Fan is OFF");
    }

    command = ""; // Clear the string variable for the next command
  }
}
