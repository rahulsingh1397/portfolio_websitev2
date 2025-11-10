# 📁 Professional Portfolio Folder Structure

## 🏗️ Root Directory
```
portfolio/
├── src/                          # Source code
├── docs/                         # Documentation
├── automation/                   # Automation scripts
├── config/                       # Configuration files
├── public/                       # Public assets
├── blog-automation/             # Blog automation (existing)
├── n8n-blog-automation/         # n8n workflows (existing)
├── .env                         # Environment variables
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── netlify.toml                 # Netlify configuration
├── _headers                     # Security headers
├── _redirects                   # URL redirects
├── docker-compose.yml           # Docker configuration
├── Dockerfile                   # Docker image
└── README.md                    # Project documentation
```

## 📁 Source Code (`src/`)
```
src/
├── html/                        # HTML files
│   ├── index.html              # Main portfolio page
│   ├── blog.html               # Individual blog post
│   └── blogs.html              # Blog listing page
├── assets/                      # Static assets
│   ├── images/                 # Image assets
│   ├── models/                 # 3D models
│   ├── icons/                  # Icons and favicons
│   └── videos/                 # Video files
├── css/                        # Stylesheets
├── js/                         # JavaScript files
└── components/                 # Reusable components
```

## 📁 Documentation (`docs/`)
```
docs/
├── guides/                     # User guides
│   ├── BLOG_AUTOMATION_SETUP.md
│   ├── N8N_BLOG_INTEGRATION_GUIDE.md
│   ├── NETLIFY_DEPLOYMENT_GUIDE.md
│   ├── TOUCH_SUPPORT_IMPLEMENTATION.md
│   └── COLOR_CYCLING_IMPLEMENTATION.md
├── deployment/                 # Deployment docs
│   ├── DEPLOY_CHECKLIST.md
│   ├── README-DOCKER.md
│   └── IMPLEMENTATION_NOTES.md
└── api/                       # API documentation
```

## 🤖 Automation (`automation/`)
```
automation/
├── n8n/                       # n8n workflow files
│   ├── workflow-blog-automation.json
│   └── n8n-config.js
├── blog-scripts/              # Blog generation scripts
│   ├── generate_blog.py
│   ├── generate_blog_demo.py
│   ├── requirements.txt
│   └── test_local.bat
└── workflows/                 # GitHub Actions
    └── .github/
        └── workflows/
            └── auto-blog.yml
```

## ⚙️ Configuration (`config/`)
```
config/
├── netlify/                   # Netlify configs
│   ├── _headers
│   ├── _redirects
│   └── netlify.toml
├── security/                  # Security configs
│   ├── .env
│   └── .env.example
└── docker/                    # Docker configs
    ├── docker-compose.yml
    └── Dockerfile
```

## 🌐 Public (`public/`)
```
public/
├── css/                       # Compiled CSS
├── js/                        # Compiled JavaScript
└── assets/                    # Public assets
```

## 📊 Existing Structure Integration
- **blog-automation/** → Keep as-is (Python scripts)
- **n8n-blog-automation/** → Keep as-is (n8n workflows)
- **models/** → Move to `src/assets/models/`
- **assets/** → Move to `src/assets/images/`

## 🔄 Migration Steps
1. ✅ Created folder structure
2. ✅ Organized HTML files
3. ✅ Organized assets
4. ✅ Updated .gitignore
5. ✅ Created structure documentation

## 🎯 Next Steps
- Update file paths in HTML files
- Test all links and references
- Update build scripts
- Verify 3D model paths
