#!/bin/bash

echo "Starting Backend Server..."
cd backend

if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

python server.py

