#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# build.sh — Build the Cookie Cutter Generator into a single executable
# Usage: chmod +x build.sh && ./build.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e  # exit on any error

APP_NAME="CookieCutterGenerator"

echo "╔══════════════════════════════════════════╗"
echo "║     Cookie Cutter Generator — Build      ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── Check Python ──────────────────────────────────────────────────────────────
echo "▶ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $PYTHON_VERSION"

# ── Check dependencies ────────────────────────────────────────────────────────
echo ""
echo "▶ Checking dependencies..."
python3 -c "import cadquery" 2>/dev/null    || { echo "  ✗ cadquery not found. Run: conda install -c conda-forge cadquery"; exit 1; }
python3 -c "import cv2" 2>/dev/null         || { echo "  ✗ opencv-python not found. Run: pip install opencv-python"; exit 1; }
python3 -c "import skimage" 2>/dev/null     || { echo "  ✗ scikit-image not found. Run: pip install scikit-image"; exit 1; }
python3 -c "import scipy" 2>/dev/null       || { echo "  ✗ scipy not found. Run: pip install scipy"; exit 1; }
python3 -c "import shapely" 2>/dev/null     || { echo "  ✗ shapely not found. Run: pip install shapely"; exit 1; }
python3 -c "import PyInstaller" 2>/dev/null || { echo "  ✗ pyinstaller not found. Run: pip install pyinstaller"; exit 1; }
echo "  ✓ All dependencies found"

# ── Clean previous build ──────────────────────────────────────────────────────
echo ""
echo "▶ Cleaning previous build artifacts..."
rm -rf build dist __pycache__ *.spec
echo "  ✓ Clean"

# ── Run PyInstaller ───────────────────────────────────────────────────────────
echo ""
echo "▶ Building executable (this takes 2–5 minutes)..."
echo ""

pyinstaller \
  --onefile \
  --windowed \
  --name "$APP_NAME" \
  --collect-all cadquery \
  --collect-all OCC \
  --collect-all cadquery_occ \
  --hidden-import skimage.morphology \
  --hidden-import skimage.filters \
  --hidden-import skimage.util \
  --hidden-import scipy.interpolate \
  --hidden-import scipy.spatial.distance \
  --hidden-import shapely \
  --hidden-import shapely.geometry \
  --hidden-import shapely.ops \
  main.py

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
if [ -f "dist/$APP_NAME" ]; then
  SIZE=$(du -sh "dist/$APP_NAME" | awk '{print $1}')
  echo "╔══════════════════════════════════════════╗"
  echo "║              ✓ Build complete!           ║"
  echo "╚══════════════════════════════════════════╝"
  echo ""
  echo "  Output:  dist/$APP_NAME"
  echo "  Size:    $SIZE"
  echo ""
  echo "  To run:  ./dist/$APP_NAME"
  echo ""
  echo "  NOTE: On Mac, first run may require:"
  echo "        right-click → Open (to bypass Gatekeeper)"
else
  echo "✗ Build failed — check output above for errors"
  exit 1
fi
