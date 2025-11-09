#!/usr/bin/env python3
"""
EV Navigation Main Application
Main loop for EV navigation and charging station management
"""

import time
import os
import sys
import logging
import json
from typing import Optional, Dict, List, Tuple

# Add project root to path BEFORE imports
# Get the directory containing this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent of navigation directory)
project_root = os.path.dirname(current_dir)
# Add to path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import project modules
from hardware.ev_navigation_hardware import EVNavigationHardware
from navigation.ev_routing_algorithm import EVRoutingAlgorithm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ev_navigation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EVNavigation")


class EVNavigationSystem:
    """Main EV navigation system"""
    
    def __init__(self, stations_file: str = "results/bhubaneswar_stations_data.json"):
        """Initialize navigation system"""
        self.hardware = EVNavigationHardware()
        self.routing = EVRoutingAlgorithm()
        
        # Load station data
        self.stations = self._load_stations(stations_file)
        self.current_location = None  # (lat, lon)
        self.current_heading = 0.0  # degrees
        self.battery_level = 100.0  # percentage
        self.destination_station = None
        
        # Navigation state
        self.navigation_active = False
        self.current_route = None
        self.route_step = 0
        
        logger.info("✅ EV Navigation System initialized")
    
    def _load_stations(self, stations_file: str) -> List[Dict]:
        """Load charging station data from JSON file"""
        try:
            if os.path.exists(stations_file):
                with open(stations_file, 'r') as f:
                    data = json.load(f)
                    stations = data.get('stations', [])
                    logger.info(f"✅ Loaded {len(stations)} charging stations")
                    return stations
            else:
                logger.warning(f"⚠️ Stations file not found: {stations_file}")
                logger.info("Using default Bhubaneswar stations...")
                return self._get_default_stations()
        except Exception as e:
            logger.error(f"❌ Error loading stations: {e}")
            return self._get_default_stations()
    
    def _get_default_stations(self) -> List[Dict]:
        """Get default station data if file not found"""
        return [
            {'station_id': 'ST01', 'lat': 20.2961, 'lon': 85.8245, 'name': 'City Center'},
            {'station_id': 'ST02', 'lat': 20.2644, 'lon': 85.8281, 'name': 'KIIT Area'},
            {'station_id': 'ST03', 'lat': 20.3100, 'lon': 85.8500, 'name': 'Patia IT Hub'},
            {'station_id': 'ST04', 'lat': 20.2800, 'lon': 85.8000, 'name': 'Old Town'},
            {'station_id': 'ST05', 'lat': 20.3200, 'lon': 85.8200, 'name': 'Nayapalli'},
        ]
    
    def main_menu(self):
        """Display and handle main menu"""
        while True:
            self.hardware.display_message("EV Navigation\n1:Find Station\n2:Navigate\n3:Status\n4:Exit")
            
            choice = None
            timeout = time.time() + 30  # 30 second timeout
            
            while choice is None and time.time() < timeout:
                key = self.hardware.read_keypad()
                if key and key in ['1', '2', '3', '4']:
                    choice = key
                    break
                time.sleep(0.1)
            
            if choice is None:
                self.hardware.display_message("Timeout\nReturning to menu")
                time.sleep(2)
                continue
            
            if choice == '1':
                self.find_station()
            elif choice == '2':
                self.start_navigation()
            elif choice == '3':
                self.show_status()
            elif choice == '4':
                self.hardware.display_message("Shutting down\nGoodbye!")
                time.sleep(2)
                break
    
    def find_station(self):
        """Find nearest charging station"""
        if not self.current_location:
            self.hardware.display_message("No GPS signal\nUsing default location")
            # Use default location (Bhubaneswar center)
            self.current_location = (20.2961, 85.8245)
            time.sleep(2)
        
        # Find nearest station
        nearest = self._find_nearest_station(self.current_location)
        
        if nearest:
            distance = self._calculate_distance(
                self.current_location, 
                (nearest['lat'], nearest['lon'])
            )
            
            self.hardware.display_station_info(
                nearest['station_id'],
                distance,
                "Available"
            )
            
            # Wait for user input
            key = None
            timeout = time.time() + 10
            
            while key != '#' and time.time() < timeout:
                key = self.hardware.read_keypad()
                if key == '#':
                    self.destination_station = nearest
                    self.hardware.display_message("Navigation\nstarting...")
                    time.sleep(1)
                    self.start_navigation()
                    return
                time.sleep(0.1)
        else:
            self.hardware.display_message("No stations\nfound")
            time.sleep(2)
    
    def start_navigation(self):
        """Start navigation to destination"""
        if not self.destination_station:
            self.hardware.display_message("No destination\nSelect station first")
            time.sleep(2)
            return
        
        if not self.current_location:
            self.current_location = (20.2961, 85.8245)  # Default
        
        # Calculate route
        destination = (self.destination_station['lat'], self.destination_station['lon'])
        route = self.routing.calculate_route(self.current_location, destination)
        
        if not route:
            self.hardware.display_message("Route calculation\nfailed")
            time.sleep(2)
            return
        
        self.current_route = route
        self.route_step = 0
        self.navigation_active = True
        
        self.hardware.display_message("Navigation\nActive\nStarting route...")
        time.sleep(2)
        
        # Navigation loop
        self._navigation_loop()
    
    def _navigation_loop(self):
        """Main navigation loop"""
        update_interval = 2.0  # Update every 2 seconds
        last_update = time.time()
        
        while self.navigation_active:
            current_time = time.time()
            
            if current_time - last_update >= update_interval:
                self._update_navigation()
                last_update = current_time
            
            # Check for stop command
            key = self.hardware.read_keypad()
            if key == '*':
                self.hardware.display_message("Navigation\nstopped")
                time.sleep(1)
                self.navigation_active = False
                break
            
            time.sleep(0.1)
    
    def _update_navigation(self):
        """Update navigation display and steering"""
        if not self.current_route or self.route_step >= len(self.current_route):
            self.hardware.display_message("Arrived at\ndestination!")
            self.hardware.set_steering("STOP")
            time.sleep(3)
            self.navigation_active = False
            return
        
        # Get current step
        step = self.current_route[self.route_step]
        
        # Calculate distance and ETA
        distance = step.get('distance', 0)
        eta = step.get('eta', 0)
        
        # Get direction
        direction = step.get('direction', 'STRAIGHT')
        
        # Update display
        self.hardware.display_navigation(
            direction=direction,
            distance=distance,
            eta=eta,
            battery=self.battery_level,
            next_station=self.destination_station['station_id'] if self.destination_station else ""
        )
        
        # Update steering
        target_heading = step.get('heading', self.current_heading)
        self.hardware.update_steering_from_heading(self.current_heading, target_heading)
        
        # Simulate movement (in real system, this would come from GPS)
        # Move to next step after some time or distance
        if distance < 0.1:  # Within 100m of waypoint
            self.route_step += 1
    
    def show_status(self):
        """Display system status"""
        status_msg = f"Battery: {self.battery_level:.0f}%\n"
        status_msg += f"Location: {self.current_location[0]:.4f}\n" if self.current_location else "Location: Unknown\n"
        status_msg += f"Stations: {len(self.stations)}\n"
        status_msg += f"Nav: {'ON' if self.navigation_active else 'OFF'}"
        
        self.hardware.display_message(status_msg)
        time.sleep(5)
    
    def _find_nearest_station(self, location: Tuple[float, float]) -> Optional[Dict]:
        """Find nearest charging station to given location"""
        if not self.stations:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for station in self.stations:
            distance = self._calculate_distance(
                location,
                (station['lat'], station['lon'])
            )
            if distance < min_distance:
                min_distance = distance
                nearest = station
        
        return nearest
    
    def _calculate_distance(self, loc1: Tuple[float, float], 
                           loc2: Tuple[float, float]) -> float:
        """Calculate distance between two coordinates (Haversine formula)"""
        from math import radians, sin, cos, sqrt, atan2
        
        lat1, lon1 = radians(loc1[0]), radians(loc1[1])
        lat2, lon2 = radians(loc2[0]), radians(loc2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        # Earth radius in km
        R = 6371.0
        
        return R * c
    
    def cleanup(self):
        """Clean up system resources"""
        logger.info("Shutting down EV Navigation System...")
        self.navigation_active = False
        self.hardware.set_steering("STOP")
        self.hardware.cleanup()
        logger.info("✅ Shutdown complete")


def main():
    """Main entry point"""
    logger.info("🚀 Starting EV Navigation System...")
    
    try:
        # Initialize system
        nav_system = EVNavigationSystem()
        
        # Display startup message
        nav_system.hardware.display_message("EV Navigation\nSystem Ready\nBhubaneswar")
        time.sleep(2)
        
        # Run main menu
        nav_system.main_menu()
        
    except KeyboardInterrupt:
        logger.info("⚠️ System shutdown requested")
    except Exception as e:
        logger.error(f"❌ System error: {e}", exc_info=True)
    finally:
        if 'nav_system' in locals():
            nav_system.cleanup()
        logger.info("System shutdown complete")


if __name__ == "__main__":
    main()


