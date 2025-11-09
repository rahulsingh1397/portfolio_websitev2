#!/usr/bin/env python3
"""
DeepSeek API Integration Script
Standalone script to generate blog posts using DeepSeek API
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

class DeepSeekBlogGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def summarize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a single article using DeepSeek Reasoner
        """
        prompt = f"""Summarize this article:

Title: {article.get('title', 'Unknown')}
URL: {article.get('url', 'Unknown')}
Date: {article.get('date', 'Unknown')}

Content:
{article.get('content', '')[:8000]}

Return ONLY valid JSON with this exact structure:
{{
  "title": "string",
  "summary": "3-sentence summary",
  "keyFacts": ["fact1", "fact2", "fact3"],
  "quotes": [{{"text": "quote", "context": "context"}}],
  "source": "source name",
  "url": "{article.get('url', '')}",
  "date": "ISO date",
  "reliability": 8
}}"""

        payload = {
            "model": "deepseek-reasoner",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a factual research summarizer. Extract key information and return structured JSON. Be precise and do NOT hallucinate."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content']
            return json.loads(content)
        except Exception as e:
            print(f"Error summarizing article: {e}")
            return None
    
    def generate_blog_post(self, research_bundle: Dict[str, Any]) -> str:
        """
        Generate a complete blog post from research bundle
        """
        prompt = f"""Create a comprehensive blog post using this research bundle:

{json.dumps(research_bundle, indent=2)}

REQUIREMENTS:

1. YAML FRONTMATTER (first lines):
---
title: "Compelling Title (60-70 chars)"
date: {research_bundle.get('generatedDate', datetime.now().isoformat())}
author: "AI Research Assistant"
tags: {json.dumps(research_bundle.get('tags', []))}
summary: "One compelling sentence (150-160 chars for SEO)"
ai_generated: true
human_reviewed: false
---

2. STRUCTURE:
- ## 🎯 TL;DR (3-4 bullet points)
- ## 📖 Introduction (2-3 paragraphs, set context)
- ## 🔍 Background (explain fundamentals)
- ## 🚀 Recent Developments (one H3 section per major finding)
- ## 🏢 Industry Applications (real company examples)
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
- Technical but accessible
- 1200-1800 words total

5. TRANSPARENCY:
- Mention "This post aggregates recent AI research" in intro
- Link to original sources

Generate the COMPLETE Markdown blog post now (including frontmatter)."""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert technical writer specializing in AI/ML/Data Science. Write comprehensive, well-researched blog posts with proper citations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error generating blog post: {e}")
            return None
    
    def save_blog_post(self, content: str, output_dir: str = "./content/blog") -> str:
        """
        Save blog post to file
        """
        # Extract title from frontmatter
        title_match = content.split('title:')[1].split('\n')[0] if 'title:' in content else 'ai-research-update'
        title = title_match.strip().strip('"').strip("'")
        
        # Create slug
        slug = title.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        
        # Create filename
        date = datetime.now().strftime('%Y-%m-%d')
        filename = f"{date}-{slug}.md"
        
        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Write file
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Blog post saved: {filepath}")
        return filepath


def main():
    """
    Example usage
    """
    # Get API key from environment
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ Error: DEEPSEEK_API_KEY environment variable not set")
        print("Set it with: export DEEPSEEK_API_KEY='your-api-key'")
        return
    
    # Initialize generator
    generator = DeepSeekBlogGenerator(api_key)
    
    # Example articles (replace with real data from NewsAPI/RSS)
    sample_articles = [
        {
            "title": "New Breakthrough in Large Language Models",
            "url": "https://example.com/article1",
            "date": "2025-11-06",
            "content": "Researchers have announced a significant breakthrough in large language model efficiency..."
        },
        {
            "title": "Advances in Computer Vision for Medical Imaging",
            "url": "https://example.com/article2",
            "date": "2025-11-05",
            "content": "A new computer vision model achieves state-of-the-art results in medical image analysis..."
        }
    ]
    
    print("📊 Summarizing articles...")
    summaries = []
    for article in sample_articles:
        summary = generator.summarize_article(article)
        if summary:
            summaries.append(summary)
            print(f"  ✓ Summarized: {article['title'][:50]}...")
    
    # Create research bundle
    research_bundle = {
        "generatedDate": datetime.now().isoformat(),
        "topic": "AI, Machine Learning & Data Science Updates",
        "sources": summaries,
        "totalSources": len(summaries),
        "tags": ["artificial-intelligence", "machine-learning", "data-science"]
    }
    
    print("\n✍️  Generating blog post...")
    blog_content = generator.generate_blog_post(research_bundle)
    
    if blog_content:
        print("\n💾 Saving blog post...")
        filepath = generator.save_blog_post(blog_content)
        print(f"\n🎉 Success! Blog post created at: {filepath}")
        
        # Print stats
        word_count = len(blog_content.split())
        citation_count = blog_content.count('[')
        print(f"\n📈 Stats:")
        print(f"  - Word count: {word_count}")
        print(f"  - Citations: {citation_count}")
        print(f"  - Sources: {len(summaries)}")
    else:
        print("\n❌ Failed to generate blog post")


if __name__ == "__main__":
    main()
