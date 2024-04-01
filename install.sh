#!/bin/sh

# Update package lists
apt-get update

# Install system-level dependencies
apt-get install -y python3-tk espeak python3.10 python3-pip 

# Install Python packages using pip3
pip3 install yfinance numpy TA-Lib plotext pytz 

echo "Dependencies installation complete."
