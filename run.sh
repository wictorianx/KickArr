#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

echo "[*] Starting KickArr Scheduler..."
python3 main.py &
SCHEDULER_PID=$!

echo "[*] Starting KickArr Web Dashboard..."
python3 -m app.web &
WEB_PID=$!

echo "[+] KickArr is running."
echo "    - Dashboard: http://localhost:5000"
echo "    - Press Ctrl+C to stop."

# Trap SIGINT (Ctrl+C) and kill both processes
trap "kill $SCHEDULER_PID $WEB_PID; exit" SIGINT SIGTERM

wait