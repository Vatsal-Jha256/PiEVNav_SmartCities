# IoT-Based EV Navigation & Charging Station Management System

**Course:** BCSE316L - Design of Smart Cities  
**Institution:** Vellore Institute of Technology  
**Academic Year:** 2025-26  
**Slot:** D2+TD2

## 🎯 Project Overview

An integrated IoT-based system for EV navigation and charging station management in Bhubaneswar, combining:
- **Hardware:** Raspberry Pi, OLED display, keypad, servo motor for physical navigation feedback
- **Software:** A* routing algorithm for optimal pathfinding
- **RL Optimization:** Multi-armed bandit algorithm for strategic station placement
- **Visualization:** Interactive maps showing 25 optimally placed charging stations

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│         IoT-Based EV Navigation System                  │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼───┐         ┌────▼────┐        ┌────▼────┐
    │Hardware│         │Software │        │   RL    │
    │ Layer  │         │  Layer  │        │Optimizer│
    └───┬───┘         └────┬────┘        └────┬────┘
        │                   │                   │
    ┌───▼───────────────────▼───────────────────▼───┐
    │  Raspberry Pi + OLED + Keypad + Servo Motor  │
    │  • GPS Tracking                                │
    │  • Real-time Route Calculation                 │
    │  • Servo Steering Indication                   │
    │  • OLED Direction Display                      │
    └─────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
smart_cities/
├── README.md                          # This file
├── requirements.txt                    # Python dependencies
├── hardware/
│   ├── ev_navigation_hardware.py     # Hardware controller
│   └── hardware_setup.md             # Setup instructions
├── navigation/
│   ├── ev_navigation_main.py         # Main application
│   └── ev_routing_algorithm.py       # A* pathfinding
├── rl_optimization/
│   ├── station_placement_rl.py       # RL-based placement
│   ├── bandit_algorithms.py         # MAB algorithms
│   └── README.md                     # RL documentation
├── visualization/
│   ├── bhubaneswar_map_visualization.py  # Map generation
│   └── results/                      # Generated maps
├── documentation/
│   ├── DA2_PPT_Content.md           # Presentation content
│   └── presentation/                 # PPT files
└── data/
    └── bhubaneswar_stations.json     # Station data
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Bhubaneswar Map with Stations

```bash
python visualization/bhubaneswar_map_visualization.py
```

This creates:
- `results/bhubaneswar_ev_stations_map.png` - Static map
- `results/bhubaneswar_ev_stations_map.html` - Interactive map
- `data/bhubaneswar_stations.json` - Station coordinates

### 3. Run Navigation System (on Raspberry Pi)

```bash
python navigation/ev_navigation_main.py
```

### 4. Run RL Station Placement

```bash
python rl_optimization/station_placement_rl.py
```

## 🔧 Hardware Setup

### Required Components
- Raspberry Pi 4 (or compatible)
- SSD1306 OLED Display (128x64) - I2C
- 4x4 Matrix Keypad - GPIO
- SG90 Servo Motor - GPIO 18, PWM

### Connections

**OLED Display (I2C):**
- VCC → 3.3V (Pin 1)
- GND → Ground (Pin 6)
- SCL → SCL (Pin 5)
- SDA → SDA (Pin 3)

**Servo Motor:**
- Red (VCC) → 5V (Pin 2)
- Brown (GND) → Ground (Pin 9)
- Orange (Signal) → GPIO 18 (Pin 12)

**Keypad (4x4 Matrix):**
- Row 1-4 → GPIO 23, 24, 25, 8
- Col 1-4 → GPIO 7, 12, 16, 20

See `hardware/hardware_setup.md` for detailed instructions.

## 📊 Features

### 1. Real-Time Navigation
- A* pathfinding algorithm for optimal routes
- Hardware feedback via servo motor (steering indication)
- OLED display showing directions, distance, ETA, battery level

### 2. RL-Based Station Placement
- Multi-armed bandit (MAB) optimization
- 10 episodes of learning
- Strategic placement of 25 stations across Bhubaneswar
- Reward function: minimize travel time + maximize coverage

### 3. Interactive Visualization
- Grid-based city division (1km × 1km cells)
- Strategic stations at key locations
- Coverage heatmap showing accessibility

## 🧠 RL Algorithm Details

### Problem Formulation
- **State:** Grid cell configuration, current station placements
- **Action:** Place station at grid cell (i, j)
- **Reward:** R = -α·T - β·D + γ·C
  - T = Average travel time to stations
  - D = Distance from demand centers
  - C = Coverage score

### Algorithm: Multi-Armed Bandit (UCB)
```
UCB(i) = μ_i + c·√(ln(N) / n_i)
where:
- μ_i = average reward for arm i
- N = total number of pulls
- n_i = number of pulls for arm i
- c = exploration parameter (2.0)
```

### Episodes
- **Episode 1-3:** Exploration phase (random placements)
- **Episode 4-7:** Exploitation phase (UCB-based selection)
- **Episode 8-10:** Refinement phase (local optimization)

## 📈 Results

### Station Placement Performance
- **Coverage:** 92% of city within 2km of a station
- **Average Distance:** 1.8km to nearest station
- **Strategic Locations:** City Center, KIIT, Patia, Railway Station, Airport

### Navigation Performance
- **Route Calculation:** < 100ms
- **Display Update:** < 50ms
- **Servo Response:** < 100ms

## 🎓 SDG Alignment

- **SDG 7:** Affordable and Clean Energy - Promotes EV adoption
- **SDG 11:** Sustainable Cities - Smart infrastructure for urban mobility
- **SDG 13:** Climate Action - Reduces carbon emissions from transportation

## 📝 Documentation

- **Hardware Setup:** `hardware/hardware_setup.md`
- **RL Algorithm:** `rl_optimization/README.md`
- **Presentation:** `documentation/DA2_PPT_Content.md`

## 🔬 Technical Details

### Routing Algorithm
- **Algorithm:** A* pathfinding
- **Heuristic:** Euclidean distance (admissible)
- **Complexity:** O(b^d) where b = branching factor, d = depth

### Station Placement
- **Grid Size:** 1km × 1km cells
- **Total Stations:** 25
- **Optimization Episodes:** 10
- **Convergence:** Episode 7

## 🛠️ Development

### Testing Hardware
```bash
python hardware/ev_navigation_hardware.py
```

### Testing Routing
```bash
python navigation/ev_routing_algorithm.py
```

### Testing RL Placement
```bash
python rl_optimization/station_placement_rl.py
```
## 🙏 Acknowledgments

- Bhubaneswar Smart City Mission
- Odisha EV Policy 2.0
- OpenStreetMap for road network data

---

**Note:** This is a class project for Design of Smart Cities. Research components are simplified for educational purposes.

## 📄 Paper Submission Safety

This code is a **simplified educational version** for a class project. It uses standard Multi-Armed Bandit algorithms (UCB, Epsilon-Greedy) which are publicly available methods in reinforcement learning literature.

**Key Points:**
- ✅ Safe to publish before research paper submission
- ✅ Different implementation (400 lines vs 2000+ in research)
- ✅ Standard algorithms (not proprietary)
- ✅ Clear distinction from research work

See `PAPER_SUBMISSION_SAFETY.md` for detailed analysis.

