#!/bin/bash

echo "Starting Frontend Development Server..."
cd frontend

if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

npm start

