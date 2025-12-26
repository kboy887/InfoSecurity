#!/bin/bash
# Lab 11: Install neofetch from source
# Practical example of installing software from GitHub repository

echo "=== Installing neofetch from Source ==="
echo ""

# Check for sudo
if [ "$EUID" -ne 0 ]; then 
    echo "This script requires sudo privileges"
    echo "Usage: sudo ./install_neofetch.sh"
    exit 1
fi

# Step 1: Update package list
echo "Step 1: Updating package repositories..."
apt-get update -qq
echo "✓ Package repositories updated"
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies (git, make)..."
apt-get install -y git make
echo "✓ Dependencies installed"
echo ""

# Step 3: Clone repository
echo "Step 3: Cloning neofetch repository from GitHub..."
if [ -d "neofetch" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd neofetch
    git pull
    cd ..
else
    git clone https://github.com/dylanaraps/neofetch.git
fi
echo "✓ Repository cloned"
echo ""

# Step 4: Navigate to directory
echo "Step 4: Navigating to neofetch directory..."
cd neofetch
echo "✓ Changed directory"
echo ""

# Step 5: Install neofetch
echo "Step 5: Installing neofetch using make..."
make install
INSTALL_STATUS=$?
cd ..
echo ""

if [ $INSTALL_STATUS -eq 0 ]; then
    echo "✓ Installation completed successfully"
    echo ""
    
    # Step 6: Verify installation
    echo "Step 6: Verifying installation..."
    if command -v neofetch &> /dev/null; then
        echo "✓ neofetch is installed and available"
        echo ""
        echo "You can now run: neofetch"
        echo ""
        echo "Would you like to run neofetch now? (y/n)"
        read -p "> " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            neofetch
        fi
    else
        echo "⚠ Installation may have completed, but neofetch command not found in PATH"
        echo "You may need to restart your terminal or update your PATH"
    fi
else
    echo "✗ Installation failed"
    exit 1
fi

echo ""
echo "=== Installation process complete ==="

