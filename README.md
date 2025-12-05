# Data Scientist Portfolio Website

A modern, interactive portfolio website featuring 3D models, animated backgrounds, and live GitHub integration built with Three.js and GSAP.

## Features

- **Interactive 3D Models**: 
  - Robotic eye on landing page that tracks mouse movement
  - ANN (Artificial Neural Network) 3D model in Achievements section
- **Animated Hexagon Grid Background**: Interactive hover effects with pulsing animations
- **Live GitHub Stats**: Real-time repository and language statistics via GitHub API
- **Responsive Design**: Optimized for desktop and mobile with touch support
- **Modern UI**: Gradient effects, smooth animations, and cyan/blue accent colors
- **Navigation Sparkle Effect**: Animated sparkle on active nav items (click & scroll)
- **Sections**:
  - Hero with 3D robotic eye
  - About Me with profile image
  - Skills showcase
  - Featured projects
  - Achievements with ANN model
  - GitHub Activity carousel
  - Contact form with calendar booking

## Version 2.0 Changes (December 2024)

### New Features
- **Profile Image**: Added circular profile image with glow effects in About Me section
- **GitHub Activity Carousel**: Auto-scrolling cards with live stats (Repositories, Python, Jupyter, JS/HTML, Other)
- **Interactive Hexagon Grid**: Mouse-following highlight with neighbor fade effect
- **Navigation Sparkle**: Sparkle animation triggers on both click and scroll navigation

### Improvements
- **ANN Model**: Zoomed out camera for better visibility (position: 45, 10, 1)
- **Hexagon Hover**: Precise mouse tracking with proper grid offset calculation
- **GitHub Carousel**: Global accessibility for button controls, touch/swipe support
- **Removed Stats**: Stars Earned, Total Forks, and Followers cards removed from GitHub section

### Bug Fixes
- Fixed hexagon hover position sync with cursor
- Fixed GitHub carousel prev/next buttons not working
- Fixed sparkle effect not showing on scroll navigation

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6 modules)
- **3D Graphics**: Three.js v0.160.0
  - GLTFLoader for 3D model loading
  - OrbitControls for camera interaction
- **3D Model**: Robotic eye (.glb format)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/rahulsingh1397/portfolio_websitev2.git
cd portfolio_websitev2
```

2. Start a local server:
```bash
python -m http.server 8000
```

3. Open your browser and navigate to:
```
http://localhost:8000/data-scientist-portfolio.html
```

## Project Structure

```
.
├── data-scientist-portfolio.html   # Main HTML file
├── models/
│   ├── robotic_eye.glb            # 3D model file
│   └── textures/
│       └── Light_emissive.png     # Emissive texture
├── IMPLEMENTATION_NOTES.md         # Technical implementation details
└── README.md                       # This file
```

## 3D Model Configuration

- **Scale**: 70x
- **Camera Position**: (0, 1.5, 7)
- **Base Rotation**: -π/10 (tilted to look at center)
- **Mouse Tracking**: Relative to model container
- **Lighting**: Multi-source setup (ambient, directional, point, spotlight)

## Version Control

### Branches
- **main**: Current production version
- **v2.0-major-update**: Version 2.0 with all new features (this branch)
- **stable-v1-backup**: Previous stable version backup

### Rollback Instructions
If v2.0 causes issues, revert to the previous stable version:

```bash
git checkout stable-v1-backup
# Or to restore main to previous version:
git checkout main
git reset --hard stable-v1-backup
git push origin main --force
```

## License

© 2025 DataSci.Pro. All rights reserved.

## Author

Rahul Singh
- GitHub: [@rahulsingh1397](https://github.com/rahulsingh1397)
