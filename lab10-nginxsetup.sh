#!/bin/bash
# Lab 10: Configuring NGINX with proxy_pass
# Demonstrates NGINX configuration and reverse proxy setup

echo "=== Lab 10: Configuring NGINX with proxy_pass ==="
echo ""

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Note: NGINX installation and configuration requires root/sudo privileges"
    echo "Running in demonstration mode..."
    echo ""
fi

echo "========================================"
echo "Step 1: Installing NGINX"
echo "========================================"
echo ""
echo "Commands to install NGINX:"
echo "  sudo apt update"
echo "  sudo apt install nginx"
echo ""

if [ "$EUID" -eq 0 ]; then
    if ! command -v nginx &> /dev/null; then
        read -p "NGINX is not installed. Install it now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            apt-get update -qq
            apt-get install -y nginx
            echo "✓ NGINX installed"
        fi
    else
        echo "✓ NGINX is already installed"
        nginx -v
    fi
else
    if command -v nginx &> /dev/null; then
        echo "✓ NGINX is installed"
        nginx -v
    else
        echo "NGINX is not installed. Run: sudo apt install nginx"
    fi
fi

echo ""
echo "========================================"
echo "Step 2: Understanding NGINX Configuration Structure"
echo "========================================"
echo ""
echo "NGINX configuration files:"
echo "  Main config: /etc/nginx/nginx.conf"
echo "  Available sites: /etc/nginx/sites-available/"
echo "  Enabled sites: /etc/nginx/sites-enabled/"
echo ""
echo "Best practice:"
echo "  1. Create config in /etc/nginx/sites-available/"
echo "  2. Create symbolic link in /etc/nginx/sites-enabled/"
echo "  3. Test configuration: sudo nginx -t"
echo "  4. Reload NGINX: sudo systemctl reload nginx"
echo ""

echo "========================================"
echo "Step 3: Creating Basic Site Configuration"
echo "========================================"
echo ""
echo "Example configuration for static site (port 8000):"
echo ""
cat << 'EOF'
server {
    listen 8000;
    server_name localhost;
    root /var/www/html;
    index my_site.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF
echo ""

echo "========================================"
echo "Step 4: NGINX proxy_pass Configuration"
echo "========================================"
echo ""
echo "The proxy_pass directive forwards requests to a backend server:"
echo ""
cat << 'EOF'
server {
    listen 8080;
    server_name localhost;

    location / {
        # Forward all requests to backend API on port 5000
        proxy_pass http://127.0.0.1:5000;
        
        # Pass important headers to backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
echo ""

echo "Key proxy_pass parameters:"
echo "  proxy_pass http://backend_server:port  - Forward requests to backend"
echo "  proxy_set_header                        - Pass headers to backend"
echo "  proxy_connect_timeout                   - Connection timeout"
echo "  proxy_read_timeout                      - Read timeout"
echo ""

echo "========================================"
echo "Step 5: Setting Up API Server"
echo "========================================"
echo ""
echo "To test proxy_pass, you need a backend API server."
echo "A sample Flask API server is provided: api_server.py"
echo ""
echo "To start the API server:"
echo "  1. Install Flask: pip install flask flask-cors"
echo "  2. Run: python api_server.py"
echo "  3. Server will run on http://127.0.0.1:5000"
echo ""

echo "========================================"
echo "Step 6: Complete Setup Process"
echo "========================================"
echo ""
echo "1. Create configuration file:"
echo "   sudo nano /etc/nginx/sites-available/api_proxy"
echo ""
echo "2. Copy the proxy configuration (see nginx_proxy_config.conf)"
echo ""
echo "3. Create symbolic link:"
echo "   sudo ln -s /etc/nginx/sites-available/api_proxy /etc/nginx/sites-enabled/"
echo ""
echo "4. Remove default site (optional):"
echo "   sudo rm /etc/nginx/sites-enabled/default"
echo ""
echo "5. Test configuration:"
echo "   sudo nginx -t"
echo ""
echo "6. Reload NGINX:"
echo "   sudo systemctl reload nginx"
echo ""
echo "7. Start API server:"
echo "   python api_server.py"
echo ""
echo "8. Test the proxy:"
echo "   curl http://localhost:8080/api/info"
echo "   curl http://localhost:8080/api/data"
echo ""

if [ "$EUID" -eq 0 ]; then
    echo "========================================"
    echo "Interactive Setup"
    echo "========================================"
    echo ""
    read -p "Do you want to set up the NGINX proxy configuration now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        CONFIG_FILE="/etc/nginx/sites-available/api_proxy"
        
        if [ -f "nginx_proxy_config.conf" ]; then
            echo "Copying configuration file..."
            cp nginx_proxy_config.conf "$CONFIG_FILE"
            echo "✓ Configuration file created at $CONFIG_FILE"
        else
            echo "Creating configuration file..."
            cat > "$CONFIG_FILE" << 'NGINXEOF'
server {
    listen 8080;
    server_name localhost;

    access_log /var/log/nginx/api_access.log;
    error_log /var/log/nginx/api_error.log;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
NGINXEOF
            echo "✓ Configuration file created"
        fi
        
        # Create symbolic link
        if [ ! -L "/etc/nginx/sites-enabled/api_proxy" ]; then
            ln -s "$CONFIG_FILE" /etc/nginx/sites-enabled/api_proxy
            echo "✓ Symbolic link created"
        fi
        
        # Test configuration
        echo ""
        echo "Testing NGINX configuration..."
        if nginx -t; then
            echo "✓ Configuration is valid"
            echo ""
            read -p "Reload NGINX now? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                systemctl reload nginx
                echo "✓ NGINX reloaded"
                echo ""
                echo "NGINX proxy is now configured!"
                echo "Make sure to start your API server: python api_server.py"
                echo "Then test: curl http://localhost:8080/api/info"
            fi
        else
            echo "✗ Configuration has errors. Please fix them."
        fi
    fi
fi

echo ""
echo "========================================"
echo "Testing and Troubleshooting"
echo "========================================"
echo ""
echo "Check NGINX status:"
echo "  sudo systemctl status nginx"
echo ""
echo "Test configuration:"
echo "  sudo nginx -t"
echo ""
echo "View error logs:"
echo "  sudo tail -f /var/log/nginx/error.log"
echo ""
echo "View access logs:"
echo "  sudo tail -f /var/log/nginx/access.log"
echo ""
echo "Restart NGINX:"
echo "  sudo systemctl restart nginx"
echo ""
echo "Test API endpoints through proxy:"
echo "  curl http://localhost:8080/"
echo "  curl http://localhost:8080/api/data"
echo "  curl http://localhost:8080/api/info"
echo ""

echo "========================================"
echo "Common proxy_pass Use Cases"
echo "========================================"
echo ""
echo "1. Reverse Proxy: Forward requests to backend application servers"
echo "2. Load Balancing: Distribute traffic across multiple servers"
echo "3. SSL Termination: Handle HTTPS and forward to HTTP backend"
echo "4. API Gateway: Route API requests to different services"
echo "5. Caching: Cache responses from backend servers"
echo ""

echo "=== Lab 10 demonstration complete ==="

