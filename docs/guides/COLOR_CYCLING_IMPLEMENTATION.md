# Color Cycling Implementation Guide

## Overview
This guide shows how to add color cycling (Cyan → Magenta → Green → Yellow) to the robotic eye's light.

## Step 1: Add lightMaterial Variable

**Location:** Line 968 (after `let roboticEyeModel = null;`)

**Add this line:**
```javascript
let lightMaterial = null; // Store reference to light material for color cycling
```

**Result should look like:**
```javascript
const loader = new GLTFLoader();
let roboticEyeModel = null;
let lightMaterial = null; // Store reference to light material for color cycling
```

---

## Step 2: Store Material Reference

**Location:** Inside the `Light_Low_Poly_0` material setup (around line 1018)

**Find this code:**
```javascript
// Light material with emissive
if (child.name === 'Light_Low_Poly_0') {
    materials.forEach((mat) => {
        mat.map = emissiveTexture;
        mat.emissiveMap = emissiveTexture;
        mat.emissive = new THREE.Color('#00f5ff');
        mat.emissiveIntensity = 9000.0;
        mat.metalness = 1.0;
        mat.roughness = 0.3;
        mat.transparent = true;
        mat.opacity = 1.0;
        mat.side = THREE.DoubleSide;
    });
    return;
}
```

**Add these 2 lines BEFORE the `});` closing:**
```javascript
        // Store reference for color cycling
        lightMaterial = mat;
```

**Result should look like:**
```javascript
// Light material with emissive
if (child.name === 'Light_Low_Poly_0') {
    materials.forEach((mat) => {
        mat.map = emissiveTexture;
        mat.emissiveMap = emissiveTexture;
        mat.emissive = new THREE.Color('#00f5ff');
        mat.emissiveIntensity = 9000.0;
        mat.metalness = 1.0;
        mat.roughness = 0.3;
        mat.transparent = true;
        mat.opacity = 1.0;
        mat.side = THREE.DoubleSide;
        
        // Store reference for color cycling
        lightMaterial = mat;
    });
    return;
}
```

---

## Step 3: Add Color Palette and Cycling Logic

**Location:** Before the `animate()` function (around line 1167-1169)

**Find this code:**
```javascript
window.addEventListener('mousemove', onMouseMove);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
```

**Replace with:**
```javascript
window.addEventListener('mousemove', onMouseMove);

// Color cycling palette
const colors = [
    new THREE.Color('#00f5ff'), // Cyan
    new THREE.Color('#ff00ff'), // Magenta
    new THREE.Color('#00ff00'), // Green
    new THREE.Color('#ffff00')  // Yellow
];

let colorTime = 0;

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    
    // Color cycling for robotic eye light
    if (lightMaterial) {
        colorTime += 0.005; // Control speed (0.005 = slow, 0.01 = medium, 0.02 = fast)
        
        // Calculate which two colors to interpolate between
        const colorIndex = Math.floor(colorTime) % colors.length;
        const nextColorIndex = (colorIndex + 1) % colors.length;
        const t = colorTime % 1; // Interpolation factor (0 to 1)
        
        // Interpolate between current and next color
        const currentColor = colors[colorIndex];
        const nextColor = colors[nextColorIndex];
        const interpolatedColor = new THREE.Color().copy(currentColor).lerp(nextColor, t);
        
        // Apply the interpolated color
        lightMaterial.emissive.copy(interpolatedColor);
    }
    
    renderer.render(scene, camera);
}
```

---

## How It Works

1. **Color Array**: Defines 4 colors that the eye will cycle through
2. **colorTime**: Increments each frame to track position in the cycle
3. **Interpolation**: Smoothly blends between colors using Three.js `lerp()` function
4. **Speed Control**: Adjust `colorTime += 0.005` to change speed:
   - 0.002 = Very slow (200 seconds per cycle)
   - 0.005 = Slow (80 seconds per cycle)
   - 0.01 = Medium (40 seconds per cycle)
   - 0.02 = Fast (20 seconds per cycle)

## Color Customization

To change colors, modify the colors array:

```javascript
const colors = [
    new THREE.Color('#ff0000'), // Red
    new THREE.Color('#00ff00'), // Green
    new THREE.Color('#0000ff'), // Blue
    new THREE.Color('#ffff00')  // Yellow
];
```

Or use hex values:
```javascript
const colors = [
    new THREE.Color(0x00f5ff), // Cyan
    new THREE.Color(0xff00ff), // Magenta
    new THREE.Color(0x00ff00), // Green
    new THREE.Color(0xffff00)  // Yellow
];
```

## Testing

After implementing:
1. Refresh browser
2. Watch the robotic eye light
3. It should smoothly transition: Cyan → Magenta → Green → Yellow → Cyan (repeat)
4. Complete cycle takes ~200 seconds at default speed (0.005)

## Troubleshooting

**If colors don't change:**
- Check console for errors
- Verify `lightMaterial` is not null
- Check that the model loaded successfully (should see "3D Model loaded successfully" in console)

**If transition is too fast/slow:**
- Adjust the `colorTime += 0.005` value

**If colors are wrong:**
- Verify the color values in the array
- Check that `lightMaterial.emissive` is being updated (not `.color`)
