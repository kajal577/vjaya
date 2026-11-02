
import subprocess
import webbrowser

def handle_pc_command(command):
    cmd = " ".join(command.lower().strip().split())

    if cmd in ("open notepad", "start notepad"):
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."

    if cmd in ("open calculator", "open calc", "start calculator"):
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."

    if cmd in ("open browser", "open google", "open web browser"):
        webbrowser.open("https://www.google.com")
        return "Opening your browser."

    if cmd in ("open youtube", "play youtube"):
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if cmd in ("open file explorer", "open explorer"):
        subprocess.Popen(["explorer.exe"])
        return "Opening File Explorer."

    if cmd in ("lock computer", "lock my pc"):
        subprocess.Popen([
            "rundll32.exe", "user32.dll,LockWorkStation"
        ])
        return "Locking your computer."

    return None
