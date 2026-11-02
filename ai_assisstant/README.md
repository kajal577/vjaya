# MUSKAN AI — PC Voice Assistant

A Python-based desktop voice assistant that can answer questions using Groq AI, recognize spoken commands, speak responses, manage personal memory, open Windows applications, and control supported ESP32 devices through HiveMQ MQTT.

## Features

- Voice input through a microphone
- Spoken responses using text-to-speech
- AI answers through the Groq API
- Personal memory: remember, recall, and forget facts
- Windows application controls
- ESP32 LED, fan, and gate commands through MQTT

## Requirements

- Windows 10 or Windows 11
- Python 3.11 recommended
- Internet connection
- Microphone and speakers
- Groq API key
- HiveMQ credentials (optional, for ESP32 control)

## Installation

1. Install Python 3.11.
2. Open a terminal inside this project folder.
3. Install the required packages:

```bash
py -3.11 -m pip install -r requirements.txt
```

4. Copy `.env.example` and rename the copy to `.env`.
5. Add your own Groq API key and, if needed, HiveMQ credentials to `.env`.
6. Save the file.

**Never publish your real `.env` file or API keys.**

## Run MUSKAN

```bash
py -3.11 main1.py
```

## Example voice commands

- Hey MUSKAN, open Notepad.
- Open Calculator.
- Remember that my favorite color is blue.
- What do you remember?
- LED ON.
- FAN1 ON.
- GATE OPEN.
- Goodbye.

## Important notes

- Groq AI and Google speech recognition require internet access.
- HiveMQ credentials are needed for ESP32 device control.
- ESP32 firmware and hardware are not included in this Python folder.
- The `memory.json` file is created when personal memory is saved.
- Allow microphone access in Windows privacy settings.

## Project files

- `main1.py` — Main assistant application
- `config.py` — Configuration settings
- `ai_client.py` — Groq AI connection
- `voice.py` — Speech recognition and voice output
- `memory_store.py` — Personal memory
- `pc_control.py` — Windows application controls
- `mqtt_control.py` — ESP32 MQTT communication
- `requirements.txt` — Python dependencies
- `.env.example` — Configuration template
