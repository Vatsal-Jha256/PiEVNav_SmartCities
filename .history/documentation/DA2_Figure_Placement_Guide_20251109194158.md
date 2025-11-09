# DA-2 Figure Placement Guide
## IoT-Based EV Navigation & Charging Station Management System

This document provides a comprehensive guide for all figures, images, and media files required for the presentation slides.

---

## 📋 Table of Contents
1. [Figure Overview](#figure-overview)
2. [Slide-by-Slide Figure Guide](#slide-by-slide-figure-guide)
3. [Media Files](#media-files)
4. [Figure Specifications](#figure-specifications)
5. [Generation Instructions](#generation-instructions)

---

## 📊 Figure Overview

| Slide | Figure Type | File Name | Status | Priority |
|-------|-------------|-----------|--------|----------|
| 1 | Title Background | `title_background.png` | Optional | Low |
| 8 | System Architecture Diagram | `system_architecture.png` | Required | High |
| 9 | Hardware Components Diagram | `hardware_block_diagram.png` | Required | High |
| 10 | A* Algorithm Flowchart | `astar_algorithm.png` | Optional | Medium |
| 11 | RL Algorithm Diagram | `rl_algorithm_diagram.png` | Optional | Medium |
| 12 | Servo Control Diagram | `servo_control_diagram.png` | Optional | Medium |
| 13 | Grid Optimization Visualization | `grid_optimization.png` | Optional | Medium |
| 15 | **Bhubaneswar Map with Stations** | `bhubaneswar_station_map.png` | **Required** | **Critical** |
| 16 | **Hardware Setup Photo** | `hardware_setup.jpg` | **Required** | **Critical** |
| 16 | **Prototype Image** | `prototype.jpeg` | **Required** | **Critical** |
| 17 | **RL Convergence Graph** | `rl_convergence_graph.png` | **Required** | **Critical** |
| 18 | **Performance Comparison Chart** | `performance_comparison.png` | **Required** | **Critical** |
| 19 | **Demo Screenshots** | `demo_screenshots.png` | **Required** | **Critical** |
| 19 | **Demo Video** | [Google Drive Link] | **Required** | **Critical** |
| 22 | Impact Metrics Chart | `impact_metrics.png` | Optional | Medium |

---

## 🎯 Slide-by-Slide Figure Guide

### SLIDE 1: Title Slide
**Figure:** Title Background (Optional)
- **File:** `title_background.png`
- **Description:** Background image related to smart cities, EVs, or Bhubaneswar
- **Specifications:**
  - Size: 1920×1080px (16:9 aspect ratio)
  - Format: PNG or JPG
  - Style: Professional, subtle, not distracting from text
- **Alternative:** Use solid color background with SDG icons

---

### SLIDE 8: System Architecture - Overview
**Figure:** System Architecture Diagram
- **File:** `system_architecture.png`
- **Description:** High-level system architecture showing Hardware, Software, and Cloud layers
- **Content Should Include:**
  - Three main layers: Hardware, Software, Cloud
  - Components: Raspberry Pi, OLED, Keypad, Servo Motor
  - Data flow arrows
  - RL Placement Algorithm box
- **Style:** Clean, professional diagram with labeled boxes and arrows
- **Color Scheme:** Blue/Green theme (sustainability)
- **Generation:** Can be created using `visualization/create_figures.py` → `create_system_architecture_diagram()`

---

### SLIDE 9: System Architecture - Detailed Design
**Figure:** Hardware Block Diagram
- **File:** `hardware_block_diagram.png`
- **Description:** Detailed hardware components and connections
- **Content Should Include:**
  - Raspberry Pi 4 (center)
  - Connected components: OLED Display, 4×4 Keypad, Servo Motor (SG90), GPS Module
  - Connection lines showing data flow
  - Component labels with specifications
- **Style:** Technical diagram, clear component labels
- **Generation:** Can be created using `visualization/create_figures.py` → `create_hardware_block_diagram()`

---

### SLIDE 10: Routing Algorithm - A* Pathfinding
**Figure:** A* Algorithm Flowchart (Optional but Recommended)
- **File:** `astar_algorithm.png`
- **Description:** Visual representation of A* pathfinding algorithm
- **Content Should Include:**
  - Flowchart showing: Start → Calculate f(n) = g(n) + h(n) → Select node → Check goal → Update path
  - Formula: f(n) = g(n) + h(n) prominently displayed
  - Example path visualization on a small grid
- **Style:** Flowchart with decision diamonds and process rectangles

---

### SLIDE 11: RL-Based Station Placement
**Figure:** RL Algorithm Diagram (Optional but Recommended)
- **File:** `rl_algorithm_diagram.png`
- **Description:** Reinforcement Learning process visualization
- **Content Should Include:**
  - State-Action-Reward cycle diagram
  - UCB formula: UCB(i) = μ_i + c·√(ln(N) / n_i)
  - Episode progression visualization
  - Grid cells with station placement actions
- **Style:** RL process diagram with labeled components

---

### SLIDE 12: Hardware Integration - Servo Steering Logic
**Figure:** Servo Control Diagram (Optional but Recommended)
- **File:** `servo_control_diagram.png`
- **Description:** Servo motor control logic visualization
- **Content Should Include:**
  - Servo motor with three positions: Left (-90°), Center (0°), Right (90°)
  - Decision logic: angle_diff > 15° → Right, < -15° → Left, else → Straight
  - OLED display mockup showing navigation info
- **Style:** Technical diagram with code-like logic flow

---

### SLIDE 13: Station Placement Optimization
**Figure:** Grid Optimization Visualization (Optional but Recommended)
- **File:** `grid_optimization.png`
- **Description:** Grid-based optimization process
- **Content Should Include:**
  - 1km × 1km grid overlay on Bhubaneswar
  - Three phases: Exploration (Episodes 1-3), Exploitation (4-7), Refinement (8-10)
  - Station placement evolution across episodes
- **Style:** Grid visualization with color-coded phases

---

### SLIDE 15: Bhubaneswar Grid & Station Placement Map ⭐ **CRITICAL**
**Figure:** Bhubaneswar Map with Grid and Stations
- **File:** `bhubaneswar_station_map.png`
- **Description:** Interactive/static map of Bhubaneswar showing grid overlay and 25 charging stations
- **Content Must Include:**
  - Map of Bhubaneswar city boundaries
  - 1km × 1km grid overlay (visible grid lines)
  - 25 charging stations marked with:
    - Red markers = Strategic locations (City Center, KIIT, Patia, Railway Station, Airport)
    - Blue markers = Grid-based optimal placements
  - Coverage heatmap showing accessibility zones (within 2km radius)
  - Legend explaining markers and colors
  - Title: "Bhubaneswar EV Charging Station Placement (25 Stations)"
- **Key Locations to Highlight:**
  - City Center (20.2961, 85.8245)
  - KIIT University area
  - Patia
  - Railway Station
  - Airport
- **Style:** Professional map visualization, high resolution
- **Generation:** 
  - Use `visualization/bhubaneswar_map_visualization.py` to generate
  - Output: `results/bhubaneswar_ev_stations_map.png`
  - Can also use `visualization/create_figures.py` → `create_station_placement_map()`

---

### SLIDE 16: Hardware Setup & Navigation Interface ⭐ **CRITICAL**
**Figure 1:** Hardware Setup Photo
- **File:** `hardware_setup.jpg`
- **Description:** High-quality photograph of the complete hardware setup
- **Content Must Include:**
  - Raspberry Pi 4 with all components connected
  - OLED display showing navigation information
  - 4×4 keypad visible
  - Servo motor (SG90) in view
  - GPS module (if visible)
  - Clean, well-lit setup
  - Professional background (white/neutral)
- **Photography Tips:**
  - Use good lighting (natural or studio)
  - Multiple angles: top view, side view, close-up of OLED
  - Ensure all components are clearly visible
  - Remove clutter from background
  - Use high resolution (at least 1920×1080px)

**Figure 2:** Prototype Image ⭐ **CRITICAL**
- **File:** `prototype.jpeg`
- **Description:** Image of the working prototype/system
- **Content Should Include:**
  - Complete working system in action
  - Can be same as hardware setup or different angle
  - Shows system operational (OLED displaying info, servo positioned)
  - Professional presentation
- **Location:** Place in presentation root or `documentation/images/prototype.jpeg`
- **Note:** This is a required file mentioned in the request

---

### SLIDE 17: RL Optimization Convergence ⭐ **CRITICAL**
**Figure:** RL Convergence Graph
- **File:** `rl_convergence_graph.png`
- **Description:** Line graph showing reward improvement over 10 episodes
- **Content Must Include:**
  - X-axis: Episodes (1-10)
  - Y-axis: Reward value
  - Line graph showing:
    - Episodes 1-3: Exploration phase (low, variable rewards, around -150)
    - Episodes 4-7: Rapid improvement (steep upward trend)
    - Episodes 8-10: Convergence (stable around -85)
  - Annotations:
    - "Exploration Phase" for episodes 1-3
    - "Exploitation Phase" for episodes 4-7
    - "Convergence" for episodes 8-10
  - Key metrics text box:
    - Initial reward: -150
    - Final reward: -85
    - Improvement: 43%
    - Convergence: Episode 7
  - Grid lines for readability
  - Professional styling
- **Style:** Clean line graph with annotations, professional colors
- **Generation:** Can be created using `visualization/create_figures.py` → `create_rl_performance_graphs()`

---

### SLIDE 18: Station Placement Performance ⭐ **CRITICAL**
**Figure:** Performance Comparison Chart
- **File:** `performance_comparison.png`
- **Description:** Bar chart comparing Random, K-Means, and RL (Our) methods
- **Content Must Include:**
  - Three methods: Random, K-Means, RL (Our)
  - Three metrics (can be separate charts or grouped):
    1. **Average Distance** (km):
       - Random: 3.2 km
       - K-Means: 2.4 km
       - RL (Our): 1.8 km
    2. **Coverage** (%):
       - Random: 68%
       - K-Means: 82%
       - RL (Our): 92%
    3. **Travel Time** (minutes):
       - Random: 12 min
       - K-Means: 9 min
       - RL (Our): 6.5 min
  - Color coding: RL (Our) in distinct color (green/blue)
  - Improvement percentages shown
  - Legend
  - Title: "Performance Comparison: Station Placement Methods"
- **Style:** Grouped bar chart or three separate bar charts, professional styling
- **Generation:** Can be created using `visualization/create_figures.py` → `create_rl_performance_graphs()`

---

### SLIDE 19: Real-Time Navigation Demo ⭐ **CRITICAL**
**Figure 1:** Demo Screenshots (Collage)
- **File:** `demo_screenshots.png`
- **Description:** Collage of screenshots/photos showing system in action
- **Content Must Include (4-panel layout):**
  1. **Keypad Input:** Photo of user entering destination via 4×4 keypad
  2. **OLED Display:** Close-up of OLED showing navigation info:
     - "→ RIGHT TURN"
     - "Distance: 2.5 km"
     - "ETA: 8 minutes"
     - "Battery: 65%"
     - "Next Station: ST05"
  3. **Servo Motor:** Photo showing servo motor pointing in turn direction (left/right/straight)
  4. **GPS Tracking:** Screenshot of map showing real-time GPS tracking and route
- **Layout:** 2×2 grid or 1×4 horizontal layout
- **Style:** Consistent lighting and styling across all images

**Figure 2:** Demo Video ⭐ **CRITICAL**
- **File:** Demo Video (Google Drive Link)
- **Description:** Video demonstration of the complete system
- **Content Should Include:**
  - User input via keypad
  - System calculating route
  - OLED display updating with navigation info
  - Servo motor moving to indicate turns
  - Real-time GPS tracking on map
  - Complete navigation flow (2-3 minutes recommended)
- **Video Specifications:**
  - Duration: 2-5 minutes
  - Resolution: 1080p (1920×1080) minimum
  - Format: MP4 (H.264 codec)
  - Audio: Optional (background music or narration)
  - Quality: High quality, well-lit, clear visuals
- **Google Drive Link Template:**
  ```
  [INSERT GOOGLE DRIVE LINK HERE]
  Example: https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing
  ```
- **Instructions:**
  1. Upload video to Google Drive
  2. Set sharing permissions to "Anyone with the link can view"
  3. Copy the shareable link
  4. Replace `[INSERT GOOGLE DRIVE LINK HERE]` in this document
  5. Add link to presentation slide
- **Current Status:** ⚠️ **PENDING** - Please add Google Drive link below:
  ```
  Demo Video Drive Link: [INSERT GOOGLE DRIVE LINK HERE]
  ```

---

### SLIDE 22: Impact on Society and Environment (Optional)
**Figure:** Impact Metrics Chart
- **File:** `impact_metrics.png`
- **Description:** Visual representation of quantified impact
- **Content Should Include:**
  - Three impact categories: Social, Environmental, Economic
  - Key metrics:
    - 30% reduction in travel time
    - 25% increase in EV adoption potential
    - 2.5 tons CO₂ saved per EV annually
    - 92% city coverage
  - Can be infographic style or bar/pie charts
- **Style:** Infographic or chart format

---

## 📁 Media Files

### Required Files Checklist
- [ ] `bhubaneswar_station_map.png` - Slide 15
- [ ] `hardware_setup.jpg` - Slide 16
- [ ] `prototype.jpeg` - Slide 16 ⭐
- [ ] `rl_convergence_graph.png` - Slide 17
- [ ] `performance_comparison.png` - Slide 18
- [ ] `demo_screenshots.png` - Slide 19
- [ ] Demo Video (Google Drive Link) - Slide 19 ⭐
- [ ] `system_architecture.png` - Slide 8
- [ ] `hardware_block_diagram.png` - Slide 9

### Optional Files
- [ ] `title_background.png` - Slide 1
- [ ] `astar_algorithm.png` - Slide 10
- [ ] `rl_algorithm_diagram.png` - Slide 11
- [ ] `servo_control_diagram.png` - Slide 12
- [ ] `grid_optimization.png` - Slide 13
- [ ] `impact_metrics.png` - Slide 22

### File Organization
```
SmartCityPiEVNav/
├── documentation/
│   ├── images/
│   │   ├── prototype.jpeg          ⭐ REQUIRED
│   │   ├── hardware_setup.jpg
│   │   ├── demo_screenshots.png
│   │   └── ...
│   └── DA2_Figure_Placement_Guide.md
├── visualization/
│   ├── figures/
│   │   ├── system_architecture.png
│   │   ├── hardware_block_diagram.png
│   │   ├── rl_convergence_graph.png
│   │   ├── performance_comparison.png
│   │   └── ...
│   └── ...
└── results/
    └── bhubaneswar_ev_stations_map.png
```

---

## 📐 Figure Specifications

### Image Resolution Requirements
- **Presentation Slides:** 1920×1080px (16:9 aspect ratio)
- **High-Quality Prints:** 300 DPI minimum
- **File Formats:**
  - Photos: JPG (high quality, 90%+ compression)
  - Diagrams/Charts: PNG (lossless)
  - Maps: PNG or JPG (high resolution)

### Color Scheme
- **Primary Colors:** Blue (#2E86AB) and Green (#2E8B57) for sustainability theme
- **Accent Colors:** 
  - Red: Strategic stations
  - Blue: Grid-based stations
  - Yellow/Orange: Warnings/alerts
- **Background:** White or light neutral (#F5F5F5)
- **Text:** Dark gray (#333333) or black for readability

### Typography
- **Titles:** Bold, 18-24pt
- **Labels:** Regular, 12-14pt
- **Body Text:** Regular, 10-12pt
- **Font Family:** Arial, Calibri, or similar sans-serif

---

## 🛠️ Generation Instructions

### 1. Bhubaneswar Station Map (Slide 15)
```bash
cd /home/vatsal/Projects/SmartCityPiEVNav
python visualization/bhubaneswar_map_visualization.py
# Output: results/bhubaneswar_ev_stations_map.png
```

**Or use the figure generator:**
```bash
python visualization/create_figures.py
# Output: visualization/figures/station_placement_map.pdf
# Convert PDF to PNG if needed
```

### 2. RL Convergence Graph (Slide 17)
```bash
python visualization/create_figures.py
# Output: visualization/figures/rl_performance_graphs.pdf
# Extract convergence graph and save as PNG
```

### 3. Performance Comparison Chart (Slide 18)
```bash
python visualization/create_figures.py
# Output: visualization/figures/rl_performance_graphs.pdf
# Extract comparison chart and save as PNG
```

### 4. System Architecture Diagram (Slide 8)
```bash
python visualization/create_figures.py
# Output: visualization/figures/system_architecture.pdf
# Convert to PNG for presentation
```

### 5. Hardware Block Diagram (Slide 9)
```bash
python visualization/create_figures.py
# Output: visualization/figures/hardware_block_diagram.pdf
# Convert to PNG for presentation
```

### 6. Hardware Setup Photo (Slide 16)
**Manual Steps:**
1. Set up hardware components on clean surface
2. Use good lighting (natural or studio lights)
3. Take multiple photos from different angles:
   - Top-down view (showing all components)
   - Side view (showing connections)
   - Close-up of OLED display
4. Select best photo(s)
5. Edit if needed (brightness, contrast, crop)
6. Save as `hardware_setup.jpg` (high quality)

### 7. Prototype Image (Slide 16) ⭐
**Manual Steps:**
1. Take photo of working prototype
2. Ensure system is operational (OLED showing info, servo positioned)
3. Use professional lighting and background
4. Save as `prototype.jpeg`
5. Place in `documentation/images/prototype.jpeg`

### 8. Demo Screenshots (Slide 19)
**Manual Steps:**
1. Capture 4 screenshots/photos:
   - Keypad input
   - OLED display
   - Servo motor
   - GPS tracking map
2. Arrange in 2×2 grid using image editor (GIMP, Photoshop, or online tool)
3. Add labels if needed
4. Save as `demo_screenshots.png`

### 9. Demo Video (Slide 19) ⭐
**Recording Steps:**
1. Set up camera/phone to record system
2. Record complete navigation flow:
   - User input via keypad
   - System processing
   - OLED display updates
   - Servo motor movements
   - GPS tracking
3. Edit video (trim, add titles, narration if needed)
4. Export as MP4 (1080p, H.264)
5. Upload to Google Drive
6. Set sharing to "Anyone with the link"
7. Copy shareable link
8. **Add link below:**

```
═══════════════════════════════════════════════════════════════
DEMO VIDEO GOOGLE DRIVE LINK:
[INSERT GOOGLE DRIVE LINK HERE]

Upload Date: [DATE]
Video Duration: [X minutes]
Resolution: [1080p / 4K]
═══════════════════════════════════════════════════════════════
```

---

## ✅ Final Checklist Before Presentation

### Critical Files (Must Have)
- [ ] `bhubaneswar_station_map.png` - Slide 15
- [ ] `hardware_setup.jpg` - Slide 16
- [ ] `prototype.jpeg` - Slide 16 ⭐
- [ ] `rl_convergence_graph.png` - Slide 17
- [ ] `performance_comparison.png` - Slide 18
- [ ] `demo_screenshots.png` - Slide 19
- [ ] Demo Video Google Drive Link - Slide 19 ⭐

### Important Files (Should Have)
- [ ] `system_architecture.png` - Slide 8
- [ ] `hardware_block_diagram.png` - Slide 9

### Optional Files (Nice to Have)
- [ ] `astar_algorithm.png` - Slide 10
- [ ] `rl_algorithm_diagram.png` - Slide 11
- [ ] `servo_control_diagram.png` - Slide 12
- [ ] `grid_optimization.png` - Slide 13
- [ ] `impact_metrics.png` - Slide 22

### Quality Checks
- [ ] All images are high resolution (1920×1080px minimum)
- [ ] All images are properly named and organized
- [ ] Demo video is uploaded and link is accessible
- [ ] Prototype image is clear and professional
- [ ] All figures match the color scheme
- [ ] Text in images is readable
- [ ] All file paths are correct in presentation

---

## 📝 Notes

1. **Priority:** Focus on completing Critical files first (marked with ⭐)
2. **Backup:** Keep backup copies of all figures
3. **Formats:** Use PNG for diagrams, JPG for photos
4. **Naming:** Use consistent naming convention (lowercase, underscores)
5. **Version Control:** Consider adding figures to git (if not too large) or use Git LFS

---

## 🔗 Quick Links

- **PPT Content:** `documentation/DA2_PPT_Content.md`
- **Visualization Scripts:** `visualization/`
- **Results Folder:** `results/`
- **Figure Generator:** `visualization/create_figures.py`
- **Map Generator:** `visualization/bhubaneswar_map_visualization.py`

---

**Last Updated:** [DATE]
**Status:** ⚠️ Demo Video Link Pending
**Next Steps:** 
1. Generate all required figures using scripts
2. Take hardware setup and prototype photos
3. Record and upload demo video
4. Create demo screenshots collage
5. Update this document with Google Drive link

---

**Good luck with your presentation! 🚀**

