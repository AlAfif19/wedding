#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT_DIR/.server.pid"
LOG_FILE="$ROOT_DIR/.server.log"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

port_pid() {
  netstat -ano 2>/dev/null | awk -v port=":$PORT" '$2 ~ port && $4 == "LISTENING" {print $5; exit}'
}

ACTIVE_PID="$(port_pid || true)"
if [[ -n "$ACTIVE_PID" ]]; then
  echo "Aliya Wedding Organizer is already running at http://$HOST:$PORT"
  echo "$ACTIVE_PID" > "$PID_FILE"
  exit 0
fi

if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE")"
  if kill -0 "$PID" 2>/dev/null; then
    echo "Aliya Wedding Organizer is already running at http://$HOST:$PORT"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

cd "$ROOT_DIR"
python server.py --host "$HOST" --port "$PORT" >"$LOG_FILE" 2>&1 </dev/null &
echo "$!" > "$PID_FILE"

echo "Aliya Wedding Organizer running at http://$HOST:$PORT"
echo "Use ./stop.sh to stop the server."
