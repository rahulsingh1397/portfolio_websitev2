/**
 * DeepSeek API Integration Script (JavaScript/Node.js)
 * Standalone script to generate blog posts using DeepSeek API
 */

const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

class DeepSeekBlogGenerator {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://api.deepseek.com/v1/chat/completions';
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }

    /**
     * Summarize a single article using DeepSeek Reasoner
     */
    async summarizeArticle(article) {
        const prompt = `Summarize this article:

Title: ${article.title || 'Unknown'}
URL: ${article.url || 'Unknown'}
Date: ${article.date || 'Unknown'}

Content:
${(article.content || '').substring(0, 8000)}

Return ONLY valid JSON with this exact structure:
{
  "title": "string",
  "summary": "3-sentence summary",
  "keyFacts": ["fact1", "fact2", "fact3"],
  "quotes": [{"text": "quote", "context": "context"}],
  "source": "source name",
  "url": "${article.url || ''}",
  "date": "ISO date",
  "reliability": 8
}`;

        const payload = {
            model: 'deepseek-reasoner',
            messages: [
                {
                    role: 'system',
                    content: 'You are a factual research summarizer. Extract key information and return structured JSON. Be precise and do NOT hallucinate.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            temperature: 0.1,
            max_tokens: 1000
        };

        try {
            const response = await axios.post(this.baseUrl, payload, {
                headers: this.headers,
                timeout: 30000
            });
            const content = response.data.choices[0].message.content;
            return JSON.parse(content);
        } catch (error) {
            console.error(`Error summarizing article: ${error.message}`);
            return null;
        }
    }

    /**
     * Generate a complete blog post from research bundle
     */
    async generateBlogPost(researchBundle) {
        const prompt = `Create a comprehensive blog post using this research bundle:

${JSON.stringify(researchBundle, null, 2)}

REQUIREMENTS:

1. YAML FRONTMATTER (first lines):
---
title: "Compelling Title (60-70 chars)"
date: ${researchBundle.generatedDate || new Date().toISOString()}
author: "AI Research Assistant"
tags: ${JSON.stringify(researchBundle.tags || [])}
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

Generate the COMPLETE Markdown blog post now (including frontmatter).`;

        const payload = {
            model: 'deepseek-chat',
            messages: [
                {
                    role: 'system',
                    content: 'You are an expert technical writer specializing in AI/ML/Data Science. Write comprehensive, well-researched blog posts with proper citations.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            temperature: 0.2,
            max_tokens: 4000
        };

        try {
            const response = await axios.post(this.baseUrl, payload, {
                headers: this.headers,
                timeout: 60000
            });
            return response.data.choices[0].message.content;
        } catch (error) {
            console.error(`Error generating blog post: ${error.message}`);
            return null;
        }
    }

    /**
     * Save blog post to file
     */
    async saveBlogPost(content, outputDir = './content/blog') {
        // Extract title from frontmatter
        const titleMatch = content.includes('title:') 
            ? content.split('title:')[1].split('\n')[0] 
            : 'ai-research-update';
        const title = titleMatch.trim().replace(/['"]/g, '');

        // Create slug
        const slug = title
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, '')
            .replace(/\s+/g, '-');

        // Create filename
        const date = new Date().toISOString().split('T')[0];
        const filename = `${date}-${slug}.md`;

        // Ensure directory exists
        await fs.mkdir(outputDir, { recursive: true });

        // Write file
        const filepath = path.join(outputDir, filename);
        await fs.writeFile(filepath, content, 'utf8');

        console.log(`✅ Blog post saved: ${filepath}`);
        return filepath;
    }
}

/**
 * Example usage
 */
async function main() {
    // Get API key from environment
    const apiKey = process.env.DEEPSEEK_API_KEY;
    if (!apiKey) {
        console.error('❌ Error: DEEPSEEK_API_KEY environment variable not set');
        console.error('Set it with: export DEEPSEEK_API_KEY="your-api-key"');
        process.exit(1);
    }

    // Initialize generator
    const generator = new DeepSeekBlogGenerator(apiKey);

    // Example articles (replace with real data from NewsAPI/RSS)
    const sampleArticles = [
        {
            title: 'New Breakthrough in Large Language Models',
            url: 'https://example.com/article1',
            date: '2025-11-06',
            content: 'Researchers have announced a significant breakthrough in large language model efficiency...'
        },
        {
            title: 'Advances in Computer Vision for Medical Imaging',
            url: 'https://example.com/article2',
            date: '2025-11-05',
            content: 'A new computer vision model achieves state-of-the-art results in medical image analysis...'
        }
    ];

    console.log('📊 Summarizing articles...');
    const summaries = [];
    for (const article of sampleArticles) {
        const summary = await generator.summarizeArticle(article);
        if (summary) {
            summaries.push(summary);
            console.log(`  ✓ Summarized: ${article.title.substring(0, 50)}...`);
        }
    }

    // Create research bundle
    const researchBundle = {
        generatedDate: new Date().toISOString(),
        topic: 'AI, Machine Learning & Data Science Updates',
        sources: summaries,
        totalSources: summaries.length,
        tags: ['artificial-intelligence', 'machine-learning', 'data-science']
    };

    console.log('\n✍️  Generating blog post...');
    const blogContent = await generator.generateBlogPost(researchBundle);

    if (blogContent) {
        console.log('\n💾 Saving blog post...');
        const filepath = await generator.saveBlogPost(blogContent);
        console.log(`\n🎉 Success! Blog post created at: ${filepath}`);

        // Print stats
        const wordCount = blogContent.split(/\s+/).length;
        const citationCount = (blogContent.match(/\[\d+\]/g) || []).length;
        console.log('\n📈 Stats:');
        console.log(`  - Word count: ${wordCount}`);
        console.log(`  - Citations: ${citationCount}`);
        console.log(`  - Sources: ${summaries.length}`);
    } else {
        console.error('\n❌ Failed to generate blog post');
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });
}

module.exports = { DeepSeekBlogGenerator };
