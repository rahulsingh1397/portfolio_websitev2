# How to Publish Your First Blog

This guide explains how to add blog posts to your portfolio website.

## Quick Start

### Step 1: Create the Blog HTML File

1. Copy `BLOG_TEMPLATE.html` and rename it with your blog's slug (e.g., `my-first-blog.html`)
2. Replace the placeholders:
   - `BLOG_TITLE` → Your blog title
   - `BLOG_DATE` → Publication date (e.g., "Dec 5, 2024")
   - `BLOG_READ_TIME` → Estimated read time (e.g., "5 min read")
   - `BLOG_TAGS` → Add tag spans like: `<span class="tag">AI</span><span class="tag">Python</span>`
   - `BLOG_CONTENT` → Your blog content in HTML format

### Step 2: Update blogs.json

Add your blog entry to `blogs/blogs.json`:

```json
{
  "blogs": [
    {
      "slug": "my-first-blog",
      "title": "My First Blog Post",
      "excerpt": "A brief description of what this blog is about...",
      "date": "Dec 5, 2024",
      "readTime": "5 min read",
      "tags": ["AI", "Machine Learning", "Python"],
      "icon": "🤖",
      "thumbnail": null
    }
  ]
}
```

### Step 3: Push to GitHub

```bash
git add blogs/
git commit -m "Add new blog post: My First Blog"
git push origin main
```

## Blog Entry Fields

| Field | Required | Description |
|-------|----------|-------------|
| `slug` | Yes | URL-friendly name (no spaces, lowercase) |
| `title` | Yes | Blog title displayed on cards |
| `excerpt` | Yes | Short description (1-2 sentences) |
| `date` | Yes | Publication date |
| `readTime` | No | Estimated read time (default: "5 min read") |
| `tags` | No | Array of topic tags |
| `icon` | No | Emoji icon for card (if no thumbnail) |
| `thumbnail` | No | Path to thumbnail image |

## Example: Complete Blog Entry

### 1. blogs.json
```json
{
  "blogs": [
    {
      "slug": "getting-started-with-langchain",
      "title": "Getting Started with LangChain for AI Applications",
      "excerpt": "Learn how to build powerful AI applications using LangChain, from basic concepts to production-ready implementations.",
      "date": "Dec 5, 2024",
      "readTime": "8 min read",
      "tags": ["LangChain", "AI", "LLMs", "Python"],
      "icon": "🔗",
      "thumbnail": null
    }
  ]
}
```

### 2. blogs/getting-started-with-langchain.html
Copy the template and fill in your content with proper HTML formatting.

## Tips for Writing Blog Content

### Use Proper HTML Structure
```html
<h2>Introduction</h2>
<p>Your introduction paragraph here...</p>

<h2>Main Section</h2>
<p>Content with <code>inline code</code> examples.</p>

<pre><code>
# Code block example
def hello_world():
    print("Hello, World!")
</code></pre>

<h3>Subsection</h3>
<ul>
    <li>Bullet point 1</li>
    <li>Bullet point 2</li>
</ul>

<blockquote>
    This is a quote or important callout.
</blockquote>
```

### Adding Images
```html
<img src="../assets/blog-images/my-image.png" alt="Description of image">
```

## Automation with n8n (Optional)

You can automate blog publishing using n8n workflows:

1. **Trigger**: Webhook or scheduled trigger
2. **Generate Content**: Use AI (OpenAI, Claude) to generate blog content
3. **Create Files**: Use n8n to create the HTML file and update blogs.json
4. **Push to GitHub**: Use GitHub API to commit and push changes

See `N8N_BLOG_INTEGRATION_GUIDE.md` for detailed automation setup.

## What Happens When You Publish

1. **Main Page**: The "Latest Insights" section automatically shows your 3 most recent blogs
2. **Blog Page**: `blog.html` displays all your blog posts in a grid
3. **Individual Posts**: Each blog has its own page at `blogs/[slug].html`

## Troubleshooting

### Blog not showing up?
- Check that `blogs.json` is valid JSON (use a JSON validator)
- Ensure the `slug` matches the HTML filename (without .html)
- Clear browser cache and refresh

### Styling issues?
- Make sure you're using the correct HTML tags
- Check that images exist at the specified paths

## File Structure
```
blogs/
├── blogs.json              # Blog index (required)
├── BLOG_TEMPLATE.html      # Template for new blogs
├── HOW_TO_PUBLISH_BLOG.md  # This guide
└── my-first-blog.html      # Your blog posts
```
