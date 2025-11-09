#!/bin/bash

###############################################################################
# n8n Blog Automation Setup Script for Ubuntu
# This script installs all prerequisites for running the blog automation
###############################################################################

set -e  # Exit on error

echo "🚀 Starting n8n Blog Automation Setup..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Please do not run this script as root${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Running as non-root user"

###############################################################################
# 1. Update System
###############################################################################
echo ""
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

###############################################################################
# 2. Install Node.js & npm
###############################################################################
echo ""
echo "📦 Installing Node.js 20.x..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    echo -e "${GREEN}✓${NC} Node.js installed: $(node --version)"
else
    echo -e "${GREEN}✓${NC} Node.js already installed: $(node --version)"
fi

###############################################################################
# 3. Install n8n
###############################################################################
echo ""
echo "📦 Installing n8n..."
if ! command -v n8n &> /dev/null; then
    sudo npm install -g n8n
    echo -e "${GREEN}✓${NC} n8n installed: $(n8n --version)"
else
    echo -e "${GREEN}✓${NC} n8n already installed: $(n8n --version)"
fi

###############################################################################
# 4. Install PM2 (Process Manager)
###############################################################################
echo ""
echo "📦 Installing PM2..."
if ! command -v pm2 &> /dev/null; then
    sudo npm install -g pm2
    echo -e "${GREEN}✓${NC} PM2 installed: $(pm2 --version)"
else
    echo -e "${GREEN}✓${NC} PM2 already installed: $(pm2 --version)"
fi

###############################################################################
# 5. Install Git
###############################################################################
echo ""
echo "📦 Installing Git..."
if ! command -v git &> /dev/null; then
    sudo apt-get install -y git
    echo -e "${GREEN}✓${NC} Git installed: $(git --version)"
else
    echo -e "${GREEN}✓${NC} Git already installed: $(git --version)"
fi

###############################################################################
# 6. Install Python 3 & pip (for Python script)
###############################################################################
echo ""
echo "📦 Installing Python 3..."
if ! command -v python3 &> /dev/null; then
    sudo apt-get install -y python3 python3-pip
    echo -e "${GREEN}✓${NC} Python installed: $(python3 --version)"
else
    echo -e "${GREEN}✓${NC} Python already installed: $(python3 --version)"
fi

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install --user requests python-dotenv

###############################################################################
# 7. Install Hugo (Static Site Generator)
###############################################################################
echo ""
echo "📦 Installing Hugo..."
if ! command -v hugo &> /dev/null; then
    sudo snap install hugo
    echo -e "${GREEN}✓${NC} Hugo installed: $(hugo version)"
else
    echo -e "${GREEN}✓${NC} Hugo already installed: $(hugo version)"
fi

###############################################################################
# 8. Install Nginx (Optional - for reverse proxy)
###############################################################################
echo ""
read -p "Install Nginx for reverse proxy? (y/n): " install_nginx
if [ "$install_nginx" = "y" ]; then
    echo "📦 Installing Nginx..."
    sudo apt-get install -y nginx
    sudo systemctl enable nginx
    sudo systemctl start nginx
    echo -e "${GREEN}✓${NC} Nginx installed and started"
fi

###############################################################################
# 9. Create Directory Structure
###############################################################################
echo ""
echo "📁 Creating directory structure..."
mkdir -p ~/portfolio/content/blog
mkdir -p ~/portfolio/static/images/blog
mkdir -p ~/n8n-data
mkdir -p ~/.n8n

echo -e "${GREEN}✓${NC} Directories created"

###############################################################################
# 10. Configure n8n
###############################################################################
echo ""
echo "⚙️  Configuring n8n..."

# Create n8n config file
cat > ~/.n8n/config <<EOF
# n8n Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=change_this_password
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=http
EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true
EOF

echo -e "${YELLOW}⚠️  Default n8n credentials:${NC}"
echo "   Username: admin"
echo "   Password: change_this_password"
echo "   ${RED}CHANGE THESE IN ~/.n8n/config${NC}"

###############################################################################
# 11. Create Environment Variables Template
###############################################################################
echo ""
echo "📝 Creating environment variables template..."

cat > ~/.n8n/.env <<EOF
# API Keys (REQUIRED - Add your keys here)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
NEWSAPI_KEY=your_newsapi_key_here

# Optional API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Portfolio Paths
PORTFOLIO_PATH=$HOME/portfolio
BLOG_CONTENT_PATH=$HOME/portfolio/content/blog
BLOG_IMAGES_PATH=$HOME/portfolio/static/images/blog

# Git Configuration
GIT_USER_NAME="Your Name"
GIT_USER_EMAIL="your.email@example.com"

# Notification Settings
NOTIFICATION_EMAIL=your.email@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@example.com
SMTP_PASSWORD=your_app_password

# n8n Settings
N8N_WEBHOOK_URL=http://localhost:5678
EOF

echo -e "${YELLOW}⚠️  Environment variables template created at ~/.n8n/.env${NC}"
echo -e "${RED}   YOU MUST ADD YOUR API KEYS BEFORE RUNNING THE WORKFLOW${NC}"

###############################################################################
# 12. Create PM2 Ecosystem File
###############################################################################
echo ""
echo "📝 Creating PM2 ecosystem file..."

cat > ~/n8n-ecosystem.config.js <<EOF
module.exports = {
  apps: [
    {
      name: 'n8n',
      script: 'n8n',
      args: 'start',
      cwd: '$HOME',
      env: {
        N8N_BASIC_AUTH_ACTIVE: 'true',
        N8N_BASIC_AUTH_USER: 'admin',
        N8N_BASIC_AUTH_PASSWORD: 'change_this_password',
        N8N_HOST: '0.0.0.0',
        N8N_PORT: '5678'
      },
      error_file: '$HOME/.n8n/logs/err.log',
      out_file: '$HOME/.n8n/logs/out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s'
    }
  ]
};
EOF

mkdir -p ~/.n8n/logs
echo -e "${GREEN}✓${NC} PM2 ecosystem file created"

###############################################################################
# 13. Create Helper Scripts
###############################################################################
echo ""
echo "📝 Creating helper scripts..."

# Start n8n script
cat > ~/start-n8n.sh <<'EOF'
#!/bin/bash
echo "🚀 Starting n8n with PM2..."
pm2 start ~/n8n-ecosystem.config.js
pm2 save
pm2 startup
echo "✅ n8n started! Access at http://localhost:5678"
EOF
chmod +x ~/start-n8n.sh

# Stop n8n script
cat > ~/stop-n8n.sh <<'EOF'
#!/bin/bash
echo "🛑 Stopping n8n..."
pm2 stop n8n
echo "✅ n8n stopped"
EOF
chmod +x ~/stop-n8n.sh

# View logs script
cat > ~/n8n-logs.sh <<'EOF'
#!/bin/bash
pm2 logs n8n
EOF
chmod +x ~/n8n-logs.sh

echo -e "${GREEN}✓${NC} Helper scripts created:"
echo "   ~/start-n8n.sh - Start n8n"
echo "   ~/stop-n8n.sh - Stop n8n"
echo "   ~/n8n-logs.sh - View logs"

###############################################################################
# 14. Configure Git
###############################################################################
echo ""
read -p "Configure Git now? (y/n): " config_git
if [ "$config_git" = "y" ]; then
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    echo -e "${GREEN}✓${NC} Git configured"
fi

###############################################################################
# 15. Initialize Portfolio Repository
###############################################################################
echo ""
read -p "Initialize portfolio Git repository? (y/n): " init_repo
if [ "$init_repo" = "y" ]; then
    cd ~/portfolio
    if [ ! -d ".git" ]; then
        git init
        echo "# My Portfolio" > README.md
        git add README.md
        git commit -m "Initial commit"
        echo -e "${GREEN}✓${NC} Portfolio repository initialized"
        echo "   Add remote with: git remote add origin <your-repo-url>"
    else
        echo -e "${YELLOW}⚠️${NC}  Git repository already exists"
    fi
fi

###############################################################################
# 16. Install Node.js Dependencies for Scripts
###############################################################################
echo ""
echo "📦 Installing Node.js dependencies..."
cd ~/portfolio
npm init -y
npm install axios dotenv

echo -e "${GREEN}✓${NC} Node.js dependencies installed"

###############################################################################
# 17. Create Test Blog Post
###############################################################################
echo ""
echo "📝 Creating test blog post..."

cat > ~/portfolio/content/blog/test-post.md <<EOF
---
title: "Test Blog Post - Setup Successful"
date: $(date -I)
author: "System"
tags: ["test", "setup"]
summary: "This is a test post to verify the blog automation setup."
---

## Test Post

This post was created during the n8n blog automation setup.

If you can see this, your setup is working correctly!

### Next Steps

1. Configure your API keys in ~/.n8n/.env
2. Import the n8n workflow
3. Test the workflow manually
4. Enable the cron trigger

Happy blogging! 🎉
EOF

echo -e "${GREEN}✓${NC} Test blog post created at ~/portfolio/content/blog/test-post.md"

###############################################################################
# 18. Display Summary
###############################################################################
echo ""
echo "========================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "========================================"
echo ""
echo "📋 Summary:"
echo "  ✓ Node.js $(node --version)"
echo "  ✓ n8n $(n8n --version)"
echo "  ✓ PM2 $(pm2 --version)"
echo "  ✓ Git $(git --version)"
echo "  ✓ Python $(python3 --version)"
echo "  ✓ Hugo $(hugo version | head -n1)"
echo ""
echo "📁 Directories:"
echo "  - Portfolio: ~/portfolio"
echo "  - Blog content: ~/portfolio/content/blog"
echo "  - n8n data: ~/.n8n"
echo ""
echo "🔑 Next Steps:"
echo ""
echo "1. Add your API keys to ~/.n8n/.env:"
echo "   nano ~/.n8n/.env"
echo ""
echo "2. Start n8n:"
echo "   ~/start-n8n.sh"
echo ""
echo "3. Access n8n at: http://localhost:5678"
echo "   Username: admin"
echo "   Password: change_this_password (CHANGE THIS!)"
echo ""
echo "4. Import the workflow:"
echo "   - Go to n8n web interface"
echo "   - Click 'Import from File'"
echo "   - Select: workflow-blog-automation.json"
echo ""
echo "5. Configure credentials in n8n:"
echo "   - DeepSeek API (Header Auth)"
echo "   - NewsAPI (Header Auth)"
echo ""
echo "6. Test the workflow manually"
echo ""
echo "7. Enable the cron trigger for daily automation"
echo ""
echo "📚 Documentation:"
echo "   - n8n docs: https://docs.n8n.io/"
echo "   - DeepSeek API: https://platform.deepseek.com/api-docs/"
echo "   - NewsAPI: https://newsapi.org/docs"
echo ""
echo -e "${YELLOW}⚠️  Important Security Notes:${NC}"
echo "   - Change default n8n password in ~/.n8n/config"
echo "   - Keep API keys secure in ~/.n8n/.env"
echo "   - Use firewall to restrict n8n access"
echo "   - Consider using HTTPS with reverse proxy"
echo ""
echo "🎉 Happy automating!"
