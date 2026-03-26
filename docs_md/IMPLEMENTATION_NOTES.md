# 3D Model Implementation Notes

## Changes Made

### 1. Updated Three.js Implementation
- Replaced old Three.js CDN with modern ES6 module imports using import maps
- Added GLTFLoader for loading 3D models (.glb format)
- Added OrbitControls for smooth camera movement

### 2. Camera Settings (Matching Reference)
- Field of View: 110 degrees
- Camera Position: (0, 1.5, 1)
- Near/Far clipping: 0.5 to 100

### 3. Enhanced Lighting Setup
- Ambient Light: 0.5 intensity
- Directional Light: 2.5 intensity at (0, 10, 5)
- Back Light: 0.8 intensity at (0, -5, -5)
- Point Light: 1.2 intensity at (0, 8, 0)
- Spotlight: 2.0 intensity with focused beam

### 4. Model Configuration
- Scale: 4x in all dimensions
- Position: (0, 0.58, 0.1)
- Mouse tracking with clamped rotation (-π/2.5 to π/2.5)

### 5. Material Properties
- **Lens**: Transparent (0.3 opacity), low metalness
- **Light**: Emissive cyan (#00f5ff) with 9000 intensity, includes texture mapping
- **Various plastics and metals**: Custom colors matching reference design

### 6. Files Added
- `models/robotic_eye.glb` - 3D model file (2.2 MB)
- `models/textures/Light_emissive.png` - Emissive texture for glowing effect

### 7. Fallback System
If the 3D model fails to load, the system automatically creates a procedural robotic eye with:
- Sphere geometry for the main eye
- Cyan iris (#00f5ff) matching the site's color scheme
- Three mechanical rings with emissive effects
- Same positioning and mouse tracking as the GLTF model

## How It Works

1. The page loads the Three.js library as ES6 modules
2. GLTFLoader attempts to load `robotic_eye.glb`
3. If successful, applies custom materials and textures
4. If failed, creates a procedural eye as fallback
5. Mouse movement rotates the eye smoothly
6. OrbitControls provide damped camera movement

## Browser Compatibility

The implementation uses:
- ES6 modules (supported in all modern browsers)
- Import maps (Chrome 89+, Firefox 108+, Safari 16.4+)
- WebGL for 3D rendering

## Performance

- Model size: ~2.2 MB (loads once, cached by browser)
- Texture size: Small PNG for emissive effect
- Smooth 60 FPS animation with requestAnimationFrame
- Responsive sizing based on container dimensions
