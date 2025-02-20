#!/usr/bin/env bash

echo "Building latex tables..."
python3 build.py

if [ $? -eq 0 ]; then
    echo "Tables built executed successfully!"
else
    echo "Tables bui;d failed!"
    exit 1
fi

# Step 2: Run Makefile
echo "Running Makefile..."
make

if [ $? -eq 0 ]; then
    echo "Makefile executed successfully!"
else
    echo "Makefile execution failed!"
    exit 1
fi
