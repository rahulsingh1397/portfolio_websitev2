# Docker Setup Guide for Data Scientist Portfolio

## 🐳 Quick Start

### Prerequisites
- Docker installed on your system
- Portfolio files in the current directory

### Build and Run

#### Option 1: Docker Compose (Recommended)
```bash
# Build and start the container
docker-compose up --build

# Or run in background
docker-compose up -d --build

# Access at http://localhost:8080
```

#### Option 2: Docker Commands
```bash
# Build the image
docker build -t data-scientist-portfolio .

# Run the container
docker run -d -p 8080:80 --name portfolio data-scientist-portfolio

# Access at http://localhost:8080
```

## 📋 Available Commands

### Development
```bash
# Start container
docker-compose up

# Stop container
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up --build
```

### Production
```bash
# Build optimized image
docker build -t portfolio:latest .

# Run with restart policy
docker run -d -p 80:80 --restart unless-stopped portfolio:latest
```

## 🔧 Configuration

### Environment Variables
- `NGINX_HOST`: Set hostname (default: localhost)
- `NGINX_PORT`: Set internal port (default: 80)

### Custom Ports
Modify `docker-compose.yml` to change host port:
```yaml
ports:
  - "3000:80"  # Access at http://localhost:3000
```

## 🚀 Deployment Options

### Local Development
```bash
docker-compose up
```

### Cloud Deployment
The container can be deployed to:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**
- **Heroku**
- **Any Docker-compatible platform**

### Example: Deploy to DigitalOcean
```bash
# Build and tag
docker build -t portfolio .
docker tag portfolio registry.digitalocean.com/your-registry/portfolio

# Push and deploy
docker push registry.digitalocean.com/your-registry/portfolio
```

## 📊 Container Details

### Image Size
- **Base Image:** nginx:alpine (~22MB)
- **Final Size:** ~50MB (with your files)

### Features
- ✅ **Static file serving** via nginx
- ✅ **Gzip compression** enabled
- ✅ **SPA routing** support
- ✅ **Security headers** configured
- ✅ **Caching** for static assets
- ✅ **Health checks** included
- ✅ **Responsive** across all devices

### Security
- Non-root nginx process
- Security headers configured
- No sensitive files in container
- Minimal attack surface

## 🏗️ Architecture

```
┌─────────────────────────────┐
│     Docker Container        │
│  ┌───────────────────────┐  │
│  │   nginx:alpine        │  │
│  │   ┌─────────────────┐ │  │
│  │   │ Static Files    │ │  │
│  │   │ - HTML          │ │  │
│  │   │ - CSS           │ │  │
│  │   │ - JS            │ │  │
│  │   │ - 3D Models     │ │  │
│  │   └─────────────────┘ │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

## 🔍 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using port 8080
lsof -i :8080

# Use different port
docker-compose up -p 8081:80
```

#### Container Won't Start
```bash
# Check logs
docker-compose logs portfolio

# Rebuild
docker-compose down
docker-compose up --build
```

#### Files Not Updating
```bash
# Force rebuild
docker-compose down --volumes
docker-compose up --build --force-recreate
```

## 🧪 Testing

### Local Testing
```bash
# Test locally
curl http://localhost:8080

# Browser testing
open http://localhost:8080
```

### Container Health Check
```bash
# Check if container is running
docker ps

# Check container health
docker inspect data-scientist-portfolio
```

## 📁 File Structure

```
data-scientist-portfolio/
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Docker Compose setup
├── .dockerignore       # Files to exclude from build
├── README-DOCKER.md    # This file
├── data-scientist-portfolio.html  # Main site
├── blog.html           # Blog page
├── models/             # 3D models
├── assets/             # Images and resources
└── ...
```

## 🎯 Next Steps

1. **Build and test locally** using commands above
2. **Customize** the Dockerfile if needed
3. **Deploy** to your preferred platform
4. **Monitor** using Docker logs and health checks

## 📞 Support

For issues with Docker setup:
1. Check container logs: `docker-compose logs`
2. Verify files are copied: `docker exec portfolio ls -la`
3. Test nginx config: `docker exec portfolio nginx -t`

---

**Happy containerizing!** 🐳✨
