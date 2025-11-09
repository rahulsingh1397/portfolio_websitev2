#!/usr/bin/env python3
"""
Automated Blog Generator for AI/ML/Data Science Portfolio
Generates well-researched, cited blog posts using DeepSeek AI
"""

import os
import json
import requests
import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

# Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
OUTPUT_DIR = 'blog'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_news_sources():
    """Gather latest AI/ML/Data Science news from multiple sources"""
    sources = []
    
    # 1. NewsAPI
    if NEWSAPI_KEY:
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': 'artificial intelligence OR machine learning OR data science',
                'sortBy': 'publishedAt',
                'pageSize': 10,
                'language': 'en',
                'from': (datetime.now() - timedelta(days=2)).isoformat(),
                'apiKey': NEWSAPI_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for article in articles[:5]:
                    sources.append({
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'description': article.get('description', ''),
                        'publishedAt': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'Unknown')
                    })
                print(f"✓ Fetched {len(articles)} articles from NewsAPI")
        except Exception as e:
            print(f"✗ NewsAPI error: {e}")
    
    # 2. arXiv RSS Feed
    try:
        feed = feedparser.parse('http://export.arxiv.org/rss/cs.AI')
        for entry in feed.entries[:3]:
            sources.append({
                'title': entry.title,
                'url': entry.link,
                'description': entry.summary,
                'publishedAt': entry.get('published', ''),
                'source': 'arXiv'
            })
        print(f"✓ Fetched {len(feed.entries[:3])} papers from arXiv")
    except Exception as e:
        print(f"✗ arXiv RSS error: {e}")
    
    # 3. OpenAI Blog RSS
    try:
        feed = feedparser.parse('https://openai.com/blog/rss/')
        for entry in feed.entries[:2]:
            sources.append({
                'title': entry.title,
                'url': entry.link,
                'description': entry.get('summary', ''),
                'publishedAt': entry.get('published', ''),
                'source': 'OpenAI Blog'
            })
        print(f"✓ Fetched {len(feed.entries[:2])} posts from OpenAI Blog")
    except Exception as e:
        print(f"✗ OpenAI Blog RSS error: {e}")
    
    return sources


def score_and_filter_sources(sources):
    """Score sources by relevance and recency, keep top 6"""
    now = datetime.now()
    scored = []
    
    for source in sources:
        try:
            pub_date_str = source.get('publishedAt', '')
            if pub_date_str:
                # Try multiple date formats
                pub_date_str = pub_date_str.replace('Z', '+00:00')
                try:
                    pub_date = datetime.fromisoformat(pub_date_str)
                except:
                    # Try parsing RFC 2822 format (RSS feeds)
                    from email.utils import parsedate_to_datetime
                    pub_date = parsedate_to_datetime(source['publishedAt'])
            else:
                pub_date = now - timedelta(days=3)
        except:
            pub_date = now - timedelta(days=3)
        
        age_hours = (now - pub_date.replace(tzinfo=None)).total_seconds() / 3600
        score = 100 - (age_hours / 24)  # Score based on days, not hours
        
        print(f"  Source: {source['title'][:50]}... Age: {age_hours/24:.1f} days, Score: {score:.1f}")
        
        # Boost trusted sources
        trusted = ['Nature', 'Science', 'arXiv', 'OpenAI', 'Google', 'MIT', 'Stanford']
        if any(t.lower() in source['source'].lower() for t in trusted):
            score += 30
        
        # Boost relevant keywords
        title_lower = source['title'].lower()
        keywords = ['breakthrough', 'released', 'announced', 'open-source', 'research', 'state-of-the-art']
        if any(k in title_lower for k in keywords):
            score += 15
        
        # Penalize old content (relaxed for testing)
        if age_hours > 168:  # 1 week
            score -= 30
        if age_hours > 336:  # 2 weeks
            score -= 50
        
        if score > -20:  # Allow slightly negative scores for testing
            scored.append({**source, 'score': score})
    
    # Sort by score and keep top 6
    top_sources = sorted(scored, key=lambda x: x['score'], reverse=True)[:6]
    print(f"✓ Filtered {len(sources)} sources down to {len(top_sources)} top sources")
    
    return top_sources


def fetch_article_content(url):
    """Fetch and extract article text from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # Try to find article content
        article = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile('article|post-content'))
        
        if article:
            text = article.get_text(separator=' ', strip=True)
        else:
            # Fallback: get all paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        
        # Clean and limit text
        text = re.sub(r'\s+', ' ', text).strip()[:8000]
        return text
    except Exception as e:
        print(f"✗ Error fetching {url}: {e}")
        return ""


def summarize_with_deepseek(source):
    """Summarize article using DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        print("✗ DeepSeek API key not found")
        return None
    
    # Fetch full content
    full_text = fetch_article_content(source['url'])
    if not full_text:
        full_text = source['description']
    
    prompt = f"""Summarize this article:

Title: {source['title']}
URL: {source['url']}
Date: {source['publishedAt']}

Content:
{full_text}

Return ONLY valid JSON with this exact structure:
{{
  "title": "string",
  "summary": "3-sentence summary",
  "keyFacts": ["fact1", "fact2", "fact3"],
  "quotes": [{{"text": "quote", "context": "context"}}],
  "source": "{source['source']}",
  "url": "{source['url']}",
  "date": "{source['publishedAt']}",
  "reliability": 8
}}"""
    
    try:
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-reasoner',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a factual research summarizer. Extract key information and return structured JSON. Be precise and do NOT hallucinate.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.1,
                'max_tokens': 1000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return json.loads(content)
        else:
            print(f"✗ DeepSeek API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Summarization error: {e}")
        return None


def generate_blog_post(research_bundle):
    """Generate comprehensive blog post using DeepSeek"""
    if not DEEPSEEK_API_KEY:
        print("✗ DeepSeek API key not found")
        return None
    
    prompt = f"""Create a comprehensive blog post using this research bundle:

{json.dumps(research_bundle, indent=2)}

REQUIREMENTS:

1. YAML FRONTMATTER (first lines):
---
title: "Compelling Title (60-70 chars)"
date: {research_bundle['generatedDate']}
author: "AI Research Assistant"
tags: {json.dumps(research_bundle['tags'])}
summary: "One compelling sentence (150-160 chars for SEO)"
ai_generated: true
human_reviewed: false
---

2. STRUCTURE:
- ## 🎯 TL;DR (3-4 bullet points)
- ## 📖 Introduction (2-3 paragraphs, set context)
- ## 🔍 Background (explain fundamentals)
- ## 🚀 Recent Developments (one H3 section per major finding from sources)
- ## 🏢 Industry Applications (real company examples from sources)
- ## 💡 Practical Implications (for data scientists/engineers)
- ## 📊 Code Example (if applicable, simple Python/pseudocode)
- ## 🔮 Future Outlook (brief, grounded in sources)
- ## 📚 References (numbered list with full URLs)

3. CITATION RULES:
- Use [1], [2] inline after factual claims
- Each source must be cited at least once
- References section: [1] Title - Source Name (Date) - URL

4. STYLE:
- Use emojis for section headers only
- Write in active voice
- Use short paragraphs (3-4 sentences max)
- Include transition sentences
- Technical but accessible
- 1200-1800 words total

5. SEO:
- Include keywords naturally: AI, machine learning, data science
- Use descriptive subheadings
- Meta description in frontmatter

6. TRANSPARENCY:
- Mention "This post was generated by AI and aggregates recent research" in intro
- Link to original sources

Generate the COMPLETE Markdown blog post now (including frontmatter)."""
    
    try:
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-chat',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an expert technical writer specializing in AI/ML/Data Science. Write comprehensive, well-researched blog posts with proper citations. Target audience: data scientists, ML engineers, technical hiring managers. Style: professional, factual, engaging, accessible.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.2,
                'max_tokens': 4000
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"✗ DeepSeek API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Blog generation error: {e}")
        return None


def quality_check(blog_content):
    """Verify blog post quality"""
    word_count = len(blog_content.split())
    citation_count = len(re.findall(r'\[\d+\]', blog_content))
    has_references = '## 📚 References' in blog_content or '## References' in blog_content
    has_tldr = 'TL;DR' in blog_content
    has_code = '```' in blog_content
    
    issues = []
    if not has_references:
        issues.append('Missing references section')
    if not has_tldr:
        issues.append('Missing TL;DR')
    if word_count < 1000:
        issues.append(f'Word count too low: {word_count}')
    if citation_count < 3:
        issues.append(f'Too few citations: {citation_count}')
    
    passed = len(issues) == 0
    
    return {
        'passed': passed,
        'wordCount': word_count,
        'citationCount': citation_count,
        'hasReferences': has_references,
        'hasTLDR': has_tldr,
        'hasCodeExample': has_code,
        'issues': issues
    }


def save_blog_post(blog_content):
    """Save blog post to file"""
    # Extract title from frontmatter
    title_match = re.search(r'title:\s*["\'](.+?)["\']', blog_content)
    title = title_match.group(1) if title_match else 'AI Research Update'
    
    # Create slug
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    # Create filename
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print(f"✓ Blog post saved: {filepath}")
    return filepath


def main():
    """Main execution flow"""
    print("🤖 Starting automated blog generation...\n")
    
    # Step 1: Fetch sources
    print("📰 Fetching news sources...")
    sources = fetch_news_sources()
    
    if not sources:
        print("✗ No sources found. Exiting.")
        return
    
    # Step 2: Filter and score
    print("\n🎯 Filtering and scoring sources...")
    top_sources = score_and_filter_sources(sources)
    
    # Step 3: Summarize each source
    print("\n📝 Summarizing articles...")
    summaries = []
    for i, source in enumerate(top_sources, 1):
        print(f"  [{i}/{len(top_sources)}] Summarizing: {source['title'][:60]}...")
        summary = summarize_with_deepseek(source)
        if summary:
            summaries.append(summary)
    
    if not summaries:
        print("✗ No summaries generated. Exiting.")
        return
    
    # Step 4: Create research bundle
    print(f"\n📦 Aggregating {len(summaries)} summaries...")
    research_bundle = {
        'generatedDate': datetime.now().isoformat(),
        'generatedDateFormatted': datetime.now().strftime('%B %d, %Y'),
        'topic': 'AI, Machine Learning & Data Science Updates',
        'sources': summaries,
        'totalSources': len(summaries),
        'avgReliability': sum(s.get('reliability', 5) for s in summaries) / len(summaries),
        'tags': ['artificial-intelligence', 'machine-learning', 'data-science', 'ai-research', 'tech-news']
    }
    
    # Step 5: Generate blog post
    print("\n✍️  Generating blog post...")
    blog_content = generate_blog_post(research_bundle)
    
    if not blog_content:
        print("✗ Blog generation failed. Exiting.")
        return
    
    # Step 6: Quality check
    print("\n✅ Running quality checks...")
    quality = quality_check(blog_content)
    print(f"  Word count: {quality['wordCount']}")
    print(f"  Citations: {quality['citationCount']}")
    print(f"  Has references: {quality['hasReferences']}")
    print(f"  Has TL;DR: {quality['hasTLDR']}")
    print(f"  Has code example: {quality['hasCodeExample']}")
    
    if quality['issues']:
        print(f"  ⚠️  Issues: {', '.join(quality['issues'])}")
    else:
        print("  ✓ All quality checks passed!")
    
    # Step 7: Save blog post
    print("\n💾 Saving blog post...")
    filepath = save_blog_post(blog_content)
    
    print(f"\n🎉 Blog generation complete!")
    print(f"📄 File: {filepath}")
    print(f"📊 Stats: {quality['wordCount']} words, {quality['citationCount']} citations")


if __name__ == '__main__':
    main()
