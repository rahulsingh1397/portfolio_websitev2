# Data Scientist Portfolio Website

A modern, interactive portfolio website featuring a 3D robotic eye model built with Three.js.

## Features

- **Interactive 3D Model**: Robotic eye that tracks mouse movement
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Gradient effects, smooth animations, and cyan accent colors
- **Sections**:
  - Hero with 3D model
  - About with statistics
  - Skills showcase
  - Featured projects
  - Contact form

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

## Baseline Version

This is the **baseline version** of the portfolio website. If future changes cause issues, you can always revert to this stable version using:

```bash
git checkout baseline
```

## License

© 2025 DataSci.Pro. All rights reserved.

## Author

Rahul Singh
- GitHub: [@rahulsingh1397](https://github.com/rahulsingh1397)
