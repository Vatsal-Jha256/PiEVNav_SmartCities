# Raspberry Pi Installation Guide

## Why This Guide?

Some Python packages require system libraries to be installed first. On Raspberry Pi, this is especially important because:
- ARM architecture may not have pre-built wheels for all packages
- Some geospatial libraries (like `rasterio`) depend on GDAL system libraries
- The code gracefully handles missing optional dependencies

## Quick Installation (Without Optional Dependencies)

If you just want to get started quickly without map background overlays:

```bash
pip install -r requirements.txt
```

The code will work fine without `contextily` - it will use enhanced fallback backgrounds instead.

## Full Installation (With All Optional Features)

### Step 1: Install System Dependencies

```bash
# Update package list
sudo apt-get update

# Install GDAL (required for contextily/rasterio)
sudo apt-get install -y gdal-bin libgdal-dev python3-gdal

# Install other geospatial dependencies
sudo apt-get install -y libgeos-dev libproj-dev
```

### Step 2: Set GDAL Environment Variable

```bash
# Find your GDAL version
gdal-config --version

# Set it as environment variable (replace X.X.X with your version)
export GDAL_VERSION=$(gdal-config --version)
```

### Step 3: Install Python Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# If contextily was commented out, install it separately
pip install contextily>=1.4.0
```

## Troubleshooting

### Error: "gdal-config: command not found"
- Make sure you installed `libgdal-dev`: `sudo apt-get install libgdal-dev`

### Error: "GDAL API version must be specified"
- Set the GDAL_VERSION environment variable as shown in Step 2
- Or add it to your `~/.bashrc` to make it permanent:
  ```bash
  echo 'export GDAL_VERSION=$(gdal-config --version)' >> ~/.bashrc
  source ~/.bashrc
  ```

### Error: "Failed to build rasterio"
- Ensure all system dependencies are installed (Step 1)
- Try installing rasterio separately: `pip install rasterio`
- If still failing, you can skip contextily - the code works without it

## What Works Without contextily?

All core functionality works without `contextily`:
- ✅ EV navigation and routing
- ✅ Station placement visualization
- ✅ Map generation with Folium
- ✅ Hardware control
- ✅ RL optimization

The only difference is that static matplotlib plots won't have OpenStreetMap tile backgrounds - they'll use enhanced fallback backgrounds instead.




