
# Sign Language Translator
## Raspberry Pi 5 Project

This project recognizes custom static hand gestures using a webcam
and converts recognized labels into text and speech.

## Hardware

- Raspberry Pi 5
- USB webcam
- USB speaker or audio output
- MicroSD card
- Raspberry Pi power supply

## Software

- Python
- OpenCV
- MediaPipe
- Scikit-learn
- pyttsx3

## Installation

Open a terminal inside the project folder.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the libraries:

```bash
pip install -r requirements.txt
```

If speech output needs eSpeak:

```bash
sudo apt update
sudo apt install espeak
```

## Collect hand-sign data

Run:

```bash
python collect_data.py
```

Enter a label, for example:

HELLO

Show the hand sign to the camera.

Press SPACE to save a sample.

Press Q to finish collecting that label.

Repeat for other labels, such as:

- HELLO
- YES
- NO
- THANK_YOU

Collect many samples for each sign, preferably 50 to 200 or more,
with different hand positions and lighting.

## Train the AI model

Run:

```bash
python train_model.py
```

The trained model will be saved in:

models/gesture_model.joblib

## Start the translator

Run:

```bash
python main.py
```

The camera window will show the recognized sign.

Press Q to quit.

Press S to speak the current recognized sign again.

## Important

This starter project recognizes static gestures that you collect
and label yourself.

It is not yet a complete Indian Sign Language translator.
Full sign-language translation requires movement, facial
expressions, body position, and language grammar.
