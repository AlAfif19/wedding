#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT_DIR/.server.pid"
PORT="${PORT:-8000}"

port_pid() {
  netstat -ano 2>/dev/null | awk -v port=":$PORT" '$2 ~ port && $4 == "LISTENING" {print $5; exit}'
}

if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE")"
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID" 2>/dev/null || true
  fi
fi

sleep 1
ACTIVE_PID="$(port_pid || true)"
if [[ -n "$ACTIVE_PID" ]]; then
  taskkill //PID "$ACTIVE_PID" //F >/dev/null 2>&1 || cmd.exe /c "taskkill /PID $ACTIVE_PID /F" >/dev/null 2>&1 || true
fi

rm -f "$PID_FILE"

if [[ -n "$(port_pid || true)" ]]; then
  echo "Server is still running on port $PORT."
  exit 1
fi

echo "Stopped Aliya Wedding Organizer server."
