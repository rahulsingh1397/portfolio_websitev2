# 🤖 Automated Blog Generator - GitHub Actions Edition

**Generate AI/ML/Data Science blog posts automatically using GitHub Actions + DeepSeek AI**

## ✅ Why This Approach?

- ✅ **Free** - GitHub Actions free tier (2000 min/month)
- ✅ **Netlify Compatible** - Auto-deploys on git push
- ✅ **No Server Needed** - Runs in GitHub cloud
- ✅ **Windows Compatible** - Test locally on your machine
- ✅ **Simple** - No Docker or n8n installation required

## 🚀 Quick Setup (5 minutes)

### 1. Get API Keys

**DeepSeek API** (Required)
- Sign up: https://platform.deepseek.com/
- Get API key from dashboard
- Cost: ~$0.01-0.03 per blog post

**NewsAPI** (Optional but recommended)
- Sign up: https://newsapi.org/register
- Free tier: 100 requests/day
- Get API key from account page

### 2. Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key
   - `NEWSAPI_KEY`: Your NewsAPI key (optional)

### 3. Test Locally (Optional)

```bash
# Install dependencies
pip install requests beautifulsoup4 feedparser

# Set environment variables
set DEEPSEEK_API_KEY=your_key_here
set NEWSAPI_KEY=your_key_here

# Run the script
python blog-automation/generate_blog.py
```

### 4. Enable GitHub Actions

1. Push this code to your GitHub repository
2. Go to **Actions** tab
3. Enable workflows if prompted
4. Click **Auto-Generate Blog Post** workflow
5. Click **Run workflow** to test manually

### 5. Automatic Daily Runs

The workflow runs automatically every day at 8 AM UTC (3 AM EST).

You can change the schedule in `.github/workflows/auto-blog.yml`:
```yaml
schedule:
  - cron: '0 8 * * *'  # Daily at 8 AM UTC
  # - cron: '0 8 * * 1'  # Weekly on Monday
  # - cron: '0 8 1 * *'  # Monthly on 1st
```

## 📁 Project Structure

```
blog-automation/
├── generate_blog.py          # Main Python script
└── README.md                  # This file

.github/workflows/
└── auto-blog.yml              # GitHub Actions workflow

blog/
└── YYYY-MM-DD-title.md        # Generated blog posts
```

## 🔄 How It Works

```
┌─────────────────────────────────────────┐
│   GitHub Actions (Daily at 8 AM)        │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Fetch Sources  │
        │ - NewsAPI      │
        │ - arXiv RSS    │
        │ - OpenAI Blog  │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Filter & Score │
        │ (Keep top 6)   │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ DeepSeek AI    │
        │ Summarize Each │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ DeepSeek AI    │
        │ Generate Blog  │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Quality Check  │
        │ Save to blog/  │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Git Commit     │
        │ & Push         │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Netlify        │
        │ Auto-Deploy    │
        └────────────────┘
```

## 📊 Output Example

Each blog post includes:
- **1200-1800 words** of professional content
- **5-7 cited sources** from trusted publications
- **Inline citations** [1], [2], etc.
- **SEO optimization** (meta description, tags)
- **Code examples** when applicable
- **Structured format** (TL;DR, sections, references)

Example filename: `2025-11-06-breakthrough-advances-in-llm-efficiency.md`

## 💰 Cost

| Service | Usage | Cost |
|---------|-------|------|
| **DeepSeek API** | 30 blogs/month | $0.30-0.90/month |
| **NewsAPI** | Free tier | $0 |
| **GitHub Actions** | Free tier | $0 |
| **Netlify** | Free tier | $0 |
| **Total** | | **$0.30-0.90/month** |

## 🛠️ Customization

### Change Blog Length
Edit `generate_blog.py` line 250:
```python
# Change from:
- 1200-1800 words total

# To:
- 800-1200 words total  # Shorter
- 2000-2500 words total  # Longer
```

### Add More Sources
Edit `generate_blog.py` in `fetch_news_sources()`:
```python
# Add more RSS feeds
feed = feedparser.parse('https://blog.google/technology/ai/rss/')
feed = feedparser.parse('https://www.microsoft.com/en-us/research/feed/')
```

### Change Writing Style
Edit the system prompt in `generate_blog_post()`:
```python
'content': 'You are an expert technical writer...'
# Add: "Use a conversational tone"
# Or: "Write in an academic style"
```

## 🐛 Troubleshooting

### Workflow fails with "API key not found"
- Check that secrets are added in GitHub Settings → Secrets
- Secret names must match exactly: `DEEPSEEK_API_KEY`, `NEWSAPI_KEY`

### No blog post generated
- Check GitHub Actions logs for errors
- Verify API keys are valid
- Test locally first with `python generate_blog.py`

### Blog quality issues
- Lower temperature in DeepSeek API calls (0.1 instead of 0.2)
- Increase max_tokens for longer posts
- Add more sources for better content

## 📈 Next Steps

1. **Test locally** to verify it works
2. **Run manually** in GitHub Actions
3. **Review first blog post** and adjust prompts if needed
4. **Enable daily automation** and let it run
5. **Monitor quality** and tweak as needed

## 🎉 Success!

Once set up, you'll get:
- ✅ 1 high-quality blog post per day
- ✅ Automatic deployment to Netlify
- ✅ SEO-optimized content
- ✅ Professional technical writing
- ✅ All for less than $1/month

**Questions?** Test locally first, then check GitHub Actions logs.
