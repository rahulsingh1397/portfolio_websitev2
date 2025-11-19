# 🚀 Blog Automation Setup Guide

## ✅ Best Solution: GitHub Actions + Python (Netlify Compatible)

**Why this beats n8n/Docker:**
- ✅ **Free** - GitHub Actions free tier
- ✅ **Netlify Compatible** - Auto-deploys on git push
- ✅ **No Server** - Runs in GitHub cloud
- ✅ **Windows Compatible** - Test locally
- ✅ **Simple** - No complex installation

---

## 📋 Quick Start (5 Minutes)

### Step 1: Get API Keys

1. **DeepSeek API** (Required - $0.01/post)
   - Go to: https://platform.deepseek.com/
   - Sign up and get API key
   - Copy the key

2. **NewsAPI** (Optional - Free)
   - Go to: https://newsapi.org/register
   - Sign up and get API key
   - Copy the key

### Step 2: Test Locally (Recommended)

```bash
# Navigate to blog-automation folder
cd "e:\Private\Data Scientist Portfolio\blog-automation"

# Run the test script
test_local.bat

# Or manually:
pip install -r requirements.txt
set DEEPSEEK_API_KEY=your_key_here
set NEWSAPI_KEY=your_key_here
python generate_blog.py
```

**Expected output:**
- Script fetches news from multiple sources
- Summarizes articles using DeepSeek AI
- Generates a complete blog post
- Saves to `blog/YYYY-MM-DD-title.md`

### Step 3: Add Secrets to GitHub

1. Push this code to GitHub:
   ```bash
   git add .
   git commit -m "Add blog automation"
   git push origin main
   ```

2. Go to your GitHub repository
3. Click **Settings** → **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add:
   - Name: `DEEPSEEK_API_KEY`, Value: your DeepSeek key
   - Name: `NEWSAPI_KEY`, Value: your NewsAPI key

### Step 4: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable workflows if prompted
3. Find **Auto-Generate Blog Post** workflow
4. Click **Run workflow** → **Run workflow** (manual test)

### Step 5: Verify Netlify Auto-Deploy

1. After GitHub Action completes, check your repository
2. New file should appear in `blog/` folder
3. Netlify will automatically detect the change and deploy
4. Check your Netlify site in ~2 minutes

---

## 🔄 How It Works

```
Daily at 8 AM UTC (3 AM EST)
        ↓
GitHub Actions Triggers
        ↓
Fetch AI/ML News (NewsAPI, arXiv, OpenAI Blog)
        ↓
Filter & Score Top 6 Sources
        ↓
DeepSeek AI Summarizes Each
        ↓
DeepSeek AI Generates Blog Post (1200-1800 words)
        ↓
Quality Check (citations, word count, structure)
        ↓
Save to blog/YYYY-MM-DD-title.md
        ↓
Git Commit & Push
        ↓
Netlify Auto-Deploy
        ↓
Live on Your Portfolio! 🎉
```

---

## 📊 What You Get

Each blog post includes:
- ✅ **1200-1800 words** of professional content
- ✅ **5-7 cited sources** from trusted publications
- ✅ **Inline citations** [1], [2], etc. with full references
- ✅ **SEO optimization** (meta description, tags, keywords)
- ✅ **Code examples** when applicable
- ✅ **Structured format** (TL;DR, Introduction, Developments, etc.)
- ✅ **YAML frontmatter** for static site generators

---

## 💰 Cost Breakdown

| Service | Usage | Cost |
|---------|-------|------|
| DeepSeek API | 30 blogs/month | **$0.30-0.90/month** |
| NewsAPI | Free tier | $0 |
| GitHub Actions | Free tier (2000 min/month) | $0 |
| Netlify | Free tier | $0 |
| **TOTAL** | | **~$0.50/month** |

**Compare to:**
- OpenAI GPT-4: ~$15-30/month
- Human writer: $50-200 per post
- Content agency: $500-2000/month

---

## ⚙️ Customization

### Change Schedule

Edit `.github/workflows/auto-blog.yml`:
```yaml
schedule:
  - cron: '0 8 * * *'    # Daily at 8 AM UTC
  # - cron: '0 8 * * 1'  # Weekly on Monday
  # - cron: '0 8 1 * *'  # Monthly on 1st
  # - cron: '0 */6 * * *' # Every 6 hours
```

### Change Blog Length

Edit `blog-automation/generate_blog.py` line ~250:
```python
# In the prompt, change:
"1200-1800 words total"
# To:
"800-1200 words total"  # Shorter
"2000-2500 words total"  # Longer
```

### Add More Sources

Edit `blog-automation/generate_blog.py` in `fetch_news_sources()`:
```python
# Add more RSS feeds:
feed = feedparser.parse('https://blog.google/technology/ai/rss/')
feed = feedparser.parse('https://www.microsoft.com/en-us/research/feed/')
feed = feedparser.parse('https://research.facebook.com/feed/')
```

### Change Writing Style

Edit `blog-automation/generate_blog.py` in `generate_blog_post()`:
```python
# System prompt - add to content:
"Use a conversational, friendly tone"
# Or:
"Write in an academic, formal style"
# Or:
"Focus on practical, actionable insights"
```

---

## 🐛 Troubleshooting

### Local Test Fails

**Error: "DeepSeek API key not found"**
```bash
# Make sure you set the environment variable:
set DEEPSEEK_API_KEY=your_actual_key_here
python generate_blog.py
```

**Error: "No module named 'requests'"**
```bash
pip install -r requirements.txt
```

### GitHub Actions Fails

**Error: "API key not found"**
- Go to Settings → Secrets and variables → Actions
- Verify secret names are EXACTLY: `DEEPSEEK_API_KEY`, `NEWSAPI_KEY`
- Re-add secrets if needed

**Error: "Permission denied"**
- Go to Settings → Actions → General
- Under "Workflow permissions", select "Read and write permissions"
- Click Save

### No Blog Post Generated

1. Check GitHub Actions logs:
   - Go to Actions tab
   - Click on the failed workflow run
   - Expand steps to see errors

2. Test locally first:
   ```bash
   cd blog-automation
   python generate_blog.py
   ```

3. Verify API keys are valid:
   - Test DeepSeek key at https://platform.deepseek.com/
   - Check usage limits

### Netlify Not Deploying

1. Check if blog post was committed to GitHub
2. Verify Netlify is connected to your repository
3. Check Netlify build logs for errors
4. Ensure `blog/` folder is not in `.gitignore`

---

## 📈 Monitoring & Maintenance

### Check Blog Quality

After first few posts, review:
- ✅ Word count (should be 1200-1800)
- ✅ Citation count (should be 5+)
- ✅ References section present
- ✅ Code examples when applicable
- ✅ Proper formatting

### Adjust Prompts

If quality issues:
1. Edit `generate_blog.py`
2. Modify system prompts or requirements
3. Test locally
4. Commit changes

### Monitor Costs

- Check DeepSeek dashboard monthly
- Should be $0.30-0.90/month for daily posts
- GitHub Actions usage visible in Settings → Billing

---

## 🎉 Success Checklist

- [ ] DeepSeek API key obtained
- [ ] NewsAPI key obtained (optional)
- [ ] Local test successful
- [ ] Code pushed to GitHub
- [ ] Secrets added to GitHub
- [ ] GitHub Actions enabled
- [ ] Manual workflow run successful
- [ ] Blog post appears in repository
- [ ] Netlify auto-deployed
- [ ] Blog post visible on live site

**All done?** You now have fully automated blog generation! 🚀

---

## 📞 Need Help?

1. **Test locally first** - Run `test_local.bat`
2. **Check logs** - GitHub Actions tab shows detailed errors
3. **Verify API keys** - Test at provider dashboards
4. **Review prompts** - Adjust in `generate_blog.py` if needed

---

## 🔮 Next Steps

1. **Monitor first week** - Review quality of generated posts
2. **Adjust prompts** - Fine-tune writing style
3. **Add sources** - Include more RSS feeds
4. **Customize schedule** - Change frequency if needed
5. **Share results** - Showcase on LinkedIn/Twitter

**Happy automating!** 🤖✨
