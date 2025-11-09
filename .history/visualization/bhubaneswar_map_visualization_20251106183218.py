#!/usr/bin/env python3
"""
Bhubaneswar EV Charging Station Map Visualization
Creates a map of Bhubaneswar with grid overlay and 25 strategically placed charging stations
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Dict, Tuple
import logging
import requests

# Add project root to path
sys.path.append(os.path.abspath('.'))

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    print("⚠️ Folium not available. Will create static map only.")

try:
    import contextily as ctx
    CONTEXTILY_AVAILABLE = True
except ImportError:
    CONTEXTILY_AVAILABLE = False
    print("⚠️ Contextily not available. Will use enhanced background.")

try:
    # Try importing from root level modules
    from gridding import CityGridding
    GRIDDING_AVAILABLE = True
except ImportError:
    try:
        from modules.utils.gridding import CityGridding
        GRIDDING_AVAILABLE = True
    except ImportError:
        GRIDDING_AVAILABLE = False
        print("⚠️ CityGridding not available. Will use manual grid creation.")

# Bhubaneswar coordinates (approximate city center)
BHUBANESWAR_CENTER = (20.2961, 85.8245)  # (lat, lon)
BHUBANESWAR_BOUNDS = {
    'min_lat': 20.20,
    'max_lat': 20.40,
    'min_lon': 85.70,
    'max_lon': 85.95
}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_optimal_stations(num_stations: int = 25, 
                              city_bounds: Dict = None,
                              grid_cells: List[Dict] = None) -> List[Dict]:
    """
    Generate 25 strategically placed charging stations for Bhubaneswar.
    Uses a combination of grid-based placement and strategic locations.
    
    Args:
        num_stations: Number of stations to place
        city_bounds: City boundary dictionary
        grid_cells: List of grid cell dictionaries
        
    Returns:
        List of station dictionaries with lat, lon, and metadata
    """
    if city_bounds is None:
        city_bounds = BHUBANESWAR_BOUNDS
    
    stations = []
    
    # Key locations in Bhubaneswar (strategic points)
    key_locations = [
        (20.2961, 85.8245, "City Center"),  # Master Canteen area
        (20.2644, 85.8281, "Acharya Vihar"),  # Near KIIT
        (20.3100, 85.8500, "Patia"),  # IT Hub
        (20.2800, 85.8000, "Old Town"),  # Old Bhubaneswar
        (20.3200, 85.8200, "Nayapalli"),  # Residential area
        (20.2500, 85.8500, "Bhubaneswar Railway Station"),
        (20.3000, 85.8800, "Airport Area"),
        (20.2700, 85.7800, "Lingaraj Temple Area"),
        (20.2900, 85.8600, "Infocity"),
        (20.3100, 85.7900, "Vani Vihar"),
    ]
    
    # Place stations at key locations first
    for i, (lat, lon, name) in enumerate(key_locations[:min(num_stations, len(key_locations))]):
        stations.append({
            'station_id': f'ST{i+1:02d}',
            'lat': lat,
            'lon': lon,
            'name': name,
            'type': 'strategic'
        })
    
    # If we need more stations, distribute them across the city
    remaining = num_stations - len(stations)
    if remaining > 0:
        # Create a grid-based distribution for remaining stations
        lat_range = city_bounds['max_lat'] - city_bounds['min_lat']
        lon_range = city_bounds['max_lon'] - city_bounds['min_lon']
        
        # Calculate grid dimensions
        grid_size = int(np.ceil(np.sqrt(remaining * 2)))  # Slightly more cells than needed
        
        for i in range(remaining):
            # Use a quasi-random distribution
            row = (i // grid_size) + 1
            col = (i % grid_size) + 1
            
            # Add some randomness to avoid perfect grid
            lat_offset = np.random.uniform(-0.01, 0.01)
            lon_offset = np.random.uniform(-0.01, 0.01)
            
            lat = city_bounds['min_lat'] + (row / (grid_size + 1)) * lat_range + lat_offset
            lon = city_bounds['min_lon'] + (col / (grid_size + 1)) * lon_range + lon_offset
            
            # Ensure within bounds
            lat = np.clip(lat, city_bounds['min_lat'], city_bounds['max_lat'])
            lon = np.clip(lon, city_bounds['min_lon'], city_bounds['max_lon'])
            
            stations.append({
                'station_id': f'ST{len(stations)+1:02d}',
                'lat': lat,
                'lon': lon,
                'name': f'Grid Station {len(stations)+1}',
                'type': 'grid'
            })
    
    return stations[:num_stations]


def create_bhubaneswar_grid(city_name: str = "Bhubaneswar", 
                           grid_size_km: float = 1.0) -> List[Dict]:
    """
    Create grid cells for Bhubaneswar.
    
    Args:
        city_name: Name of the city
        grid_size_km: Size of grid cells in kilometers
        
    Returns:
        List of grid cell dictionaries
    """
    if GRIDDING_AVAILABLE:
        try:
            gridder = CityGridding(primary_grid_size_km=grid_size_km, 
                                  fetch_osm_features=False)
            
            # Use coordinates for Bhubaneswar
            grid_cells = gridder.create_city_grid(
                city_name=city_name,
                coordinates=(BHUBANESWAR_CENTER[0], BHUBANESWAR_CENTER[1])
            )
            
            logger.info(f"✅ Created {len(grid_cells)} grid cells for {city_name} using CityGridding")
            return grid_cells
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create grid using CityGridding: {e}")
            logger.info("Creating manual grid...")
    
    # Fallback: Create manual grid
    grid_cells = []
    lat_range = BHUBANESWAR_BOUNDS['max_lat'] - BHUBANESWAR_BOUNDS['min_lat']
    lon_range = BHUBANESWAR_BOUNDS['max_lon'] - BHUBANESWAR_BOUNDS['min_lon']
    
    # Approximate grid size in degrees (1km ≈ 0.009 degrees)
    grid_size_deg = grid_size_km * 0.009
    
    num_lat = int(np.ceil(lat_range / grid_size_deg))
    num_lon = int(np.ceil(lon_range / grid_size_deg))
    
    grid_id = 0
    for i in range(num_lat):
        for j in range(num_lon):
            min_lat = BHUBANESWAR_BOUNDS['min_lat'] + i * grid_size_deg
            max_lat = min(BHUBANESWAR_BOUNDS['min_lat'] + (i + 1) * grid_size_deg, 
                         BHUBANESWAR_BOUNDS['max_lat'])
            min_lon = BHUBANESWAR_BOUNDS['min_lon'] + j * grid_size_deg
            max_lon = min(BHUBANESWAR_BOUNDS['min_lon'] + (j + 1) * grid_size_deg,
                         BHUBANESWAR_BOUNDS['max_lon'])
            
            grid_cells.append({
                'grid_id': f'grid_{grid_id:03d}',
                'cell_id': f'grid_{grid_id:03d}',
                'min_lat': min_lat,
                'max_lat': max_lat,
                'min_lon': min_lon,
                'max_lon': max_lon,
                'center_lat': (min_lat + max_lat) / 2,
                'center_lon': (min_lon + max_lon) / 2,
                'area_km2': grid_size_km ** 2,
                'corners': [
                    [min_lon, min_lat],
                    [min_lon, max_lat],
                    [max_lon, max_lat],
                    [max_lon, min_lat]
                ]
            })
            grid_id += 1
    
    logger.info(f"✅ Created {len(grid_cells)} manual grid cells")
    return grid_cells


def create_static_map(stations: List[Dict], 
                     grid_cells: List[Dict] = None,
                     output_path: str = "bhubaneswar_ev_stations_map.png") -> str:
    """
    Create a static map visualization of Bhubaneswar with stations and grid.
    
    Args:
        stations: List of station dictionaries
        grid_cells: List of grid cell dictionaries
        output_path: Output file path
        
    Returns:
        Path to saved visualization
    """
    logger.info("📊 Creating static map visualization...")
    
    # Set up matplotlib with publication quality
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Set bounds
    bounds = BHUBANESWAR_BOUNDS
    ax.set_xlim(bounds['min_lon'], bounds['max_lon'])
    ax.set_ylim(bounds['min_lat'], bounds['max_lat'])
    
    # Add background color
    ax.set_facecolor('#e6f3ff')
    
    # Add grid cells if provided
    if grid_cells:
        logger.info(f"   Adding {len(grid_cells)} grid cells...")
        for cell in grid_cells:
            width = cell.get('max_lon', 0) - cell.get('min_lon', 0)
            height = cell.get('max_lat', 0) - cell.get('min_lat', 0)
            
            rect = patches.Rectangle(
                (cell.get('min_lon', 0), cell.get('min_lat', 0)),
                width, height,
                linewidth=0.5, edgecolor='blue', facecolor='lightblue', 
                alpha=0.15, zorder=1
            )
            ax.add_patch(rect)
    
    # Add stations
    logger.info(f"   Adding {len(stations)} charging stations...")
    strategic_stations = [s for s in stations if s.get('type') == 'strategic']
    grid_stations = [s for s in stations if s.get('type') == 'grid']
    
    # Plot strategic stations (larger, red)
    if strategic_stations:
        for station in strategic_stations:
            ax.scatter(station['lon'], station['lat'], 
                      c='red', marker='s', s=200, 
                      edgecolors='white', linewidth=2, 
                      zorder=10, label='Strategic Station' if station == strategic_stations[0] else '')
    
    # Plot grid stations (smaller, blue)
    if grid_stations:
        for station in grid_stations:
            ax.scatter(station['lon'], station['lat'],
                      c='blue', marker='o', s=150,
                      edgecolors='white', linewidth=1.5,
                      zorder=10, label='Grid Station' if station == grid_stations[0] else '')
    
    # Add station labels
    for station in stations:
        ax.annotate(station['station_id'], 
                   (station['lon'], station['lat']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='yellow', alpha=0.7, edgecolor='black'))
    
    # Add title and labels
    ax.set_title('Bhubaneswar EV Charging Station Placement\n25 Stations with Grid Overlay', 
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor='red', 
               markersize=10, markeredgecolor='white', markeredgewidth=2,
               label='Strategic Stations'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue',
               markersize=10, markeredgecolor='white', markeredgewidth=1.5,
               label='Grid Stations'),
        Line2D([0], [0], color='blue', linewidth=1, alpha=0.5,
               label='Grid Cells')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
             frameon=True, fancybox=True, shadow=True)
    
    # Add info box
    info_text = f"""Total Stations: {len(stations)}
Strategic: {len(strategic_stations)}
Grid-based: {len(grid_stations)}
City: Bhubaneswar, Odisha"""
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black'),
           family='monospace')
    
    plt.tight_layout()
    
    # Save figure
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.savefig(output_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Static map saved to: {output_path}")
    return output_path


def create_interactive_map(stations: List[Dict],
                          grid_cells: List[Dict] = None,
                          output_path: str = "bhubaneswar_ev_stations_map.html") -> str:
    """
    Create an interactive Folium map of Bhubaneswar with stations and grid.
    
    Args:
        stations: List of station dictionaries
        grid_cells: List of grid cell dictionaries
        output_path: Output file path
        
    Returns:
        Path to saved HTML map
    """
    if not FOLIUM_AVAILABLE:
        logger.warning("⚠️ Folium not available. Skipping interactive map.")
        return None
    
    logger.info("🌐 Creating interactive map...")
    
    # Create map centered on Bhubaneswar
    m = folium.Map(
        location=[BHUBANESWAR_CENTER[0], BHUBANESWAR_CENTER[1]],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add grid cells
    if grid_cells:
        logger.info(f"   Adding {len(grid_cells)} grid cells...")
        for cell in grid_cells:
            folium.Rectangle(
                bounds=[[cell.get('min_lat', 0), cell.get('min_lon', 0)],
                       [cell.get('max_lat', 0), cell.get('max_lon', 0)]],
                color='blue',
                weight=1,
                fillOpacity=0.1,
                fillColor='lightblue',
                popup=f"Grid: {cell.get('grid_id', 'Unknown')}"
            ).add_to(m)
    
    # Add stations
    logger.info(f"   Adding {len(stations)} charging stations...")
    for station in stations:
        color = 'red' if station.get('type') == 'strategic' else 'blue'
        icon = 'star' if station.get('type') == 'strategic' else 'info-sign'
        
        folium.Marker(
            location=[station['lat'], station['lon']],
            popup=folium.Popup(
                f"<b>{station['station_id']}</b><br>"
                f"Name: {station.get('name', 'N/A')}<br>"
                f"Type: {station.get('type', 'N/A').title()}<br>"
                f"Coordinates: ({station['lat']:.4f}, {station['lon']:.4f})",
                max_width=200
            ),
            tooltip=station['station_id'],
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 150px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Bhubaneswar EV Charging Stations</b></p>
    <p><i class="fa fa-star" style="color:red"></i> Strategic Stations</p>
    <p><i class="fa fa-info-sign" style="color:blue"></i> Grid Stations</p>
    <p><i class="fa fa-square" style="color:lightblue"></i> Grid Cells</p>
    <p><b>Total: 25 Stations</b></p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    m.save(output_path)
    
    logger.info(f"✅ Interactive map saved to: {output_path}")
    return output_path


def main():
    """Main function to generate Bhubaneswar map with stations."""
    logger.info("🚀 Starting Bhubaneswar EV Station Map Generation...")
    
    # Create grid
    logger.info("📐 Creating city grid...")
    grid_cells = create_bhubaneswar_grid(city_name="Bhubaneswar", grid_size_km=1.0)
    
    # Generate stations
    logger.info("📍 Generating 25 charging stations...")
    stations = generate_optimal_stations(num_stations=25, 
                                        city_bounds=BHUBANESWAR_BOUNDS,
                                        grid_cells=grid_cells)
    
    # Create visualizations
    logger.info("🎨 Creating visualizations...")
    
    # Static map
    static_path = create_static_map(stations, grid_cells, 
                                   "results/bhubaneswar_ev_stations_map.png")
    
    # Interactive map
    if FOLIUM_AVAILABLE:
        interactive_path = create_interactive_map(stations, grid_cells,
                                                  "results/bhubaneswar_ev_stations_map.html")
    
    # Save station data
    import json
    stations_data = {
        'city': 'Bhubaneswar',
        'total_stations': len(stations),
        'stations': stations,
        'grid_cells': len(grid_cells) if grid_cells else 0
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/bhubaneswar_stations_data.json', 'w') as f:
        json.dump(stations_data, f, indent=2)
    
    logger.info("✅ All visualizations created successfully!")
    logger.info(f"   📊 Static map: {static_path}")
    if FOLIUM_AVAILABLE:
        logger.info(f"   🌐 Interactive map: {interactive_path}")
    logger.info(f"   💾 Station data: results/bhubaneswar_stations_data.json")
    
    return stations, grid_cells


if __name__ == "__main__":
    main()


