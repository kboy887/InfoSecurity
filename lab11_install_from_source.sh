#!/bin/bash
# Lab 11: Installing Packages from Source
# Demonstrates different methods of installing software from source code

echo "=== Lab 11: Installing Packages from Source ==="
echo ""

# Check if running as root/sudo for installations
if [ "$EUID" -ne 0 ]; then 
    echo "Note: Some installation steps require root/sudo privileges"
    echo "This script demonstrates the process - actual installations require sudo"
    echo ""
fi

echo "This script demonstrates different methods of installing software from source."
echo ""

# Method 1: Manual Compilation (Classic Method)
echo "========================================"
echo "Method 1: Manual Compilation (Classic)"
echo "========================================"
echo ""
echo "Steps:"
echo "1. Download source code"
echo "   wget https://example.com/software-1.0.tar.gz"
echo ""
echo "2. Extract source code"
echo "   tar -xvzf software-1.0.tar.gz"
echo ""
echo "3. Navigate to directory"
echo "   cd software-1.0"
echo ""
echo "4. Configure (if configure script exists)"
echo "   ./configure"
echo "   # or with options: ./configure --prefix=/usr/local"
echo ""
echo "5. Compile"
echo "   make"
echo ""
echo "6. Install (requires sudo)"
echo "   sudo make install"
echo ""
echo "========================================"
echo ""

# Method 2: CMake Build System
echo "========================================"
echo "Method 2: Installation Using CMake"
echo "========================================"
echo ""
echo "Steps:"
echo "1. Clone repository"
echo "   git clone https://github.com/example/example-software.git"
echo ""
echo "2. Navigate to directory"
echo "   cd example-software"
echo ""
echo "3. Create build directory"
echo "   mkdir build"
echo "   cd build"
echo ""
echo "4. Run cmake"
echo "   cmake .."
echo "   # or with options: cmake -DCMAKE_INSTALL_PREFIX=/usr/local .."
echo ""
echo "5. Compile"
echo "   make"
echo ""
echo "6. Install (requires sudo)"
echo "   sudo make install"
echo ""
echo "========================================"
echo ""

# Method 3: Git-based Installation
echo "========================================"
echo "Method 3: Installation Using Git"
echo "========================================"
echo ""
echo "Steps:"
echo "1. Clone repository"
echo "   git clone https://github.com/example/example-software.git"
echo ""
echo "2. Navigate to directory"
echo "   cd example-software"
echo ""
echo "3. Build and install"
echo "   make"
echo "   sudo make install"
echo ""
echo "========================================"
echo ""

# Method 4: Automated Installation Scripts
echo "========================================"
echo "Method 4: Automated Installation Scripts"
echo "========================================"
echo ""
echo "Steps:"
echo "1. Download installation script"
echo "   wget https://example.com/install.sh"
echo ""
echo "2. Make executable"
echo "   chmod +x install.sh"
echo ""
echo "3. Run script"
echo "   ./install.sh"
echo "   # or: sudo ./install.sh"
echo ""
echo "========================================"
echo ""

# Practical Example 1: youtube-dl
echo "========================================"
echo "Practical Example 1: Installing youtube-dl"
echo "========================================"
echo ""

if command -v youtube-dl &> /dev/null; then
    echo "youtube-dl is already installed:"
    youtube-dl --version
    echo ""
else
    echo "youtube-dl is not installed. Installation steps:"
    echo ""
    echo "1. Install dependencies:"
    echo "   sudo apt update"
    echo "   sudo apt install python3 python3-pip python3-setuptools"
    echo ""
    echo "2. Clone repository:"
    echo "   git clone https://github.com/ytdl-org/youtube-dl.git"
    echo ""
    echo "3. Navigate to directory:"
    echo "   cd youtube-dl"
    echo ""
    echo "4. Install:"
    echo "   sudo python3 setup.py install"
    echo ""
    echo "5. Verify:"
    echo "   youtube-dl --version"
    echo ""
    
    # Ask if user wants to install (for demonstration)
    read -p "Do you want to install youtube-dl now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] && [ "$EUID" -eq 0 ]; then
        echo "Installing youtube-dl..."
        # Check if dependencies are installed
        if ! command -v python3 &> /dev/null; then
            echo "Installing Python dependencies..."
            apt-get update -qq
            apt-get install -y python3 python3-pip python3-setuptools
        fi
        
        if [ ! -d "youtube-dl" ]; then
            git clone https://github.com/ytdl-org/youtube-dl.git
        fi
        
        cd youtube-dl
        python3 setup.py install
        cd ..
        
        if command -v youtube-dl &> /dev/null; then
            echo "✓ youtube-dl installed successfully!"
            youtube-dl --version
        fi
    elif [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Please run this script with sudo to install packages"
    fi
    echo ""
fi

echo "========================================"
echo ""

# Practical Example 2: neofetch
echo "========================================"
echo "Practical Example 2: Installing neofetch"
echo "========================================"
echo ""

if command -v neofetch &> /dev/null; then
    echo "neofetch is already installed:"
    neofetch --version 2>/dev/null || echo "neofetch is installed"
    echo ""
else
    echo "neofetch is not installed. Installation steps:"
    echo ""
    echo "1. Install dependencies:"
    echo "   sudo apt update"
    echo "   sudo apt install git make"
    echo ""
    echo "2. Clone repository:"
    echo "   git clone https://github.com/dylanaraps/neofetch.git"
    echo ""
    echo "3. Navigate to directory:"
    echo "   cd neofetch"
    echo ""
    echo "4. Install:"
    echo "   sudo make install"
    echo ""
    echo "5. Verify:"
    echo "   neofetch"
    echo ""
    
    # Ask if user wants to install (for demonstration)
    read -p "Do you want to install neofetch now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] && [ "$EUID" -eq 0 ]; then
        echo "Installing neofetch..."
        # Check if dependencies are installed
        if ! command -v git &> /dev/null || ! command -v make &> /dev/null; then
            echo "Installing dependencies..."
            apt-get update -qq
            apt-get install -y git make
        fi
        
        if [ ! -d "neofetch" ]; then
            git clone https://github.com/dylanaraps/neofetch.git
        fi
        
        cd neofetch
        make install
        cd ..
        
        if command -v neofetch &> /dev/null; then
            echo "✓ neofetch installed successfully!"
        fi
    elif [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Please run this script with sudo to install packages"
    fi
    echo ""
fi

echo "========================================"
echo ""

# Additional Examples - Suggesting simple utilities
echo "========================================"
echo "Suggested Simple Utilities to Install"
echo "========================================"
echo ""
echo "1. bat (cat clone with syntax highlighting):"
echo "   git clone https://github.com/sharkdp/bat.git"
echo "   cd bat"
echo "   cargo build --release  # Requires Rust"
echo ""
echo "2. exa (modern ls replacement):"
echo "   git clone https://github.com/ogham/exa.git"
echo "   cd exa"
echo "   make install"
echo ""
echo "3. fd (find replacement):"
echo "   git clone https://github.com/sharkdp/fd.git"
echo "   cd fd"
echo "   cargo build --release  # Requires Rust"
echo ""
echo "4. ripgrep (grep replacement):"
echo "   git clone https://github.com/BurntSushi/ripgrep.git"
echo "   cd ripgrep"
echo "   cargo build --release  # Requires Rust"
echo ""
echo "5. htop (interactive process viewer):"
echo "   wget https://github.com/htop-dev/htop/releases/download/3.x.x/htop-3.x.x.tar.xz"
echo "   tar -xf htop-3.x.x.tar.xz"
echo "   cd htop-3.x.x"
echo "   ./configure"
echo "   make"
echo "   sudo make install"
echo ""
echo "========================================"
echo ""

# Common commands reference
echo "========================================"
echo "Common Commands Reference"
echo "========================================"
echo ""
echo "Extracting archives:"
echo "  tar -xvzf file.tar.gz     # Extract .tar.gz"
echo "  tar -xvjf file.tar.bz2    # Extract .tar.bz2"
echo "  tar -xvf file.tar         # Extract .tar"
echo "  unzip file.zip            # Extract .zip"
echo ""
echo "Configuration options (common):"
echo "  --prefix=/usr/local        # Installation directory"
echo "  --enable-feature           # Enable a feature"
echo "  --disable-feature          # Disable a feature"
echo "  --with-library=/path       # Specify library path"
echo ""
echo "Build commands:"
echo "  make                       # Compile"
echo "  make install               # Install (requires sudo)"
echo "  make clean                 # Clean build files"
echo "  make uninstall             # Remove installation"
echo ""
echo "CMake commands:"
echo "  cmake ..                   # Configure"
echo "  cmake --build .            # Build"
echo "  cmake --install .          # Install"
echo ""
echo "========================================"
echo ""

# Cleanup option
echo "Cleanup downloaded repositories? (y/n)"
read -p "This will remove youtube-dl/ and neofetch/ directories: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "youtube-dl" ]; then
        rm -rf youtube-dl
        echo "Removed youtube-dl directory"
    fi
    if [ -d "neofetch" ]; then
        rm -rf neofetch
        echo "Removed neofetch directory"
    fi
fi

echo ""
echo "=== Lab 11 demonstration complete ==="
echo ""
echo "Key Takeaways:"
echo "- Installing from source gives you access to latest versions"
echo "- Allows customization and optimization"
echo "- Common methods: configure/make, cmake, git clone, install scripts"
echo "- Always check README.md or INSTALL files for specific instructions"
echo "- Most installations require root/sudo privileges"
