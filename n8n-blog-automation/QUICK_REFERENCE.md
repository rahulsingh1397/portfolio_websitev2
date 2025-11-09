# ⚡ Quick Reference Card - n8n Blog Automation

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Setup
chmod +x setup-ubuntu.sh && ./setup-ubuntu.sh

# 2. Configure
nano ~/.n8n/.env  # Add API keys

# 3. Start
~/start-n8n.sh

# 4. Access
http://localhost:5678  # Import workflow

# 5. Test
# Click "Execute Workflow" in n8n

# 6. Activate
# Toggle "Active" in workflow
```

---

## 🔑 Essential Commands

### n8n Management
```bash
# Start n8n
~/start-n8n.sh
# or
pm2 start n8n

# Stop n8n
~/stop-n8n.sh
# or
pm2 stop n8n

# Restart n8n
pm2 restart n8n

# View logs
~/n8n-logs.sh
# or
pm2 logs n8n

# Check status
pm2 status
```

### Blog Management
```bash
# List blog posts
ls -lh ~/portfolio/content/blog/

# View latest post
cat ~/portfolio/content/blog/$(ls -t ~/portfolio/content/blog/ | head -1)

# Count posts
ls ~/portfolio/content/blog/*.md | wc -l

# Word count
wc -w ~/portfolio/content/blog/*.md

# Citation count
grep -o '\[[0-9]\+\]' ~/portfolio/content/blog/*.md | wc -l
```

### Git Operations
```bash
# Check status
cd ~/portfolio && git status

# Manual commit
git add content/blog/*.md
git commit -m "Add blog posts"
git push origin main

# View history
git log --oneline -10
```

### Site Building
```bash
# Hugo
cd ~/portfolio && hugo

# Next.js
cd ~/portfolio && npm run build

# Serve locally
pm2 start hugo -- server --bind 0.0.0.0
```

---

## 📁 Important Paths

```
~/.n8n/.env                          # API keys
~/.n8n/config                        # n8n configuration
~/portfolio/content/blog/            # Blog posts
~/n8n-ecosystem.config.js            # PM2 config
~/.n8n/logs/                         # n8n logs
```

---

## 🔧 Common Tasks

### Add New RSS Feed
1. Open workflow in n8n
2. Add "RSS Feed Read" node
3. Enter feed URL
4. Connect to "Merge Sources" node
5. Save workflow

### Change Schedule
1. Open workflow
2. Click "Daily Trigger" node
3. Edit cron expression:
   - `0 8 * * *` = Daily 8 AM
   - `0 8 * * 1` = Weekly Monday
   - `0 8 1 * *` = Monthly 1st
4. Save workflow

### Update Prompts
1. Edit `system-prompts.md`
2. Copy new prompt
3. Open workflow → "DeepSeek - Generate Blog" node
4. Paste in "System" message
5. Save workflow

### Check API Usage
- DeepSeek: https://platform.deepseek.com/usage
- NewsAPI: https://newsapi.org/account

---

## 🐛 Quick Troubleshooting

### Workflow Not Running
```bash
# Check if n8n is running
pm2 status

# Check logs for errors
pm2 logs n8n --lines 50

# Restart n8n
pm2 restart n8n
```

### API Errors
```bash
# Verify API keys
cat ~/.n8n/.env | grep API_KEY

# Test DeepSeek API
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}]}'
```

### Git Push Fails
```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Add remote
cd ~/portfolio
git remote add origin https://github.com/user/repo.git

# Use SSH
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub  # Add to GitHub
```

### Blog Not Building
```bash
# Check Hugo
cd ~/portfolio && hugo --verbose

# Check frontmatter
head -20 ~/portfolio/content/blog/*.md

# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('file.md').read().split('---')[1])"
```

---

## 📊 Monitoring

### Daily Checks
```bash
# New posts today
ls -lt ~/portfolio/content/blog/ | head -5

# Execution logs
pm2 logs n8n --lines 20

# Disk space
df -h ~/portfolio
```

### Weekly Checks
```bash
# Total posts this week
find ~/portfolio/content/blog/ -name "*.md" -mtime -7 | wc -l

# Average word count
for f in ~/portfolio/content/blog/*.md; do wc -w "$f"; done | awk '{sum+=$1; n++} END {print sum/n}'

# API costs
# Check DeepSeek dashboard
```

---

## 🔐 Security Quick Checks

```bash
# Check file permissions
ls -la ~/.n8n/.env  # Should be 600

# Check firewall
sudo ufw status

# Check n8n auth
grep AUTH ~/.n8n/config

# Review logs for suspicious activity
pm2 logs n8n | grep -i error
```

---

## 💡 Quick Tips

### Improve Quality
- Lower temperature to 0.1 for more factual output
- Add more trusted RSS sources
- Increase minimum word count
- Add second LLM review step

### Reduce Costs
- Use DeepSeek Reasoner for summaries (cheaper)
- Reduce max_tokens in API calls
- Filter sources more aggressively
- Cache API responses

### Speed Up
- Run source fetching in parallel
- Reduce article fetch timeout
- Skip quality check for trusted sources
- Use faster model for summaries

---

## 📞 Emergency Contacts

### If Everything Breaks
```bash
# 1. Stop n8n
pm2 stop n8n

# 2. Backup data
cp -r ~/.n8n ~/backup-n8n-$(date +%Y%m%d)

# 3. Clear cache
rm -rf ~/.n8n/cache

# 4. Restart
pm2 restart n8n

# 5. Check logs
pm2 logs n8n
```

### Reset Workflow
1. Export current workflow (backup)
2. Delete workflow in n8n
3. Re-import from `workflow-blog-automation.json`
4. Reconfigure credentials
5. Test manually

---

## 📚 Quick Links

- **n8n UI:** http://localhost:5678
- **DeepSeek Dashboard:** https://platform.deepseek.com/
- **NewsAPI Dashboard:** https://newsapi.org/account
- **n8n Docs:** https://docs.n8n.io/
- **Community:** https://community.n8n.io/

---

## 🎯 Performance Targets

| Metric | Target | Check |
|--------|--------|-------|
| Posts/day | 1 | `ls ~/portfolio/content/blog/ \| wc -l` |
| Word count | 1200-1800 | `wc -w ~/portfolio/content/blog/*.md` |
| Citations | 5-7 | `grep -o '\[[0-9]\+\]' file.md \| wc -l` |
| Execution time | <5 min | Check n8n execution history |
| Success rate | >95% | Check n8n execution history |
| Cost/month | <$3 | Check DeepSeek dashboard |

---

## 🔄 Backup & Restore

### Backup
```bash
# Backup n8n workflows
cp -r ~/.n8n ~/backups/n8n-$(date +%Y%m%d)

# Backup blog posts
tar -czf ~/backups/blog-$(date +%Y%m%d).tar.gz ~/portfolio/content/blog/

# Backup config
cp ~/.n8n/.env ~/backups/.env-$(date +%Y%m%d)
```

### Restore
```bash
# Restore n8n
cp -r ~/backups/n8n-YYYYMMDD/* ~/.n8n/

# Restore blog posts
tar -xzf ~/backups/blog-YYYYMMDD.tar.gz -C ~/

# Restart
pm2 restart n8n
```

---

## 🎉 Success Checklist

Daily:
- [ ] New blog post generated
- [ ] Git commit successful
- [ ] Site rebuilt
- [ ] No errors in logs

Weekly:
- [ ] 7 posts published
- [ ] All posts have citations
- [ ] API costs under budget
- [ ] Backup created

Monthly:
- [ ] 30 posts published
- [ ] Review post quality
- [ ] Update RSS sources
- [ ] Check for updates

---

**Keep this card handy for quick reference!** 📌

**Version:** 1.0  
**Last Updated:** November 6, 2025
