
from voice import listen, speak
from ai_client import ask_ai
from pc_control import handle_pc_command
from memory_store import remember, recall, forget
from mqtt_control import connect_mqtt, send_device_command, disconnect_mqtt


DEVICE_COMMANDS = {
    "led on": "LED ON",
    "turn led on": "LED ON",
    "led off": "LED OFF",
    "turn led off": "LED OFF",
    "fan on": "FAN ON",
    "fan off": "FAN OFF",
    "fan one on": "FAN1 ON",
    "fan one off": "FAN1 OFF",
    "fan two on": "FAN2 ON",
    "fan two off": "FAN2 OFF",
    "gate open": "GATE OPEN",
    "gate close": "GATE CLOSE",
}


def speak_response(response):
    """Print and speak a response safely."""
    if response is None:
        response = "Sorry, I could not generate an answer."

    response = str(response).strip()

    if not response:
        response = "Sorry, I received an empty answer."

       
        speak(response)
    


def handle_command(text):
    command = text.lower().strip()

    if command.startswith("hey muskan"):
        command = command[len("hey muskan"):].strip(" ,.!")

    # Exit
    if command in ("exit", "quit", "goodbye", "stop listening"):
        speak("Goodbye. MUSKAN is shutting down.")
        return False

    # Help
    if command in ("help", "what can you do"):
        speak_response(
            "I can answer questions, remember facts, open apps, "
            "and control your ESP32."
        )
        return True

    # Remember a fact
    if command.startswith("remember that "):
        fact = command[len("remember that "):]

        if " is " in fact:
            key, value = fact.split(" is ", 1)
            speak_response(remember(key, value))
        else:
            speak_response(
                "Say: remember that my favorite color is blue."
            )

        return True

    # Recall all memories
    if command in ("what do you remember", "show my memory"):
        speak_response(recall())
        return True

    # Forget a fact
    if command.startswith("forget "):
        speak_response(forget(command[len("forget "):]))
        return True

    # Recall a specific fact
    if command.startswith("what do you know about "):
        topic = command[len("what do you know about "):]
        speak_response(recall(topic))
        return True

    # PC commands
    result = handle_pc_command(command)

    if result is not None:
        speak_response(result)
        return True

    # ESP32 / MQTT commands
    if command in DEVICE_COMMANDS:
        result = send_device_command(DEVICE_COMMANDS[command])
        speak(result)
        return True

    # AI question: always pass the generated answer to speak()
          # AI question: generate, print, and speak the answer
    print("MUSKAN AI: Generating answer...", flush=True)

    try:
        answer = ask_ai(text)

        if answer and str(answer).strip():
            speak(answer)
        else:
            speak("Sorry, I could not generate an answer.")

    except Exception as error:
        print("AI ERROR:", error, flush=True)
        speak("Sorry, I could not answer that question.")

    return True

    

def main():
    speak_response(
        "Hello. I am MUSKAN, your personal voice assistant."
    )

    try:
        connect_mqtt()
    except Exception as error:
        print("MQTT CONNECTION ERROR:", error, flush=True)
        speak_response(
            "I could not connect to the device control service, "
            "but I will continue running."
        )

    speak_response(
        "I am ready. Ask me anything, or say exit when you want to stop."
    )

    try:
        while True:
            text = listen()

            if text:
                print("YOU:", text, flush=True)

                if not handle_command(text):
                    break

    except KeyboardInterrupt:
        speak_response("Stopping MUSKAN.")

    except Exception as error:
        print("ASSISTANT ERROR:", error, flush=True)

    finally:
        try:
            disconnect_mqtt()
        except Exception as error:
            print("MQTT DISCONNECT ERROR:", error, flush=True)

        print("MUSKAN stopped.", flush=True)


if __name__ == "__main__":
    main()
