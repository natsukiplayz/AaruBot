from threading import Thread
import subprocess

# Start Flask Ludo server
def run_web():
    subprocess.run(["python", "web_server.py"])

Thread(target=run_web, daemon=True).start()

# Start Telegram bot
subprocess.run(["python", "Aru.py"])