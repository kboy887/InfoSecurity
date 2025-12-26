#!/bin/bash
# Lab 11: Install youtube-dl from source
# Practical example of installing software from GitHub repository

echo "=== Installing youtube-dl from Source ==="
echo ""

# Check for sudo
if [ "$EUID" -ne 0 ]; then 
    echo "This script requires sudo privileges"
    echo "Usage: sudo ./install_youtube_dl.sh"
    exit 1
fi

# Step 1: Update package list
echo "Step 1: Updating package repositories..."
apt-get update -qq
echo "✓ Package repositories updated"
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies (python3, pip, setuptools)..."
apt-get install -y python3 python3-pip python3-setuptools
echo "✓ Dependencies installed"
echo ""

# Step 3: Clone repository
echo "Step 3: Cloning youtube-dl repository from GitHub..."
if [ -d "youtube-dl" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd youtube-dl
    git pull
    cd ..
else
    git clone https://github.com/ytdl-org/youtube-dl.git
fi
echo "✓ Repository cloned"
echo ""

# Step 4: Navigate to directory
echo "Step 4: Navigating to youtube-dl directory..."
cd youtube-dl
echo "✓ Changed directory"
echo ""

# Step 5: Install youtube-dl
echo "Step 5: Installing youtube-dl using setup.py..."
python3 setup.py install
INSTALL_STATUS=$?
cd ..
echo ""

if [ $INSTALL_STATUS -eq 0 ]; then
    echo "✓ Installation completed successfully"
    echo ""
    
    # Step 6: Verify installation
    echo "Step 6: Verifying installation..."
    if command -v youtube-dl &> /dev/null; then
        echo "✓ youtube-dl is installed and available"
        echo ""
        echo "Version:"
        youtube-dl --version
        echo ""
        echo "Usage example:"
        echo "  youtube-dl <video-url>"
        echo ""
    else
        echo "⚠ Installation may have completed, but youtube-dl command not found in PATH"
        echo "You may need to restart your terminal or update your PATH"
    fi
else
    echo "✗ Installation failed"
    exit 1
fi

echo ""
echo "=== Installation process complete ==="

