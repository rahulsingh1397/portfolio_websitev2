# n8n Blog Automation Integration Guide

## Overview
This guide explains how to integrate your n8n workflow with the blog page to automatically generate and publish blog posts.

---

## 📋 Blog Page Features

### Current Implementation
- **File:** `blog.html`
- **Dynamic Loading:** JavaScript function ready for n8n webhook integration
- **Responsive Design:** Mobile-optimized grid layout
- **Card Format:** Thumbnail, headline, preview, tags, and "Read More" button

### Blog Card Structure
Each blog post displays:
- **Thumbnail:** Image URL or emoji icon
- **Metadata:** Date, read time, author
- **Headline:** Post title (H3)
- **Preview:** First 3 lines with "..." truncation
- **Tags:** Topic categories
- **Read More Button:** Links to full blog post

---

## 🔧 n8n Workflow Setup

### Step 1: Create Webhook Endpoint

In your n8n workflow, create a **Webhook** node:

```
Webhook Node Settings:
- HTTP Method: GET
- Path: /blogs
- Response Mode: Last Node
- Response Data: JSON
```

### Step 2: Expected JSON Format

Your n8n workflow should return JSON in this format:

```json
{
  "blogs": [
    {
      "id": "unique-blog-id-123",
      "title": "The Future of AI in Data Science",
      "preview": "Exploring how artificial intelligence is revolutionizing data analysis and predictive modeling in modern enterprises. Discover the latest trends...",
      "thumbnail": "https://example.com/image.jpg",
      "date": "2025-11-05",
      "readTime": "5 min",
      "author": "AI Generated",
      "tags": ["AI", "Machine Learning", "Data Science"],
      "slug": "future-of-ai-in-data-science"
    },
    {
      "id": "unique-blog-id-456",
      "title": "Building Scalable ML Pipelines",
      "preview": "Best practices for designing and deploying production-ready machine learning pipelines that scale with your business needs...",
      "thumbnail": "🤖",
      "date": "2025-11-04",
      "readTime": "8 min",
      "author": "AI Generated",
      "tags": ["MLOps", "DevOps", "Cloud"],
      "slug": "building-scalable-ml-pipelines"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the blog post |
| `title` | string | Yes | Blog post headline (displayed as H3) |
| `preview` | string | Yes | Short preview text (3 lines max, auto-truncated) |
| `thumbnail` | string | Yes | Image URL (http/https) or emoji (📊, 🤖, ⚡) |
| `date` | string | Yes | Publication date (format: YYYY-MM-DD) |
| `readTime` | string | Yes | Estimated reading time (e.g., "5 min") |
| `author` | string | Yes | Author name (e.g., "AI Generated") |
| `tags` | array | Yes | Array of topic tags (max 3-5 recommended) |
| `slug` | string | Yes | URL-friendly slug for blog post page |

---

## 🚀 Integration Steps

### 1. Update Webhook URL in blog.html

Open `blog.html` and locate line ~470:

```javascript
// Replace this URL with your n8n webhook URL
const n8nWebhookURL = 'YOUR_N8N_WEBHOOK_URL_HERE';
```

Replace with your actual n8n webhook URL:

```javascript
const n8nWebhookURL = 'https://your-n8n-instance.com/webhook/blogs';
```

### 2. Enable Auto-Loading

Uncomment line ~490 in `blog.html`:

```javascript
// Load blogs on page load
loadBlogsFromN8N(); // ← Uncomment this line
```

### 3. Optional: Enable Auto-Refresh

Uncomment line ~493 to refresh blogs every 5 minutes:

```javascript
// Auto-refresh blogs every 5 minutes
setInterval(loadBlogsFromN8N, 5 * 60 * 1000); // ← Uncomment this line
```

---

## 🤖 Sample n8n Workflow

### Workflow Structure

```
1. Schedule Trigger (Daily/Weekly)
   ↓
2. AI Content Generator (OpenAI/Claude/etc.)
   ↓
3. Format JSON Response
   ↓
4. Store in Database (Optional)
   ↓
5. Webhook Response
```

### Example Nodes

#### Node 1: Schedule Trigger
```
Trigger: Schedule
Interval: Every day at 9:00 AM
```

#### Node 2: OpenAI Node
```
Model: GPT-4
Prompt: "Generate a blog post about [topic] in data science"
Max Tokens: 1000
```

#### Node 3: Function Node (Format JSON)
```javascript
// Format AI response into blog structure
const aiContent = $input.first().json.choices[0].message.content;

// Extract title, preview, tags from AI content
const title = aiContent.split('\n')[0].replace(/^#\s*/, '');
const preview = aiContent.substring(0, 300) + '...';

return {
  json: {
    blogs: [{
      id: `blog-${Date.now()}`,
      title: title,
      preview: preview,
      thumbnail: '🤖',
      date: new Date().toISOString().split('T')[0],
      readTime: '5 min',
      author: 'AI Generated',
      tags: ['AI', 'Data Science', 'Machine Learning'],
      slug: title.toLowerCase().replace(/\s+/g, '-')
    }]
  }
};
```

#### Node 4: Webhook Response
```
Response Mode: Last Node
Response Data: JSON
```

---

## 📝 Creating Individual Blog Post Pages

### Option 1: Static HTML Files

Create individual HTML files for each blog post:

```
blog-post.html?id=future-of-ai-in-data-science
```

### Option 2: Dynamic Loading (Recommended)

Create a single `blog-post.html` template that loads content dynamically:

```javascript
// In blog-post.html
const urlParams = new URLSearchParams(window.location.search);
const blogId = urlParams.get('id');

// Fetch full blog content from n8n
fetch(`https://your-n8n-instance.com/webhook/blog/${blogId}`)
  .then(response => response.json())
  .then(data => {
    // Render full blog content
    document.getElementById('blogTitle').textContent = data.title;
    document.getElementById('blogContent').innerHTML = data.content;
  });
```

---

## 🎨 Customization

### Change Color Scheme

The blog page uses your website's color palette:
- **Primary:** Cyan (#00f5ff)
- **Secondary:** Blue (#0080ff)
- **Accent:** Purple (#8B5CF6)

To customize, edit the CSS variables in `blog.html`.

### Modify Card Layout

Blog cards use CSS Grid with auto-fill:

```css
.blogs-grid {
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 2.5rem;
}
```

Adjust `minmax(380px, 1fr)` to change card width.

### Add Filters/Categories

Add filter buttons above the blog grid:

```html
<div class="blog-filters">
    <button class="filter-btn active" data-filter="all">All</button>
    <button class="filter-btn" data-filter="ai">AI</button>
    <button class="filter-btn" data-filter="ml">Machine Learning</button>
</div>
```

---

## 🔒 Security Considerations

### CORS Configuration

Ensure your n8n webhook allows requests from your domain:

```javascript
// In n8n Webhook settings
Access-Control-Allow-Origin: https://yourdomain.com
```

### Rate Limiting

Implement rate limiting in n8n to prevent abuse:

```javascript
// In n8n Function node
const requestCount = $('Webhook').item.json.headers['x-request-count'];
if (requestCount > 100) {
  throw new Error('Rate limit exceeded');
}
```

### API Authentication (Optional)

Add API key authentication:

```javascript
// In blog.html
const response = await fetch(n8nWebhookURL, {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
});
```

---

## 🧪 Testing

### Test with Sample Data

1. Create a test webhook in n8n
2. Return sample JSON data
3. Verify blog cards render correctly
4. Check responsive design on mobile

### Debug Mode

Enable console logging in `blog.html`:

```javascript
console.log('Fetched blogs:', data.blogs);
```

---

## 📊 Analytics Integration

### Track Blog Views

Add analytics to blog cards:

```javascript
document.querySelectorAll('.blog-card').forEach(card => {
  card.addEventListener('click', () => {
    const blogId = card.getAttribute('data-blog-id');
    // Send to analytics
    gtag('event', 'blog_view', { blog_id: blogId });
  });
});
```

---

## 🚨 Troubleshooting

### Issue: Blogs Not Loading

**Solution:**
1. Check browser console for errors
2. Verify n8n webhook URL is correct
3. Test webhook directly in browser
4. Check CORS settings

### Issue: Thumbnail Not Displaying

**Solution:**
- Ensure image URLs are valid and accessible
- Check if using emoji (no http/https prefix)
- Verify image CORS headers

### Issue: Preview Text Too Long

**Solution:**
- Limit preview to 300 characters in n8n
- CSS will auto-truncate to 3 lines

---

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Webhook Integration Guide](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [OpenAI API for Content Generation](https://platform.openai.com/docs)

---

## 🎯 Next Steps

1. ✅ Set up n8n workflow
2. ✅ Configure webhook endpoint
3. ✅ Test with sample data
4. ✅ Create blog post template page
5. ✅ Deploy and monitor

---

**Last Updated:** November 5, 2025  
**Version:** 1.0  
**Author:** Portfolio Website Team
