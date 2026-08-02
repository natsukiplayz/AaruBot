import subprocess

# Start Telegram bot.
# Aru.py already runs its own Flask keep-alive server internally
# (see keep_alive() in Aru.py), so there's no need for a separate
# web_server.py process here anymore -- that was only for the Ludo
# WebSocket relay, which has been removed.
subprocess.run(["python", "Aru.py"])
