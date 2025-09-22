#!/bin/bash

PROJECT_DIR="/home/$(whoami)/projects/pipeline-spotify"
cd "$PROJECT_DIR" || exit 1

export PYTHONPATH="$PYTHON_DIR:$PYTHONPATH"

mkdir -p logs

echo "$(date): Starting ETL pipeline..." >> logs/cron.log
if python3 main.py; then
    echo "$(date): ETL pipeline finished successfully" >> logs/cron.log
else
    echo "$(date): ETL pipeline failed with exit code $?" >> logs/cron.log
fi