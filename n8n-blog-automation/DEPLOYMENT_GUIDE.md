# Complete Deployment Guide - n8n Blog Automation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Workflow Import](#workflow-import)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Maintenance](#maintenance)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This guide walks you through deploying the automated blog generation system that:
- Runs daily at 8 AM
- Gathers AI/ML/Data Science news from multiple sources
- Generates a well-researched, cited blog post
- Commits to Git and deploys to your portfolio
- Costs ~$1-3/month

**Expected Results:**
- 1 blog post per day (1200-1800 words)
- 5-7 cited sources per post
- Professional technical writing
- SEO optimized
- Fully automated

---

## 📦 Prerequisites

### Required Accounts & API Keys

1. **DeepSeek API** (Primary LLM)
   - Sign up: https://platform.deepseek.com/
   - Get API key from dashboard
   - Cost: ~$0.01-0.03 per blog post

2. **NewsAPI** (News aggregation)
   - Sign up: https://newsapi.org/register
   - Free tier: 100 requests/day (sufficient)
   - Get API key from account page

3. **GitHub Account** (Optional - for backup)
   - For pushing blog posts to remote repo

### System Requirements

- **OS:** Ubuntu 20.04+ (or similar Linux)
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 10GB free space
- **Network:** Stable internet connection

---

## 🚀 Installation

### Option 1: Automated Setup (Recommended)

```bash
# 1. Download the setup script
cd ~/Downloads
# (Copy setup-ubuntu.sh to your system)

# 2. Make it executable
chmod +x setup-ubuntu.sh

# 3. Run the setup
./setup-ubuntu.sh

# Follow the prompts - the script will:
# - Install Node.js, n8n, PM2, Git, Python, Hugo
# - Create directory structure
# - Set up configuration files
# - Create helper scripts
```

### Option 2: Manual Setup

```bash
# 1. Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. Install n8n globally
sudo npm install -g n8n

# 3. Install PM2 (process manager)
sudo npm install -g pm2

# 4. Install Git
sudo apt-get install -y git

# 5. Install Python & dependencies
sudo apt-get install -y python3 python3-pip
pip3 install requests python-dotenv

# 6. Install Hugo (static site generator)
sudo snap install hugo

# 7. Create directories
mkdir -p ~/portfolio/content/blog
mkdir -p ~/portfolio/static/images/blog
mkdir -p ~/.n8n
```

---

## ⚙️ Configuration

### Step 1: Configure API Keys

```bash
# Create environment file
nano ~/.n8n/.env
```

Add your API keys:

```bash
# API Keys (REQUIRED)
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
NEWSAPI_KEY=your-newsapi-key-here

# Portfolio Paths
PORTFOLIO_PATH=/home/youruser/portfolio
BLOG_CONTENT_PATH=/home/youruser/portfolio/content/blog

# Git Configuration
GIT_USER_NAME="Your Name"
GIT_USER_EMAIL="your.email@example.com"

# Notification Email (Optional)
NOTIFICATION_EMAIL=your.email@example.com
```

**Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

### Step 2: Configure n8n

```bash
# Edit n8n config
nano ~/.n8n/config
```

Update credentials:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_secure_password_here
N8N_HOST=0.0.0.0
N8N_PORT=5678
```

### Step 3: Start n8n

```bash
# Start n8n with PM2
pm2 start n8n
pm2 save
pm2 startup  # Enable auto-start on boot

# Check status
pm2 status
```

### Step 4: Access n8n Web Interface

Open browser and go to:
```
http://localhost:5678
```

Login with credentials from Step 2.

---

## 📥 Workflow Import

### Step 1: Import Workflow JSON

1. In n8n web interface, click **"Import from File"**
2. Select `workflow-blog-automation.json`
3. Click **"Import"**

### Step 2: Configure Credentials

#### DeepSeek API Credential

1. Go to **Credentials** → **New**
2. Select **"Header Auth"**
3. Name: `DeepSeek API`
4. Header Name: `Authorization`
5. Header Value: `Bearer YOUR_DEEPSEEK_API_KEY`
6. **Save**

#### NewsAPI Credential

1. Go to **Credentials** → **New**
2. Select **"Header Auth"**
3. Name: `NewsAPI Credentials`
4. Header Name: `X-Api-Key`
5. Header Value: `YOUR_NEWSAPI_KEY`
6. **Save**

### Step 3: Update Workflow Nodes

Update these nodes with your paths:

**Node: "Write Blog File"**
```
File Path: /home/youruser/portfolio/content/blog/{{ $json.filename }}
```

**Node: "Git Commit & Push"**
```bash
cd /home/youruser/portfolio && \
git add content/blog/*.md && \
git commit -m "Auto-blog: {{ $json.title }}" && \
git push origin main
```

**Node: "Build & Deploy Site"**
```bash
cd /home/youruser/portfolio && \
hugo && \
pm2 restart portfolio
```

### Step 4: Save Workflow

Click **"Save"** in the top right.

---

## 🧪 Testing

### Test 1: Manual Execution

1. In n8n workflow editor, click **"Execute Workflow"**
2. Watch the execution flow
3. Check for errors in each node
4. Verify blog post created in `~/portfolio/content/blog/`

### Test 2: Verify Blog Content

```bash
# List blog posts
ls -lh ~/portfolio/content/blog/

# View latest post
cat ~/portfolio/content/blog/$(ls -t ~/portfolio/content/blog/ | head -1)
```

**Check for:**
- ✅ YAML frontmatter present
- ✅ TL;DR section
- ✅ Multiple sections with emojis
- ✅ Inline citations [1], [2], etc.
- ✅ References section with URLs
- ✅ 1200+ words

### Test 3: Quality Checks

```bash
# Word count
wc -w ~/portfolio/content/blog/*.md

# Citation count
grep -o '\[[0-9]\+\]' ~/portfolio/content/blog/*.md | wc -l

# Check for references section
grep -i "## 📚 References" ~/portfolio/content/blog/*.md
```

---

## 🌐 Production Deployment

### Option 1: Hugo Static Site

```bash
# Initialize Hugo site
cd ~/portfolio
hugo new site . --force

# Add theme (example: PaperMod)
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# Configure Hugo
nano config.toml
```

Add configuration:

```toml
baseURL = "http://yourportfolio.com/"
languageCode = "en-us"
title = "Your Name - Data Scientist Portfolio"
theme = "PaperMod"

[params]
  description = "AI/ML/Data Science Blog"
  author = "Your Name"

[[menu.main]]
  name = "Blog"
  url = "/blog/"
  weight = 1
```

Build and serve:

```bash
# Build site
hugo

# Serve with PM2
pm2 start hugo -- server --bind 0.0.0.0 --port 1313 --baseURL http://localhost:1313
pm2 save
```

### Option 2: Netlify Deployment

Your portfolio is already configured for Netlify! The blog posts will automatically be included when you push to GitHub.

```bash
# Ensure blog posts are in the repo
cd ~/portfolio
git add content/blog/*.md
git commit -m "Add automated blog posts"
git push origin main

# Netlify will auto-deploy
```

### Option 3: Next.js Static Export

```bash
# Initialize Next.js
cd ~/portfolio
npx create-next-app@latest . --typescript --tailwind --app

# Add blog posts to /app/blog/
# Configure next.config.js for static export

# Build
npm run build
npm run export

# Serve
pm2 start npm --name "portfolio" -- start
```

---

## 🔄 Enable Automation

### Activate Cron Trigger

1. In n8n workflow editor
2. Find **"Daily Trigger - 8 AM"** node
3. Click **"Activate"** toggle in top right
4. Workflow will now run daily at 8 AM

### Verify Cron Schedule

```bash
# Check n8n logs
pm2 logs n8n

# You should see:
# "Workflow activated"
# "Cron trigger set for 0 8 * * *"
```

---

## 🔧 Maintenance

### Daily Checks

```bash
# View latest blog post
ls -lt ~/portfolio/content/blog/ | head -5

# Check n8n logs
pm2 logs n8n --lines 50

# Check execution history in n8n web interface
```

### Weekly Tasks

1. **Review generated posts** for quality
2. **Check API usage** (DeepSeek dashboard)
3. **Verify Git commits** are working
4. **Monitor disk space**

```bash
df -h ~/portfolio
```

### Monthly Tasks

1. **Update dependencies**
```bash
sudo npm update -g n8n
pip3 install --upgrade requests
```

2. **Backup blog posts**
```bash
tar -czf blog-backup-$(date +%Y%m%d).tar.gz ~/portfolio/content/blog/
```

3. **Review and update RSS feeds** in workflow

---

## 🐛 Troubleshooting

### Issue: Workflow fails at "Fetch Article HTML"

**Cause:** Website blocking requests or timeout

**Solution:**
```javascript
// In "Fetch Article HTML" node, add:
{
  "headers": {
    "User-Agent": "Mozilla/5.0 (compatible; BlogBot/1.0)"
  },
  "timeout": 15000
}
```

### Issue: DeepSeek API returns error

**Cause:** Invalid API key or rate limit

**Solution:**
1. Verify API key in credentials
2. Check DeepSeek dashboard for usage limits
3. Add retry logic:

```javascript
// In DeepSeek nodes, wrap in try-catch
try {
  // API call
} catch (error) {
  if (error.response?.status === 429) {
    // Wait and retry
    await new Promise(r => setTimeout(r, 5000));
    // Retry API call
  }
}
```

### Issue: Blog post has no citations

**Cause:** LLM not following prompt

**Solution:**
1. Check "System Prompts" are correctly set
2. Reduce temperature to 0.1
3. Add explicit instruction in prompt:
```
CRITICAL: Every factual claim MUST have an inline citation [N].
```

### Issue: Git push fails

**Cause:** Authentication or remote not configured

**Solution:**
```bash
# Configure Git credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add remote if missing
cd ~/portfolio
git remote add origin https://github.com/yourusername/portfolio.git

# Use SSH for authentication
ssh-keygen -t ed25519 -C "your.email@example.com"
cat ~/.ssh/id_ed25519.pub  # Add to GitHub

# Test
git push origin main
```

### Issue: n8n not starting

**Cause:** Port already in use or corrupted data

**Solution:**
```bash
# Check what's using port 5678
sudo lsof -i :5678

# Kill process if needed
sudo kill -9 <PID>

# Clear n8n cache
rm -rf ~/.n8n/cache

# Restart
pm2 restart n8n
```

### Issue: Blog posts not building

**Cause:** Hugo/Next.js configuration issue

**Solution:**
```bash
# Test Hugo build
cd ~/portfolio
hugo --verbose

# Check for errors in frontmatter
# Ensure dates are in ISO format: 2025-11-06
```

---

## 📊 Monitoring & Analytics

### Track Blog Performance

```bash
# Count total posts
ls ~/portfolio/content/blog/*.md | wc -l

# Average word count
for f in ~/portfolio/content/blog/*.md; do wc -w "$f"; done | awk '{sum+=$1; count++} END {print sum/count}'

# Citation statistics
grep -roh '\[[0-9]\+\]' ~/portfolio/content/blog/ | sort -u | wc -l
```

### Cost Monitoring

**DeepSeek API:**
- Check usage: https://platform.deepseek.com/usage
- Expected: $0.01-0.03 per blog post
- Monthly: ~$0.30-0.90 for 30 posts

**NewsAPI:**
- Free tier: 100 requests/day
- Usage: ~20 requests per workflow run
- Well within limits

---

## 🔐 Security Best Practices

1. **Protect API Keys**
```bash
chmod 600 ~/.n8n/.env
```

2. **Use Firewall**
```bash
sudo ufw allow 5678/tcp  # Only from trusted IPs
sudo ufw enable
```

3. **Enable HTTPS** (if exposing n8n publicly)
```bash
# Use Nginx reverse proxy with Let's Encrypt
sudo apt-get install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d n8n.yourdomain.com
```

4. **Regular Backups**
```bash
# Backup n8n workflows
cp -r ~/.n8n ~/backups/n8n-$(date +%Y%m%d)

# Backup blog posts
tar -czf ~/backups/blog-$(date +%Y%m%d).tar.gz ~/portfolio/content/blog/
```

---

## 📚 Additional Resources

- **n8n Documentation:** https://docs.n8n.io/
- **DeepSeek API Docs:** https://platform.deepseek.com/api-docs/
- **NewsAPI Docs:** https://newsapi.org/docs
- **Hugo Documentation:** https://gohugo.io/documentation/
- **PM2 Documentation:** https://pm2.keymetrics.io/docs/

---

## 🎉 Success Checklist

- [ ] n8n installed and running
- [ ] Workflow imported successfully
- [ ] API credentials configured
- [ ] Manual test execution successful
- [ ] Blog post generated with proper format
- [ ] Git commits working
- [ ] Site builds successfully
- [ ] Cron trigger activated
- [ ] Monitoring set up
- [ ] Backups configured

---

**Congratulations!** Your automated blog system is now live. You'll have a new, well-researched blog post every day at 8 AM! 🚀

**Version:** 1.0  
**Last Updated:** November 6, 2025  
**Support:** Check troubleshooting section or n8n community forums
