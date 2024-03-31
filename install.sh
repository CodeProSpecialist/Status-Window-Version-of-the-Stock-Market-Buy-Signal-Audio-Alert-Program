#!/bin/bash

# Update package lists
apt-get update

# Install system-level dependencies
apt-get install -y python3-tk espeak

# Install Python packages using pip3
pip3 install yfinance numpy TA-Lib plotext

echo "Dependencies installation complete."
