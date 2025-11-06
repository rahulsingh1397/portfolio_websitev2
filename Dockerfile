# Use lightweight nginx image to serve static files
FROM nginx:alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Copy all website files to nginx html directory
COPY . .

# Remove unnecessary files from the container
RUN rm -f Dockerfile docker-compose.yml .gitignore *.md

# Create nginx configuration for SPA routing
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index data-scientist-portfolio.html index.html; \
    \
    # Enable gzip compression \
    gzip on; \
    gzip_vary on; \
    gzip_min_length 1024; \
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript; \
    \
    # Handle SPA routing \
    location / { \
        try_files $uri $uri/ /data-scientist-portfolio.html; \
    } \
    \
    # Cache static assets \
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ { \
        expires 1y; \
        add_header Cache-Control "public, immutable"; \
    } \
    \
    # Security headers \
    add_header X-Frame-Options "SAMEORIGIN" always; \
    add_header X-Content-Type-Options "nosniff" always; \
    add_header X-XSS-Protection "1; mode=block" always; \
}' > /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
