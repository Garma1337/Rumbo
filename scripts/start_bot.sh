#!/usr/bin/env bash

CURRENT_DIRECTORY=$(dirname "$0")
VENV_BIN="${CURRENT_DIRECTORY}/../venv/bin/activate"
BOT_BIN="${CURRENT_DIRECTORY}/../bot.py"

source "$VENV_BIN"
python3 -B "$BOT_BIN"
